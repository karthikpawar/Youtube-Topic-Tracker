# Youtube-Topic-Tracker
Get latest information of youtube videos using Youtube Data API

### Working
  This project works on Django with MySQL as database. The information of latest Youtube videos from a predefined topic/query is periodically added/updated to the database every 60 seconds by a CronJob.

  ## Start the project

  1. Add the Youtube API keys and a search query in mysite/settings file 

  *# mysite/settings.py*


    SEARCH_QUERY = 'News'
    YOUTUBE_API_KEYS = ['API_KEY_1', 'API_KEY_2'...]


  2. Build the docker images and start the containers(assuming docker is installed on your machine)
  
   *# Go to mysite/*

    $ docker-compose up


  3. The Django server will be live on http://127.0.0.1:8000

   ## Interaction with the API 
   
   - The GET API to view all video with pagination will be active on;
        (http://127.0.0.1:8000/youtubevideos/)
 
   ## Search query to the API
   
   -  To search the database with a particular query, provide query parameters to the API url:
       
       (http://127.0.0.1:8000/youtubevideos?search=__keyword__)
   
    Note: Only 'title' and 'description' fields used for searching.*
  
   ## Sorting of API results (ASC/DSC)
   
   *Example;*
    - (http://127.0.0.1:8000/youtubevideos?ordering=-published_at)
     
    Note: sorting is available only for field 'published_at'
   
  
   ## Key Features
  
    - Youtube-Topic-Tracker when given a set of API keys, it can handle the Youtube API error 403 by
      switching the key to the next available one.
      
    - Write concurrencies on the database are taken care.
 
   
 ## CronJob
  - A Django management command is used as a CronJob here: 
       update_youtubevideo_table_data.py
  - The arguments accepted by the management command are:
       1. **--batch_size** : The batch size value used for bulk updating or inserting to the database table(default values: 50)
       2. **--search_query** : The search query used for the Youtube API search(default value: 'pawrii')
       3. **--row_limit** : The maximum number of rows to fetch via the youtube API(default value: '50)

   
