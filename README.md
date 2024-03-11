# Table of Contents
- [Table of Contents](#table-of-contents)
- [FMsGen: Random generation of feature models](#fmsgen-random-generation-of-feature-models)
  - [Available online](#available-online)
  - [Artifact description](#artifact-description)
  - [How to use it](#how-to-use-it)
  - [Deployment of the web application](#deployment-of-the-web-application)
    - [Requirements](#requirements)
    - [Download and install](#download-and-install)
    - [Execution](#execution)
  - [Video](#video)
  - [References and third-party software](#references-and-third-party-software)

# FMsGen: Random generation of feature models
A tool to generate random feature models.

## Available online
:construction: Soon :construction:


## Artifact description
:construction: Soon :construction:


## How to use it
:construction: Soon :construction:

## Deployment of the web application

### Requirements
- Linux
- [Python 3.10+](https://www.python.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/stable/index.html)
- [Flama](https://flamapy.github.io/)

### Download and install
1. Install [Python 3.10+](https://www.python.org/)
2. Install [Redis](https://redis.io/docs/install/install-redis/)
   
   2a. Check if `redis-server` is running:

    `systemctl status redis-server`

   2b. If `redis-server` is not running, run it:
    
    `redis-server`

3. Clone this repository and enter into the main directory:

    `git clone https://github.com/jmhorcas/fmsGen.git`

    `cd fmsGen`

4. Create a virtual environment and activate it: 
   
   `python -m venv env`

   `. env/bin/activate`

5. Install the dependencies: 
   
   `pip install -r requirements.txt`

   
### Execution
To run the server locally execute the following commands:

1. Go to the app folder: `cd app`
   
2. Run Celery: `celery -A app worker --loglevel INFO`

3. Run the Flask application: `python app.py`

Access to the web service in the localhost:

http://127.0.0.1:5000

## Video
:construction: Soon :construction:


## References and third-party software
- [Flama](https://flamapy.github.io/)