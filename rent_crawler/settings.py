# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = env.str("SECRET_KEY")

# Database
MONGODB_DB = env.str("MONGODB_DB")
MONGODB_HOST = env.str("MONGODB_HOST")
MONGODB_PORT = env.int("MONGODB_PORT")
MONGODB_USERNAME = env.str("MONGODB_USERNAME")
MONGODB_PASSWORD = env.str("MONGODB_PASSWORD")
