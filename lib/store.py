"""Module to store objects of classes which require only a
single instance to be created.
"""
from threading import Lock
from utils import Singleton 
import os
from azure.eventhub import EventHubProducerClient


class ProviderStore(metaclass = Singleton):
    """Singleton class to store instances of classes.
    Instead of making classes singleton, a single instance of their
    objects is stored here.
    """
    def __init__(self) -> None:
        self.producer_lock = Lock()
        self.producer_connection = None

    def get_producer(self) -> EventHubProducerClient:
        """Returns an instance of AzureTableStorage
        """
        if self.producer_connection is None:
            with self.producer_lock:
                if self.producer_connection is None:
                    self.conn_str = os.environ.get('conn_str',"Endpoint=sb://scale2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=2kcRyt2habYK6SXXvQjPrnw240465QqxdNBy9PtvEa4=")
                    self.eventhub_name = os.environ.get('eventhub_name' ,"scaleeh")
                    self.producer_connection = EventHubProducerClient.from_connection_string(conn_str=self.conn_str, eventhub_name=self.eventhub_name)
                    
        return self.producer_connection
