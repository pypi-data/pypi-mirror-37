from arctic import Arctic
from arctic.date import DateRange
import pandas as pd
import requests


class ArcticRepository:

    def __init__(self, config):
        self.config = config
        self.store = Arctic(config['arctic']['host'])
        self.store.initialize_library(config["arctic"]["collection"])
        self.library = self.store[config["arctic"]["collection"]]


    def checkIfNewVersion(self, symbol, dataFrame, metadata):
        """Check if an update or insert of the DataFrame is required"""
        #Check for symbol in arctic
        try:
            #If symbol already exists read it
            item = self.library.read(symbol)
        except:
            #If symbol does not exist this is a new version exit function and return True
            return True

        #If both time series data and metadata are the same return false
        #if data.equals(item.data) and dict(metadata) == dict(item.metadata):
        if dataFrame.equals(item.data) and metadata == item.metadata:
            return False
        else:
            return True


    def insert(self, id, data, metadata):
        """Upsert the DataFrame into Arctic and Indexer
        accepts id: string
        """
        #dataFrame = data
        if(self.checkIfNewVersion(id, data, metadata)):
            self.library.write(id, data, metadata=metadata)
            metadata['symbol'] = id
            r = requests.put(self.config["elastic"]["url"] + id + '?pretty',
                         json=metadata)
            r.raise_for_status()


    def read(self, name, as_of=None, start_date=None, end_date=None):
        """Read DataFrame from Arctic using the provided ticker"""
        date_range = None
        if start_date != None or end_date != None:
            date_range = DateRange(start_date, end_date)
        return self.library.read(name, as_of, date_range)

    def get_info(self, name):
        """Read DataFrame from Arctic using the provided ticker"""
        return self.library.get_info(name)

    def frequency(self, name):
        """Read DataFrame from Arctic using the provided ticker"""
        return self.library.get_info(name)
