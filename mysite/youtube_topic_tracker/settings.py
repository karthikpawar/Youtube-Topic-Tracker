from django.conf import settings

YOUTUBE_API_KEYS = getattr(settings, 'YOUTUBE_API_KEYS', [])
BATCH_SIZE = getattr(settings, 'YTT_BULK_BATCH_SIZE', 50)
SEARCH_QUERY = getattr(settings, 'YTT_SEARCH_QUERY', 'how to pawrii')
ROW_LIMIT = getattr(settings, 'YTT_ROW_LIMIT', 50)
