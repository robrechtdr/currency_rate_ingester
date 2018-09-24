# Problem

High level requirements:

- Use the http://fixer.io/ API to ingest currency rates.
- Have the ingest & store procedure run daily at 9:00AM.
- Ingest and store rates for all days *except* weekends.
- Ensure the system holds at least the last month of rates information.

Technical requrements:

- Write code as you normally would write for deployment to a production environment.
- Use Python version 3.6+.
- Provide instructions on how to install and run the application.
- Document (in a text/markdown file) how you could go about deploying & monitoring the application.
- If you ran out of time on any of the high level requirements, write down which you specifically did not yet implement.


# Solution

## Requirements

[Install docker](https://docs.docker.com/install/)   
[Install docker-compose](https://docs.docker.com/compose/install/)

> Tested on docker version 17.03.2-ce and docker-compose version 1.22.0


## Run

### Run server

	sudo docker-compose up -d

> Use `sudo docker-compose stop` to stop the service, using `down` command will reset db.


### Set cron

> Setting this manually to prevent possible surprise of your current local crontab getting messed with. 

	crontab -e

Then write and save:

	0 9 * * 1-5 bash /path/to/python-exercise/ingest.sh

> This triggers `http://0.0.0.0:5000/ingest`. You can run `docker-compose up` command without `-d` to see the cron triggering the endpoint.


## Run tests

	sudo docker-compose run web bash

then run the following in container shell:

	pytest -v


# Further improvements

First of all it would be nice to run the crontab from a separate virtual service in the background so we don't need to tamper with our local crontab. We'd also like if the crontab service somehow gets shut down it auto-restarts so it's as reliable as possible that it gets called.


We could [set up our deployment on AWS Beanstalk](https://docker-curriculum.com/#docker-on-aws) for ease or AMAZON EC2. We'd first want to have our database on a separate server so that our db can't simply be removed by running a docker command. We'd also like to have a staging and production environment; we'd use separate env variable setting files per environment that contain the pw and api_key that we wouldn't add to version control, passing it on confidentially between developers.

We'd also want to keep the endpoint only accessible to the machine itself so externally facing pple can't spam trigger our service. We'd also like to use something like gunicorn as our appserver as Flask's server is not meant for production. 

Another thing we'd want to do is to make sure there is enough disk space available for our database, for this problem case it shouldn't be a problem but if disk space becomes a higher concern we can periodically delete data older than a month ago.

When pushing code for review we'd also want to make sure we have continuous integration and test coverage via e.g. Travis or Codeship so we are sure to see if our new code breaks existing tests and that we'd ideally want to have our new code tested.

For monitoring our application on AWS we could use a service like [AWS Cloudwatch](https://aws.amazon.com/cloudwatch/) or [New Relic](https://newrelic.com/partner/aws-monitoring). 
