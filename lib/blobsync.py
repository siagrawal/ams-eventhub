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
from azure.storage.blob import AppendBlobService
from azure.common import AzureConflictHttpError
from concurrent.futures import wait
import os

class BlobStorageSync:
    def __init__(self):
        self.myaccount = os.environ.get('myaccount','siwanistorage1808')
        self.mykey = os.environ.get('mykey' ,'phNc0KGq1JvxJYEdQ9WvQ1+6nnKJzqPe104Z7VROsGavO7VkleX/f0yYXku4ri60ABagfOgke2Z6+AStvwQ6VA==')
      
# write function to write in the blob, write call for each event    
    def blobwrite(self,table, blob_number,message):
        myaccount = self.myaccount
        mykey = self.mykey
        message+='\n'
        append_blob_service = AppendBlobService(account_name=myaccount, account_key=mykey)
        blob=f'func_{blob_number}_{table}'
        try:
            append_blob_service.create_blob(container_name='scalet', blob_name=blob, timeout=3, if_none_match="*")
        except AzureConflictHttpError as ex:
            logging.info(f'coflict error {ex}')
        except ResourceExistsError as ex:
            logging.info(f'blob already exists {ex}')
        except Exception as exp:
            logging.error(f'Exception_{blob_number}_{table}_{exp}')
        finally:
            append_blob_service.append_blob_from_text('scalet', blob, message)
    

    




