# Youtube-Topic-Tracker
Get latest information of youtube videos using Youtube Data API

### Working
  This project works on Django with MySQL as database. The information of latest Youtube videos from a predefined topic/query is periodically added/updated to the database every 60 seconds by a dedicted Cron server.

  ## Start the project

  1. Add the Youtube API keys and Search query in mysite/settings file 

  *# mysite/settings.py*


    SEARCH_QUERY = 'News'
    YOUTUBE_API_KEYS = ['API_KEY_1', 'API_KEY_2'...]


  2. Build the docker images and start the containers(assuming docker is installed on your machine)
  
   *#Go to youtube_api_project/mysite*

    $ docker-compose up


  3. The Django server will be live on http://127.0.0.1:8000

   ## Interaction with the API 
   
   - The GET API to view all video with pagination will be active on;
        (http://127.0.0.1:8000/youtubevideos/)
 
   ## Search query to the API
   
   - To search the database with a particular query, provide query parameters to the API url
        (http://127.0.0.1:8000/youtubevideos?search=**<key word>**
    *Note: Only 'title' and 'description' fields used for searching.*
  
   ## Sorting of API results (ASC/DSC)
   
   *Example;*
    - (http://127.0.0.1:8000/youtubevideos?ordering=-published_at)
   
  
   ## Key Features
  
    - Youtube-Topic-Tracker when given a set of API keys, it can handle the Youtube API error 403 by
      switching the key to the next one available one.
      
    - Write concurrencies on the database are taken care.
 
   
   
   
   
