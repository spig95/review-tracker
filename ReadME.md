# Review Tracker

A Django project to scrape reviews and show the average evolution over time. See the project at https://reviewtracker.herokuapp.com.

### Watch the following video see how the website works
[<img src="https://img.youtube.com/vi/nw7wc2y8jpY/maxresdefault.jpg" width="600">](https://youtu.be/nw7wc2y8jpY)


## 1 Local setup

The project is deployed on Heroku (https://reviewtracker.herokuapp.com). 

However, if you want to run it locally  please follow the following steps.

### 1.1 Create the local environment

Clone the repository and open a terminal in the project folder, then run the following. This will create an environment
called **rt** with the needed requirements.

```
conda create -n rt python=3.9.12
conda activate rt
pip install -r requirements.txt
```

In the local virtual environment, we also want to set the following environmental variables
```
conda env config vars set SECRET_KEY=<put-anything-we-do-not-use-random-key>
conda env config vars set REDIS_URL=redis://localhost:6379
```

**Note**: deactivate the environment for these changes to be applied.

### 1.2 Install Celery

The project relies on Celery, which needs to be installed.

If you are using a Windows machine: download and install msi files from [here](https://github.com/microsoftarchive/redis/releases).

### 1.3 Start redis server

Open a terminal and run these preliminary commands:
```
redis-cli.exe
shutdown
```

Now, open a **new** terminal and type:
```
redis-server
```

At this point, the redis server should be running.

### 1.4 Start Celery

Open a **new** terminal and start Celery by running:
```
conda activate rt
celery -A review_tracker worker -l info -P gevent
```

**Note**: `-P gevent` is necessary to make it work on Windows.


### 1.5 Start the Django server (finally!)

Open a **new** terminal and execute the following:
```
conda activate rt
python manage.py collectstatic --noinput
python manage.py runserver
```

At this point, the website should be up an running on your localhost.


## 2 Want to contribute?

At the moment, the project is only able to scrape from Tripadvisor. 
If you would like to help me out and add a scraper for another website, 
you need to define a new scraper class and add it in the `ScraperFactory`. 

I explained all the required steps in the docstring of 
`Scraper`(in [scrape_app/scrapers/base.py](https://github.com/spig95/review-tracker/blob/main/scrape_app/scrapers/base.py)).
There, you can find an explanation on how to write a new scraper and how to add it in the factory.

In addition, this project exposes the
`DebugScraper` ([scrape_app/scrapers/debug.py](https://github.com/spig95/review-tracker/blob/main/scrape_app/scrapers/debug.py)),
which offers a complete and minimal example of how one should implement a scraper.

### 2.1 Possible issues/improvements...

 - I am not an expert Django + Celery + Redis, this was an exploratory project. 
   Because of this, one might achieve the same results with a simpler setup or a cleaner code. 
   Any suggestion?
 - We quickly reach the maximum number of clients on the Heroku deployment. 
   In particular, clients stay connected to Redis for a while even after we press stop or after we close the website. 
   Some expert of the setup could have a fix for this, which I did not find.
 - `TripAdvisorScraper` is extremely slow. One could use some multi-threading, or a different tool to scrape.
 - Sometimes TripAdvisor blocks requests. For this, I've specified some headers.
   If the website stops to work, they might need to be updated.
 - When something goes wrong in the back-end, the front-end does not always give meaningful error. 
   This is a foggy task definition, but sometimes I'll need to tackle it.
