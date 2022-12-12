import logging
import uuid
from xmlrpc.client import DateTime
import azure.functions as func
from datetime import datetime , timezone
import time
from threading import Thread
import traceback
import json
from azure.core.exceptions import ResourceExistsError
from azure.common import AzureConflictHttpError
from concurrent.futures import wait
import os
import json
import time
import os
import traceback
import requests
import logging
import azure.functions as func
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter, Retry
from azure.core.exceptions import ResourceExistsError
from azure.common import AzureMissingResourceHttpError, AzureConflictHttpError
from azure.storage.blob import AppendBlobService
from azure.eventhub import EventHubProducerClient
from azure.eventhub import EventData 
from lib.store import ProviderStore
import sys


class EventHubSync:
    def __init__(self):
        self.conn_str = os.environ.get('conn_str',"Endpoint=sb://scale2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=2kcRyt2habYK6SXXvQjPrnw240465QqxdNBy9PtvEa4=")
        self.eventhub_name = os.environ.get('eventhub_name' ,"scaleeh")
      
# write function to write in the blob, write call for each event    
    def eventsend(self,message):
        # conn_str = self.conn_str
        # eventhub_name = self.eventhub_name
        producer= ProviderStore().get_producer()
        e=json.loads(message)
        partitionId=str(e[0]["partition"])

        message+='\n'
        # producer = EventHubProducerClient.from_connection_string(conn_str=conn_str, eventhub_name=eventhub_name)
        self.send_event_data_batch_with_partition_id(producer,partitionId,message)
            
    def send_event_data_batch_with_partition_id(self,producer,id,message):
        
        try:
            event_data_batch_with_partition_id = producer.create_batch(partition_id=id)
            try:
                event_data_batch_with_partition_id.add(EventData(message))
            except ValueError:
                logging.info("valueError")
                    
            producer.send_batch(event_data_batch_with_partition_id)
            
        finally:
            logging.info("pushed data to event")
            
            
    

    




