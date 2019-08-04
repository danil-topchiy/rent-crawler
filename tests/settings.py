"""Settings module for test app."""
from environs import Env

env = Env()
env.read_env()

ENV = "development"
TESTING = True
SECRET_KEY = "not-so-secret-in-tests"

# Database
MONGODB_DB = env.str("MONGODB_DB") + '-testing'
MONGODB_HOST = env.str("MONGODB_HOST")
MONGODB_PORT = env.int("MONGODB_PORT")
