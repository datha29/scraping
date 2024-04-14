from datetime import datetime as dt
import os, sys, json, re, traceback
from concurrent.futures import TimeoutError
from typing import Dict, Any
from google.cloud import pubsub_v1
from newspaper import Article,Config
sys.path.append("../../../")
from src.news_extraction import env
from utilities.common import timeit, Timer,get_logger,gcp_key
from src.news_extraction.news_extraction import NewsExtraction
from src.news_extraction.connection_handler import MongoHandler
from src.news_extraction.translator import ms_translator
sys.path.insert(0, os.path.abspath('../..'))

# try:
#      nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

@timeit
def is_valid_language(data:Dict[Any,Any]):
    """Checking the Article language code 

    Args:
        data (Dict[Any,Any]): Dictonary

    Returns:
        Boolean: True,False
    """
    if data["language"]["code"] in env.COMMON.VALID_LANGUAGES:
        return True
    return False

def add_fields(
            parsed_entities_json:Dict[Any,Any],
            **kwargs:Dict[Any,Any]
        ):
    """Adding More fields like article_object,inserted_date,contentType,contentId

    Args:
        parsed_entities_json (JSON): Full text JSON

    Returns:
        JSON: parsed_entities_json
    """
    for k,v in kwargs.items():
        parsed_entities_json[k] = v
    return parsed_entities_json

def remove(parsed_entities_json:Dict[Any,Any]):
    """Remove the pre-defined noises from the article and its related fields.
    
    Args:
        parsed_entities_json (Dict[Any,Any]): Dict having all the fields need to be cleaned.
    """
    try:
        remove = env.COMMON.NOISE_LIST
        for key, value in parsed_entities_json.items():
            for r in remove:
                if (key == "article_body" or key == "image_description" or  key == "summary") and value is not None:
                    value = value.replace(r,'')
                    clean = re.compile('&.*?;')
                    value = re.sub(clean, " ", value)
                    parsed_entities_json[key] = value
                elif key == "image_url" and value is not None:
                    if value.startswith("https") or value.startswith("http"):
                        value = value.split(",")[0]
                        parsed_entities_json[key] = value
                    else:
                        value = value.split(",")[1]
                        parsed_entities_json[key] = value  
    except IndexError:
        parsed_entities_json.pop("image_url",None)
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        return parsed_entities_json

@timeit
def insert_into_mongodb(doc:Dict[Any, Any]):
    """Make the connections to mongodb and insert the data into the MongoDB.
    
    Args:
        doc (Dict[Any, Any]): Data to be inserted.
    """
    try:
        mongo_obj = MongoHandler(env.MONGO.CONN_STIRNG, env.MONGO.DATABASE, env.MONGO.COLLECTION)
        my_col = mongo_obj.get_col_obj()
        return my_col.update_one({"contentType":doc.pop("contentType"),"contentId":doc.pop("contentId")},{"$set":doc},upsert=True)
    except Exception as e:
        logger.error(traceback.format_exc())
    finally :
        mongo_obj.close_conn()

@timeit     
def crawler_v2(data:Dict[Any,Any]):
    """The flow of this function is 
          - fetch the articleIds from PubSub
          - Check if these articleIds exist in MongoDB or not.
          - Only those articleIds which are not present in MongoDB will be processed
          - Hit the url and crawl the content from the website, then process the data.
          - If the Publisher Name and the associated regex is available then after processing the article will be pushed to MongoDB and Plsql

    Args:
        data (Dict[Any,Any]): Data to be processed.
    """
    # define variables
    process_total_time, total_time = [0]*2
    fetch_time = Timer(roundOff=True)
    domtree_prep_time = Timer(roundOff=True)
    newspaper = Timer(roundOff=True)
    extract_time = Timer(roundOff=True)
    noise_removal_time = Timer(roundOff=True)
    summarize_time = Timer(roundOff=True)
    ingest_time = Timer(roundOff=True)
    tb_msg = None
    req_fields = ['url', 'article_body', 'date_published', 'author']
    parsed_entities_json = {"url": data["url"]}
    try:
        # try to scrap the article using regex
        logger.info("Trying to Scrap using Regex...")
        crawl = "Regex"
        data['url'] = ''.join(re.split(r'\s+', data['url']))
        url = data["url"]
        news_extraction_obj = NewsExtraction(
            url, 
            save_dom_Tree = False, 
            fetch_time = fetch_time, 
            domtree_prep_time = domtree_prep_time, 
            extract_time = extract_time
        )
        if not news_extraction_obj.publisher_name:
            raise Exception(f"Regex Not Added for {url.split('//')[1].split('/')[0]}")
        noise_removal_time.start_timer()
        parsed_entities = news_extraction_obj.save_to_db(False)
        parsed_entities_json = news_extraction_obj.get_JSON(parsed_entities)
        parsed_entities_json = json.loads(parsed_entities_json)
        noise_removal_time.calculate_total_time()
        if not parsed_entities_json["article_body"]:
            raise Exception(f"Regex available but No Article-Body scrapped for {url.split('//')[1].split('/')[0]}!!")
        logger.info("Scrapped by Regex Successfully.")
    except Exception as e:
        log_failed_article.info(f"Can't scrap {url.split('//')[1].split('/')[0]} using regex.")
        log_failed_article.error(e)
        logger.info("Trying to Scrap using Newspaper...")
        crawl = "Newspaper"
        try:
            newspaper.start_timer()
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
            config = Config()
            config.request_timeout = 20
            config.browser_user_agent = user_agent
            article = Article(url ,config=config)
            article.download()
            article.parse()
            article.nlp()
            parsed_entities_json = {
                "url": article.url,
                "article_body" : article.text,
                "date_published" : article.publish_date,
                "author" : ",".join(article.authors)
            }
            newspaper.calculate_total_time()
        except Exception as e:
            crawl = None
            log_failed_article.info(f"Article URL : {url}")
            log_failed_article.info(f'Article Title : "{data["title"]}"')
            log_failed_article.info(f'Article ContentId : "{data["contentId"]["$oid"]}"')
            log_failed_article.info(f'Article ContentType : "{data["contentType"]}"')
            log_failed_article.info(f'Article language : "{data["language"]["code"]}"')
            log_failed_article.error(traceback.format_exc())
            logger.info(f"Crawled by {crawl}")
            logger.info(f"Article URL : {url}")
            logger.info(f'Article language : "{data["language"]["code"]}"')
            logger.error(f"Exception : {traceback.format_exc()}")

    finally:
        parsed_entities_json = {k:parsed_entities_json.get(k) for k in req_fields}
        try:
            article_object = {
                "publisher" : data["publisher"],
                "categories" : data["categories"],
                "publisherPublishedAt" : data["publisherPublishedAt"],
                "language" : data["language"]
            }
            parsed_entities_json = add_fields(
                parsed_entities_json,
                article_object = article_object, 
                inserted_date = dt.now(), 
                contentId = data['contentId']['$oid'],
                contentType = data["contentType"],
                title = data["title"],
                image_url = data["thumbnailUrl"]["original"],
                publisher_name = data["publisher"]["name"],
                model = crawl
                
            )
            parsed_entities_json = remove(parsed_entities_json)
            # str_list = [parsed_entities_json["article_body"],parsed_entities_json["title"]]
            str_list = [parsed_entities_json["title"]]
            if (translated_list_str := ms_translator(logger,str_list,parsed_entities_json["article_object"]["language"]["sourceNames"][0])) != False:
                # translated_list_str = ms_translator(logger,str_list,parsed_entities_json["article_object"]["language"]["sourceNames"][0])
                # parsed_entities_json["article_body_english"] = translated_list_str[0]
                # parsed_entities_json["title_english"] = translated_list_str[1]
                parsed_entities_json["title_english"] = translated_list_str[0]
            else:
                # parsed_entities_json["article_body_english"] = ""
                parsed_entities_json["title_english"] = ""
            if parsed_entities_json["article_object"]["language"]["sourceNames"][0] == "English":
                 parsed_entities_json["article_body_english"] = parsed_entities_json["article_body"]
            else:
                parsed_entities_json["article_body_english"] = None
            process_total_time = (domtree_prep_time.total_time + extract_time.total_time + noise_removal_time.total_time + summarize_time.total_time)
            # process_total_time = (newspaper.total_time + domtree_prep_time.total_time + extract_time.total_time + noise_removal_time.total_time + summarize_time.total_time)
            ingest_time.start_timer()
            insert_into_mongodb(parsed_entities_json)
            ingest_time.calculate_total_time()
            
            total_time = fetch_time.total_time + process_total_time + ingest_time.total_time + newspaper.total_time
            # total_time = fetch_time.total_time + process_total_time + ingest_time.total_time 
            log_validated_article.info(url)
        except:
            log_failed_article.info(f"Article URL : {url}")
            log_failed_article.info(f'Article Title : "{data["title"]}"')
            log_failed_article.info(f'Article ContentId : "{data["contentId"]["$oid"]}"')
            log_failed_article.info(f'Article ContentType : "{data["contentType"]}"')
            tb_msg = traceback.format_exc()
            logger.info(f'"{translated_list_str}"')
            log_failed_article.error(f"Exception : {tb_msg}")
        finally:
            logger.info(f"Crawled by {crawl}")
            logger.info(f"Article URL : {url}")
            logger.info(f"Fetch Time : {fetch_time.total_time} sec")
            logger.info(f"DomTree Preaparing Time : {domtree_prep_time.total_time} sec")
            logger.info(f"Extract Time : {extract_time.total_time} sec")
            logger.info(f"Noise Removal Time : {noise_removal_time.total_time} sec")
            logger.info(f"Summarization Time : {summarize_time.total_time} sec")
            logger.info(f"Process Time : {process_total_time} sec")
            logger.info(f"Ingestion Time : {ingest_time.total_time} sec")
            logger.info(f"Crawled Total Time By {crawl} : {total_time} sec")
            logger.error(f"Exception : {tb_msg}")

if __name__ == '__main__':
    # start logger
    logger = get_logger("logs/crawler_v2.log")
    logger.info("_________Logging is started_________")
    log_validated_article = get_logger("logs/validated_article.log")
    log_validated_article.info("_________Logging is started_________")
    log_failed_article = get_logger("logs/failed_article.log")
    log_failed_article.info("_________Logging is started_________")
    # define variablesa
    article_count = 0
    gcp_key()
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
        os.path.abspath(''),
        env.GCP.RELATIVE_PATH,
        env.GCP.GCP_KEY_FILENAME
    )
  
    project_id = env.PUBSUB.PROJECT_ID
    subscription_id = env.PUBSUB.SUBSCRIPTION_ID
    timeout = env.PUBSUB.TIMEOUT

    # Publishes multiple messages to a Pub/Sub topic with an error handler.
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    def callback(message):
        try: 
            """Using the Pub-Sub, fetch Article Dictonary.
            Args:
                message (bytes): Article dictionary fetched in Bytes format.
            """
            global article_count
            # decoding bytes
            data = message.data.decode('utf-8')
            data = json.loads(data)
            article_count = article_count + 1
            if (entity_data :=data.get("url",None)) is not None:
                crawler_v2(data)
                message.ack()
        except:
           logger.error(traceback.format_exc())
           
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    logger.info(f"Listening for messages on {subscription_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result(timeout = timeout)
            # streaming_pull_future.result(timeout=None)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()  
            logger.info(f"Total Articles Fetched from PubSub : {article_count}")
        # We are getting double logs in logger file because of below code
        # except Exception as e:
        #     logger.error(str(traceback.format_exc()))
