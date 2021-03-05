from django.core.management.base import BaseCommand
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from django.db.models import Q
import youtube_topic_tracker.models as models
from django.conf import settings
from collections import deque
from django.db import transaction
import datetime
from django.utils import timezone
'''
This management command updates the YoutubeVideo model
periodically with latest information

The periodicity of this command is handled by a crontab scheduled to run every 60 seconds
'''

# declare API constants
DEVELOPER_KEY = deque(settings.YOUTUBE_API_KEYS)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


class Command(BaseCommand):
    help = 'Update YoutubeVideo model with the latest information of a topic'
    youtube = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_youtube_api_handle()

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch_size',
            type=int,
            default=200,
            help='The batch size value used for bulk updating or inserting to the database table',
        )
        parser.add_argument(
            '--search_query',
            type=str,
            default=settings.SEARCH_QUERY,
            help='The search query used for the Youtube API search',
        )

        parser.add_argument(
            '--row_limit',
            type=int,
            default=2,
            help='The maximum number of rows to fetch via the youtube API ' + \
                'in multiples of --batch_size for bulk updating or inserting ' + \
                'to the YoutubeVideo table',
        )

    def handle(self, *args, **options):
        current_datetime = datetime.datetime.now(tz=timezone.utc)
        '''
        Check if the periodicity is maintained and skip if any job is running using a lookup table
        in the database with runtime information of the cronjob
        '''
        datetime_threshold = current_datetime - datetime.timedelta(
            seconds=60)
        last_run = models.CronLog.objects.filter(
                ended_at__gte=datetime_threshold).filter(status='running').exists()
        cronjob_object = models.CronLog(
            name="update_youtubevideo_table_data.py",
            status='running',
            )
        cronjob_object.save()
        try:
            if last_run:
                cronjob_object.status = 'skipped'
                cronjob_object.save()
                return
            cronjob_object.is_running = True
            cronjob_object.save()
            search_query = options['search_query']
            batch_size = options['batch_size']
            row_limit = options['row_limit']
            next_token = None
            '''
            Since Youtube Data API can only provide a maximum of 50 items per request,
            we stack the items to form a batch of size --batch-size and update the database
            '''
            for x in range(row_limit):
                batch_list, next_token = self.get_batch(
                    search_query, next_token=next_token, limit=batch_size)
                if not batch_list:
                    break
                id_to_snippet = {}
                id_to_etag = {}
                for search_result in batch_list:
                    video_id = search_result['id']['videoId']
                    if not video_id:
                        continue
                    id_to_snippet[str(video_id)] = search_result['snippet']
                    id_to_etag[str(video_id)] = search_result['etag']
                '''
                Get the video_ids of pre existing videos and filter out;
                    1. The new videos
                    2. existing but not up to date videos
                    3. The videos which are not changed since the last request(stale)
                '''
                existing_video_ids = models.YoutubeVideo.objects.filter(
                    video_id__in=id_to_etag.keys()).values_list(
                        'video_id', flat=True)
                query = self.insert_new_videos(
                    id_to_etag, id_to_snippet, existing_video_ids)
                self.update_existing_videos(query, id_to_etag, id_to_snippet)
                if not next_token:
                    break
            cronjob_object.status = 'success'
        except Exception as e:
            cronjob_object.status = 'failed'
            cronjob_object.error_log = str(e)

        cronjob_object.is_running = False
        cronjob_object.save()
        self.stdout.write(self.style.SUCCESS(
            f'Cron ended at :{str(datetime.datetime.now(tz=timezone.utc))}'))

    def get_batch(self, search_query, limit, next_token=None):
        '''
        Produces stacked video items of length --limit
        '''
        chunks = []
        counter = 0
        '''
        Here a counter is used as a fallback to the 'break' statements
        '''
        while(counter <= limit/50):
            if (len(chunks) >= limit):
                break
            params = {
                'q': search_query,
                'part': 'id,snippet',
                'maxResults': 50,
                'order': 'date',
                'type': 'video',
            }
            if next_token:
                params['pageToken'] = next_token
            try:
                successing_page_response = self.youtube.search().list(**params).execute()
            except Exception as e:
                if e.resp.status == 403:
                    self.set_youtube_api_handle()
                    continue
                return (None, None)
            if not (successing_page_response['pageInfo']['totalResults'] > 0):
                break
            chunks.extend(successing_page_response['items'])
            next_token = successing_page_response['nextPageToken'] if ('nextPageToken' in successing_page_response) else None
            if not next_token:
                break
            counter = counter + 1

        return (chunks, next_token)

    def set_youtube_api_handle(self):
        '''
        Manage the API keys in queue fashion if the active key's quota is exhausted
        '''
        if len(DEVELOPER_KEY) == 0:
             raise Exception("YouTube Data API keys are exhausted, please update the keys or increase quota")
        ACTIVE_KEY = DEVELOPER_KEY.popleft()
        self.youtube = discovery.build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=ACTIVE_KEY)

    def insert_new_videos(self, id_to_etag, id_to_snippet, existing_video_ids):
        '''
        Does a bulk insert using bulk_create() method of all new videos fetched in the last API request.
        This method return a Q filter query which is used to get the not-upto-date videos
        '''
        new_video_ids = []
        new_youtubevideo_objects = []
        query = Q()
        for video_id, etag in id_to_etag.items():
            if video_id in existing_video_ids:
                query |= Q(video_id=video_id, etag=etag)
                continue
            new_video_ids.append(video_id)
            youtubevideo_object = models.YoutubeVideo(
                video_id=video_id,
                etag=id_to_etag[video_id],
                title=id_to_snippet[video_id]['title'],
                description=id_to_snippet[video_id]['description'],
                thumbnails=id_to_snippet[video_id]['thumbnails'],
                published_at=id_to_snippet[video_id]['publishedAt'],
            )
            new_youtubevideo_objects.append(youtubevideo_object)
        models.YoutubeVideo.objects.bulk_create(
            new_youtubevideo_objects, ignore_conflicts=True)
        return query

    @transaction.atomic()
    def update_existing_videos(self, query, id_to_etag, id_to_snippet):
        outdated_video_objects = models.YoutubeVideo.objects.select_for_update().filter(
            video_id__in=id_to_etag.keys()).exclude(query)
        for video in outdated_video_objects:
            video_id = video.video_id
            video.etag = id_to_etag[video_id]
            video.title = id_to_snippet[video_id]['title']
            video.description = id_to_snippet[video_id]['description']
            video.published_at = id_to_snippet[video_id]['publishedAt']
            video.thumbnails = id_to_snippet[video_id]['thumbnails']
        models.YoutubeVideo.objects.bulk_update(
            outdated_video_objects, ['etag', 'title', 'description', 'published_at', 'thumbnails'])
