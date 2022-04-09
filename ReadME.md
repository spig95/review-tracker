# Review Tracker

A Django project to scrape reviews and show the average evolution over time.

<center>

[<img src="https://img.youtube.com/vi/jhnRtDc4NAc/maxresdefault.jpg" width="600">](https://youtu.be/jhnRtDc4NAc)

_Please click on the video above to see how the website works._

</center>

## 1 Local setup and run


To run the server locally, please follow the following steps

### 1.1 Create the local environment

```
conda env create -f environment.yml
```

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
python manage.py runserver
```

At this point, the website should be up an running on your localhost.

