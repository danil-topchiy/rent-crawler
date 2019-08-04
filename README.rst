===============================
rent-crawler
===============================

Small app to crawl rent objects


Quickstart
----------

Run the following commands to bootstrap your environment ::

    git clone https://github.com/danil_topc/rent-crawler
    cd rent_crawler
    pip install -r requirements/dev.txt
    cp .env.example .env
    flask run

Deployment
----------

To deploy::

    export FLASK_ENV=production
    export FLASK_DEBUG=0
    export DATABASE_URL="<YOUR DATABASE URL>"
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
--------------------

To run flask tests, run ::

    pytest tests/


Running crawling
-----------------

To start crawling and saving rent objects to database (currently dom.ria.com kyiv objects only) , run ::

    flask start_crawling


Docker
------

To get MongoDb up in docker run ::

    docker-compose up -d mongo

