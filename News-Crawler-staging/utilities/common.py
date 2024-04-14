import json
import logging
import signal
import time
from abc import ABC
from contextlib import contextmanager
from datetime import datetime as dt
from functools import wraps
from logging.handlers import RotatingFileHandler

import dateutil.parser as dparser
from pymongo import MongoClient

from src.news_extraction import env
from src.news_extraction.connection_handler import MongoHandler

client = MongoClient(env.COMMON.JIO_MONGO_CONN)

blacklist_items = ['html_parser','request','dom_tree']


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # print(f'Function {str(func.__name__)}  Took {total_time:.3f} s.ms')
        #TODO: add logger later - ani
        return result
    return timeit_wrapper

class common(ABC):
    def __init__(self):
       pass

    def get_connection(self,collection = None):
        db = client['publisher_entity_extract']
        return db[collection]
    def convert_to_datetime(self,x):
        try :
            return dparser.parse(x,fuzzy = True).strftime("%Y/%m/%d %H:%M:%S")
        except :
            return ''
            pass
    def get_publishers_list(self):
        return (self.get_connection('latest_links').distinct("publisher_name"))

    def flatten(self,list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return self.flatten(list_of_lists[0]) + self.flatten(list_of_lists[1:])
        return list_of_lists[:1] + self.flatten(list_of_lists[1:])
    
    def get_data_for_entity(self,data):
        temp_list = []
        for item in data:
            if(len(item[0])>3):
                temp_list.append(item[0])
        return temp_list
    @timeit
    def save_to_db(self, save_to_db = False):
        required_entites = [key for key, value in self.__dict__.items() if key not in blacklist_items]
        final_data = {entity: self.__dict__[entity] for entity in required_entites}
        # pprint.pprint(final_data)
        # print(type(final_data))
        if save_to_db:
            self.get_connection("entities").insert_one(final_data)
            # print("Inserted to Database")
        return(final_data)

    def get_JSON(self, parsed_obj):
        return json.dumps(parsed_obj)

class Timer:
    def __init__(self, roundOff:int=False):
        self.roundOff = roundOff
        self.start_time = 0
        self.end_time = 0
        self.total_time = 0
    def start_timer(self):
        self.start_timer=dt.now()
    def calculate_total_time(self):
        self.end_time=dt.now()
        self.total_time = (self.end_time - self.start_timer).seconds + (self.end_time - self.start_timer).microseconds/1_000_000
        if self.roundOff:
            self.total_time = round(self.total_time, self.roundOff)

@timeit
def get_logger(fileName, log_level=logging.DEBUG):
    """Using get_logger to track and store the process and exicutions

    Args:
        file_log (_type_): __file_name__
        log_level (_type_, optional): _description_. Defaults to logging.INFO.
    """
    # create logger
    logger = logging.getLogger(fileName[:fileName.index('.')])
    logger.setLevel(log_level)

    # create handler
    rf_handler= RotatingFileHandler(fileName,"a",40000000,3)
    rf_handler.setLevel(log_level)

    # create formatter
    format = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(thread)d - %(message)s"
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(format, datefmt)
    rf_handler.setFormatter(formatter)
    logger.addHandler(rf_handler)
    return logger
@timeit
def gcp_key():
    path="src/news_extraction/GCP_Key_pub_sub.json"
    mongo_obj = MongoHandler(env.MONGO.CONN_STIRNG, env.GCPKEY.GCP_CREDENTIALS_DATABASE, env.GCPKEY.GCP_CREDENTIALS_COLLECTION)
    my_col = mongo_obj.get_col_obj()
    gcp_data=my_col.find_one()
    gcp_data.pop("_id",None)
    with open(path, "w") as outfile:
     json.dump(gcp_data,outfile,indent=4) 
    mongo_obj.close_conn()


class TimeoutException(Exception): pass

@contextmanager
def set_timeout(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)