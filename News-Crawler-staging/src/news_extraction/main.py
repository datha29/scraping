from datetime import datetime as dt
import os, sys, json, re, traceback
from concurrent.futures import TimeoutError
from typing import Dict, Any
from google.cloud import pubsub_v1
from bson import json_util
from google.cloud import pubsub_v1
sys.path.append("../../../")
from src.news_extraction import env
from src.news_extraction.scraper import Scraper
from src.news_extraction.article_process import EntityData, Insertion
from src.news_extraction.log_handler import LogHandler
from utilities.common import timeit, Timer, gcp_key
from flask import Flask, jsonify, request
import requests, time,re

EXTERNAL_API_URL ="https://jionews-llama-opesource.pie.news/generate"
MAX_QUERY_LENGTH = 4000
sys.path.insert(0, os.path.abspath('../..'))

# try:
#      nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

def articles_publisher(doc):
    """Publishes a message to a Pub/Sub topic."""
    try:
        parsed_entity_json_encoded = json_util.dumps(doc).encode('utf-8')
        client = pubsub_v1.PublisherClient()
        topic_path = client.topic_path(project_id, env.PUBSUB.PUBLISHING_ID)
        api_future = client.publish(topic_path, parsed_entity_json_encoded)
        message_id = api_future.result()
        logger.info(f"data is pushed to the topic successfully")
        #print(f"Published to {topic_path}: {message_id}")
    except Exception as e:
        logger.error(traceback.format_exc())

def clean_text(text):
  """
  Cleans text by removing URLs, mentions, extra spaces, miscellaneous characters, and double quotes.

  Args:
      text (str): The text to be cleaned.

  Returns:
      tuple: A tuple containing the cleaned text and its length.
  """

  text = re.sub(r"http\S+", "", text)  # Remove URLs
  text = re.sub(r"@[^\s]+", "", text)  # Remove mentions
  text = re.sub(r"\s+", " ", text)    # Replace multiple spaces with a single space
  text = re.sub(r"\^[^ ]+", "", text)  # Remove miscellaneous characters
  text = re.sub(r'"', "", text)        # Remove double quotes

  cleaned_text_length = len(text)

  return cleaned_text, cleaned_text_length




def summarize(text):
    """Summarizes the provided text."""

    # Define the prompt for summarization
    prompt = "Summarize the following text:"

    # Append the prompt to the input text
    text_with_prompt = f"{prompt}\n{text}"

    # Check for empty text
    if not text_with_prompt:
        return {"error": "Please provide text for summarization"}

    # Count non-whitespace characters (assuming limit applies to input text)
    non_whitespace_count = sum(1 for char in text_with_prompt if not char.isspace())

    # Check for text exceeding the limit
    if non_whitespace_count > MAX_QUERY_LENGTH:
        return {"error": f"Text length exceeds the maximum of {MAX_QUERY_LENGTH} characters (excluding whitespace)"}

    # Prepare payload with the text to be summarized
    payload = {"query": text_with_prompt}

    # Send the request to the external summarization API (assuming handle_external_api_error exists)
    response = requests.post(EXTERNAL_API_URL, json=payload)
    error = handle_external_api_error(response)
    if error:
        return error

    # Extract the summarized text from the response
    try:
        summary_text = response.json().get('generated_text')
        if summary_text:
            # Remove potential ending tag (assuming </s> is used) and leading/trailing whitespace
            summary_text = summary_text.replace('</s>', '').strip()
        else:
            summary_text = "Summary unavailable"
    except:
        summary_text = "Summary unavailable"

    # Return the generated summary
    return {"summary": summary_text}



def crawler_v2(pubsub_response: Dict[Any, Any]):
    """The flow of this function is 
          - fetch the articleIds from PubSub
          - Check if these articleIds exist in MongoDB or not.
          - Only those articleIds which are not present in MongoDB will be processed
          - Hit the url and crawl the content from the website, then process the data.
          - If the Publisher Name and the associated regex is available then after processing the article will be pushed to MongoDB and Plsql

    Args:
        response_pubsub (Dict[Any,Any]): Data to be processed.
    """
    # Define variables
    process_total_time, total_time = [0] * 2
    scrap_time = Timer(roundOff=True)
    ingest_time = Timer(roundOff=True)
    tb_msg = None
    url = pubsub_response.get("url")
    if url:
        pubsub_response['url'] = ''.join(re.split(r'\s+', url))
    parsed_entities_json = {"url": url}
    scrap_time.start_timer()
    if url:
        pubsub_response['url'] = ''.join(re.split(r'\s+', pubsub_response["url"]))
        article_scraper = Scraper(pubsub_response, logger)
        parsed_entities_json, crawled_by = article_scraper.main()
        if 'article_body' in parsed_entities_json:
            parsed_entities_json['article_body'] = clean_text(parsed_entities_json['article_body'])

    if 'article_body' in parsed_entities_json:
      cleaned_text, cleaned_text_length = clean_text(parsed_entities_json['article_body'])
      if cleaned_text_length > 4000:
        # Call the imported summary function
        summary = summary(cleaned_text)
        parsed_entities_json['article_body_original'] = cleaned_text
        parsed_entities_json['article_body_summary'] = summary
      else:
        parsed_entities_json['article_body'] = cleaned_text
    else:
        crawled_by = None
    scrap_time.calculate_total_time()
    # Mapped a required field
    parsed_entities_json = EntityData(parsed_entities_json, logger, pubsub_response, crawled_by).main()
    process_total_time = (scrap_time.total_time)
    ingest_time.start_timer()
    # Insert into MongoDB and publish to Pub/Sub
    Insertion(parsed_entities_json.copy(), logger)
    # articles_publisher(parsed_entities_json)
    ingest_time.calculate_total_time()
    total_time = process_total_time + ingest_time.total_time
    logger.info(url, log_in="validated_article")
    
except:
    # Exception handling
        logger.info(f"Article URL : {url}", log_in="failed_article")
        logger.info(f'Article Title : "{pubsub_response["title"]}"', log_in="failed_article")
        logger.info(f'Article ContentId : "{pubsub_response["contentId"]["$oid"]}"', log_in="failed_article")
        logger.info(f'Article ContentType : "{pubsub_response["contentType"]}"', log_in="failed_article")
        tb_msg = traceback.format_exc()
        # logger.info(f'"{translated_list_str}"', log_in="failed_article")
        logger.error(f"Exception : {tb_msg}")
    finally:
        logger.info(f"Crawled by {crawled_by}")
        logger.info(f"Article URL : {url}")
        logger.info(f"Scrap time Time : {scrap_time.total_time} sec")
        logger.info(f"Process Time : {process_total_time} sec")
        logger.info(f"Ingestion Time : {ingest_time.total_time} sec")
        logger.info(f"Crawled Total Time By {crawled_by} : {total_time} sec")
        logger.error(f"Exception : {tb_msg}")


if __name__ == '__main__':
    # initialize loggers
    logger = LogHandler()
    # define variables
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
            response_pubsub = message.data.decode('utf-8')
            response_pubsub = json_util.loads(response_pubsub)
            article_count = article_count + 1
            message.ack()
            crawler_v2(response_pubsub)
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

