import traceback,re
from datetime import datetime as dt
from src.news_extraction.translator import ms_translator
from src.news_extraction import env
from src.news_extraction.connection_handler import MongoHandler

class EntityData:
    def __init__(self,parsed_entities_json, logger, pubsub_response, crawled_by) -> None:
        """"Initializing the variable

        Args:
            parsed_entities_json (JSON): Scraped data
            logger (Object): Logging Object
            pubsub_response (JSON): Pub/Sub reponse
            crawled_by (str): variable
        """
        self.parsed_entities_json = parsed_entities_json
        self.logger = logger
        self.pubsub_response = pubsub_response
        self.crawled_by = crawled_by

    def add_req_fields(self):
        """Adding More fields like inserted_date,article_body 

        Args:
            parsed_entities_json (JSON): Full text JSON

        Returns:
            JSON: parsed_entities_json
        """
        req_fields = ['title_english', 'article_body', 'article_body_english', 'author', 'date_published', 'inserted_date', 'model']
        self.parsed_entities_json = {k:self.parsed_entities_json.get(k) for k in req_fields}
        self.parsed_entities_json.update({
            'inserted_date' : dt.now(),
            'model' : self.crawled_by
        })
        # article_object = {
        #     "publisher" : self.pubsub_response["publisher"],
        #     "categories" : self.pubsub_response["categories"],
        #     "publisherPublishedAt" : self.pubsub_response["publisherPublishedAt"],
        #     "language" : self.pubsub_response["language"]
        # }
        # self.parsed_entities_json.update({
        #     "article_object" : article_object, 
        #     "inserted_date" : dt.now(), 
        #     "contentId" : self.pubsub_response['contentId']['$oid'],
        #     "contentType" : self.pubsub_response["contentType"],
        #     "title" : self.pubsub_response["title"],
        #     "image_url" : self.pubsub_response["thumbnailUrl"]["original"],
        #     "publisher_name" : self.pubsub_response["publisher"]["name"],
        #     "model" : self.crawled_by
        # })
        
    def remove(self):
        """Remove the pre-defined noises from the article and its related fields.
        
        Args:
            parsed_entities_json (Dict[Any,Any]): Dict having all the fields need to be cleaned.
        """
        try:
            remove = env.COMMON.NOISE_LIST
            for key, value in self.parsed_entities_json.items():
                for r in remove:
                    if (key == "article_body" or key == "image_description" or  key == "summary") and value is not None:
                        value = value.replace(r,'')
                        clean = re.compile('&.*?;')
                        value = re.sub(clean, " ", value)
                        self.parsed_entities_json[key] = value
                    elif key == "image_url" and value is not None:
                        if value.startswith("https") or value.startswith("http"):
                            value = value.split(",")[0]
                            self.parsed_entities_json[key] = value
                        else:
                            value = value.split(",")[1]
                            self.parsed_entities_json[key] = value  
        except IndexError:
            self.parsed_entities_json.pop("image_url",None)
        except Exception as e:
            self.logger.error(traceback.format_exc())
        
    def articles_translator(self):
        """Translate the articles title
        """
        str_list = [self.parsed_entities_json["title"]]
        if (translated_list_str := ms_translator(self.logger,str_list,self.parsed_entities_json["language"]["sourceNames"][0])) != False:  
            self.parsed_entities_json["fullArticle"]["title_english"] = translated_list_str[0]
        else:
            self.parsed_entities_json["fullArticle"]["title_english"] = None
        if self.parsed_entities_json["language"]["sourceNames"][0].lower() == "english":
                self.parsed_entities_json["fullArticle"]["article_body_english"] = self.parsed_entities_json["fullArticle"]["article_body"]
        else:
            self.parsed_entities_json["fullArticle"]["article_body_english"] = None
        
    def main(self):
        """Added the required filed and manage the schema of the JSON

        Returns:
            JSON: Output data
        """
        try:
            self.add_req_fields()
            self.remove()
            temp, self.parsed_entities_json = self.parsed_entities_json.copy(), self.pubsub_response.copy()
            self.parsed_entities_json["fullArticle"] = temp
            self.articles_translator()
        except:
            self.logger(traceback.format_exc())
        finally:
            return self.parsed_entities_json


class Insertion:
    def __init__(self, parsed_entities_json, logger) -> None:
        """Initializing the variable

        Args:
            parsed_entities_json (JSON): Scrapped data
            logger (Object): Logging Object
        """
        self.parsed_entities_json = parsed_entities_json
        self.logger = logger
        self.insert_into_mongodb()
        
    def insert_into_mongodb(self):
        """Make the connections to mongodb and insert the data into the MongoDB.
        
        Args:
            doc (Dict[Any, Any]): Data to be inserted.
        """
        try:
            mongo_obj = MongoHandler(env.MONGO.CONN_STIRNG, env.MONGO.DATABASE, env.MONGO.COLLECTION)
            my_col = mongo_obj.get_col_obj()
            return my_col.update_one({"url":self.parsed_entities_json.pop("url")},{"$set":self.parsed_entities_json},upsert=True)
        except Exception as e:
            self.logger.error(traceback.format_exc())
        finally :
            mongo_obj.close_conn()
            