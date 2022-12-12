import os
from datetime import datetime
from typing import Dict
from threading import Lock
utils_lock = Lock()
def get_provider_version():
    return os.environ.get('provider_version', '8.1')

def get_provider_type():
    return "foobar"

def get_default_log_analytics_data(table: int,partition: int, provider_instance_name: str,
                                   provider_instance_metadata: str) -> Dict:
    """Build a log item from provider instance to be pushed into laws

    Args:
        provider_instance_name (str): name of provider instance
        provider_instance_metadata (str): metadata corresponding to provider instance

    Returns:
        Dict: default_log_analytics_data to be pushed into laws
    """
    default_log_analytics_data = {
        "table": table,
        "partition": partition,
        "SAPMON_VERSION": get_provider_version(),
        "PROVIDER_INSTANCE": provider_instance_name,
        "METADATA": provider_instance_metadata,
        "Time_Generated": datetime.utcnow().isoformat()
    }
    return default_log_analytics_data


class Singleton(type):
    """ Create a new instance of the Singleton class.

    This is used as a meta class for EventhubConnection.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with utils_lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        Singleton, cls).__call__(
                        *args, **kwargs)
        return cls._instances[cls]

