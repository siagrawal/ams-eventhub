import logging
import json
import os
import base64
import hmac
import hashlib
import traceback
import requests
import datetime
import json
import base64
import hmac
import datetime
import hashlib
import time
import os
import sys
import traceback
import logging
import requests

import azure.functions as func
table_1=[]
table_2=[]
table_3=[]
table_4=[]
table_5=[]
table_6=[]
table_7=[]
table_8=[]
table_9=[]
table_10=[]
table_11=[]
table_12=[]
table_13=[]
table_14=[]
table_15=[]


def main(event: func.EventHubEvent):
            global table_1
            global table_2
            global table_3
            global table_4
            global table_5
            global table_6
            global table_7
            global table_8
            global table_9
            global table_10
            global table_11
            global table_12
            global table_13
            global table_14
            global table_15
                #  event.get_body().decode('utf-8'))
            for e in event:
                e= e.get_body()
                
                lists=[]
                lists=json.loads(e)
                table=int(lists[0]["table"])
                if(table==1):
                    table_1+=lists
                elif(table==2):
                    table_2+=lists
                elif(table==3):
                    table_3+=lists
                elif(table==4):
                    table_4+=lists
                elif(table==5):
                    table_5+=lists
                elif(table==6):
                    table_6+=lists
                elif(table==7):
                    table_7+=lists
                elif(table==8):
                    table_8+=lists
                elif(table==9):
                    table_9+=lists
                elif(table==10):
                    table_10+=lists
                elif(table==11):
                    table_11+=lists
                elif(table==12):
                    table_12+=lists
                elif(table==13):
                    table_13+=lists
                elif(table==14):
                    table_14+=lists
                else:
                    table_15+=lists
            laws = AzureLogAnalytics()
            t=datetime.datetime.now()
            logging.info("pushing to laws")
            response = laws.post_data(f'tables_1', json.dumps(table_1))
            if (response==True):
                    table_1=[]
            response = laws.post_data(f'tables_2', json.dumps(table_2))
            if (response==True):
                    table_2=[]
            response = laws.post_data(f'tables_3', json.dumps(table_3))
            if (response==True):
                    table_3=[]
            response = laws.post_data(f'tables_4', json.dumps(table_4))
            if (response==True):
                    table_4=[]
            response = laws.post_data(f'tables_5', json.dumps(table_5))
            if (response==True):
                    table_5=[]
            response = laws.post_data(f'tables_6', json.dumps(table_6))
            if (response==True):
                    table_6=[]
            response = laws.post_data(f'tables_7', json.dumps(table_7))
            if (response==True):
                    table_7=[]
            response = laws.post_data(f'tables_8', json.dumps(table_8))
            if (response==True):
                    table_8=[]
            response = laws.post_data(f'tables_9', json.dumps(table_9))
            if (response==True):
                    table_9=[]
            response = laws.post_data(f'tables_10', json.dumps(table_10))
            if (response==True):
                    table_10=[]
            response = laws.post_data(f'tables_11', json.dumps(table_11))
            if (response==True):
                    table_11=[]
            response = laws.post_data(f'tables_12', json.dumps(table_12))
            if (response==True):
                    table_12=[]
            response = laws.post_data(f'tables_13', json.dumps(table_13))
            if (response==True):
                    table_13=[]
            response = laws.post_data(f'tables_14', json.dumps(table_14))
            if (response==True):
                    table_14=[]
            response = laws.post_data(f'tables_15', json.dumps(table_15))
            if (response==True):
                    table_15=[]
            duration=datetime.datetime.now()-t
            logging.info(f'total time  to push in laws for 10 tables {duration}')
            
            
        
        
            

  

class AzureLogAnalytics:
    """
    This class provides the functionality to log metrics to Log Analytics Workspace (LAWS).
    """
    def __init__(self):
        self.shared_key = os.environ.get('laws_shared_key', "gupxSQ/WgUB1WQc73rJM/86MixzmVN9W5o3HqDRoSeUqTes4/LaTUefjYf3QTrAI65GKezgfnrb00tAYKzYOew==")
        self.workspace_id = os.environ.get('laws_workspace_id', "4512a1e8-514c-4ae6-b070-cfb8494292fb")

    def build_authorization_signature(self, date, content_length,
                                      method, content_type, resource):
        """
        Returns authorization header which will be used when
            sending data into Azure Log Analytics.
        """

        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" \
                                + str(content_length) + "\n" \
                                + content_type + "\n" \
                                + x_headers + "\n" \
                                + resource
        bytes_to_hash = bytes(string_to_hash, 'UTF-8')
        decoded_key = base64.b64decode(self.shared_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash,
                                                 digestmod=hashlib.sha256).digest()).\
            decode('utf-8')
        authorization = f"SharedKey {self.workspace_id}:{encoded_hash}"
        return authorization

    def post_data(self, custom_log, body)->bool:
        """
        method to push json data to LAWS.

        Args:
            custom_log: the log type for LAWS.
            body: json string that needs to be pushed into LAWS.

        Returns:
           requests.Response: Response to Http request to post data to log analytics workspace.
        """

        method = 'POST'
        content_type = 'application/json'
        resource = '/api/logs'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(body)
        signature = self.build_authorization_signature(rfc1123date, content_length, method,
                                                       content_type, resource)

        #TODO(nitinagarwal): the uri will not work for other clouds like national clouds. handle it properly.
        uri = 'https://' + self.workspace_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'
        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': custom_log,
            'x-ms-date': rfc1123date
        }
        try:
            logging.debug("pushing data to log analytics workspace")
            start_time = time.time()
            response=requests.post(uri, data=body, headers=headers, timeout=5)
            if not (response.status_code >= 200 and response.status_code <= 299):
                        logging.error(
                            f"unable to Write: code {response.status} message {response.text}")
                        raise Exception("got exception from LAWS")
            else:
                        logging.debug("total time taken to push data to log analytics "+\
                            f"workspace: {time.time()-start_time}")

        except Exception as exception:
            logging.error(traceback.format_exc())
            raise

        return True
