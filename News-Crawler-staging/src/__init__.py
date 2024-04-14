from src.news_extraction import env
from src.news_extraction.connection_handler import MongoHandler

mongo_details = env.STORAGEDETAILS["prod"]
mongo_details_stage = env.STORAGEDETAILS["stage"]
# TODO: refactor later for supporting all env
MONGO_COLL_OBJ = MongoHandler(env.MONGO.CONN_STIRNG, mongo_details["db"], mongo_details["collection"]).get_col_obj()
MONGO_COLL_OBJ_STAGE = MongoHandler(env.MONGO.CONN_STIRNG, mongo_details_stage["db"], mongo_details_stage["collection"]).get_col_obj()

CRAWLER_URL = "http://34.36.231.72/crawl"
