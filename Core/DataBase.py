import pymongo as pm
import os

from Core.Logger import Logger


class DataBase:
    class _DataBase:
        def __init__(self):
            self.client = pm.MongoClient(os.getenv("MONGO_URL"))

    _instance = None

    def __init__(self):
        self.logger = Logger()

        if not DataBase._instance:
            DataBase._instance = DataBase._DataBase()
            self.logger.info("DataBase", "Connected to database")
        else:
            self.logger.warn("DataBase", "Already connected to database")

    def __getattr__(self, name):
        return getattr(self._instance, name)