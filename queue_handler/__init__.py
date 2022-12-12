
import logging
import random
from unittest.result import failfast
from urllib import request
import azure.functions as func
from datetime import datetime , timezone
from lib.eventsync import EventHubSync
from lib.store import ProviderStore
import json
import time
import time
import os
from lib.lawsync import AzureLogAnalyticsSync
from utils import get_default_log_analytics_data
import requests
import aiohttp

from typing import List, Dict

def main(msg: func.QueueMessage, context:func.Context) -> None:
    start_time = time.time()
    sleep_time = float(os.environ.get('queue_sleep_time', 10))
    activity_data = json.loads(msg.get_body().decode('utf-8'))
    table = activity_data['table']
    partition=activity_data['partition']
    time_pushed = activity_data['epoch_time']
    data = dict()
    data['msg'] = activity_data
    data['parent_invocation_id'] = activity_data['invocation_id']
    data['start_time_from_queue_push'] = int(time.time()) - time_pushed
    read_blob_failure_count = 0
    eventhub_insertion_failure_count = 0
    ams_code_start = time.time()
    
    read_blob_failure_count = 1
    with open("mock_data.json", 'r') as debug_config:
            blob_data = debug_config.read()
    blob_data = json.loads(blob_data)

    event_start_time = time.time()
    try:
        laws_data = generate_json_string(table,partition,blob_data['cols'], blob_data['results'])
        azure_eventhub_sync=EventHubSync()
        azure_eventhub_sync.eventsend(json.dumps(laws_data))
    except:
        logging.exception("failed to push data to eventhub")
        eventhub_insertion_failure_count = 1

    finally:
        data['eventhub_finish_time'] = time.time() - event_start_time
        data['ams_code_execution_time'] = time.time() - ams_code_start

    sleep_time = max(0, sleep_time - (int(time.time()) - start_time))
    # time.sleep(sleep_time)
    data['ams_code_sleep_time'] = sleep_time
    data['ams_control_start_time_epoch'] = convert_epoch_to_datetime(int(start_time))
    data['finish_time_from_queue_push'] = int(time.time()) - time_pushed
    data['time_used_by_ams'] = time.time() - start_time
    data['ams_control_end_time_epoch'] = convert_epoch_to_datetime(int(time.time()))
    data['provider_version'] = os.environ.get('provider_version', None)
    data['eventhub_insertion_failure_count'] = eventhub_insertion_failure_count
    data['read_blob_failure_count'] = read_blob_failure_count
    logging.info(json.dumps(data))


def convert_epoch_to_datetime(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))

def generate_json_string(table,partition, col_index: Dict, result_rows: List) -> list:
        """convert sql server metrics into json string which can be pushed to laws.

        Args:
            col_index (Dict): column names
            result_rows (List): result rows for the metrics check

        Returns:
            str: jsonstring of the metrics data
        """
        # The correlation_id can be used to group fields from the same metrics
        # call
        log_data = []

        # Iterate through all rows of the last query result
        for row in result_rows:
            log_item = get_default_log_analytics_data(table,partition,"foobar",
                                                    {})
            idx = 0
            while idx < (col_index.__len__()):
                # Unless it's the column mapped to TimeGenerated, remove
                # internal fields
                if (col_index[idx].startswith("_") or col_index[idx] == "DUMMY"):
                    continue
                #
                log_item[col_index[idx]] = row[idx]
                idx=idx+1

            log_data.append(log_item)

        # create the json file, set the default to str (string) to cope with date/time columns

        return log_data
