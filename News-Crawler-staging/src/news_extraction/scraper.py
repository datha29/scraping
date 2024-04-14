import os 
import json 
import traceback
import requests
import time
from lxml import html
from newspaper import Article, Config
from config.html_parser import html_parser_dict
from config.xpath_parser import xpath_parser_dict
from src.news_extraction.news_extraction import NewsExtraction
from src.news_extraction.env import JIOCRAWLER
from utilities.common import TimeoutException,set_timeout
import datetime as DT
from requests_html import HTMLSession

class Scraper:
    def __init__(self, pubsub_response, logger=None) -> None:
        """Initializing the variable

        Args:
            pubsub_response (dict[Any][Any]): Pub/Sub response
            logger (log_handler.LogHandler): This instance can be used to log different scenarios 
        """
        self.pubsub_response = pubsub_response
        self.crawled_by = None
        self.logger = logger
        self.headers = JIOCRAWLER.HEADER

    def is_entity_exists_xpath(self, entity_name, pub_map):
        """Checking the xpath json file is available or not for the particular publisher name.

        Args:
            entity_name (str): List of the entities getting crawled, like Article_Body, Author, Date_published etc.
            pub_map (str): Name of the publisher for the given entity

        Returns:
             1: if publisher name is available
             0: if publisher name is not available
        """
        path = os.path.abspath('')+f"/config/{entity_name}_Xpath.json"
        with open(path) as f:
            js = json.load(f)
        if js.get(pub_map):
            return 1
        return 0

    def get_entity_xpath(self):
        url = self.pubsub_response["url"]
        pub = url.split('//')[1].split('/')[0]
        pub_map = xpath_parser_dict["publisher_mapping"].get(pub)
        pub_entities = xpath_parser_dict["publisher_entites"].get(pub_map)
        return pub, pub_map, pub_entities

    def check_pub_xpath(self):
        """Check if the xpath for a publisher is available or not.

        Returns:
            msg (str): Returns True if a URL can be scraped using Xpath else will return the Error Message.
        """
        pub, pub_map, pub_entities = self.get_entity_xpath()
        if not pub_map:
            msg = f"Publisher Xpath Mapping not available for {pub}!"
        elif not pub_entities:
            msg = f"Publisher Xpath Entities not available for {pub_map}"
        elif (
            len([self.is_entity_exists_xpath(entity, pub_map) for entity in pub_entities]) 
            != sum([self.is_entity_exists_xpath(entity, pub_map) for entity in pub_entities])
        ):
            msg = f"Regex Not Available for some Entities of {pub_map} Publisher!"
        else:
            msg = True
        return msg

    def scraper_xpath(self):
        """Scraping the articles using the xpath expressions

        Raises:
            Exception: If the xpath is not available for the particular article.
            Exception: If the articles_body have empty string and not the scrapped data.

        Returns:
            dict[Any,Any]: Returns the scraped aticles data.
        """
        session = requests.Session()
        if self.logger: self.logger.info("Trying to scrap the article using xpath........")
        url = self.pubsub_response["url"]
        parsed_entities = {"url":url}
        page = session.get(url,headers=self.headers,timeout=5)
        tree = html.fromstring(page.content)
        _, pub_map, pub_entities = self.get_entity_xpath()
        for entity in pub_entities:
            path = os.path.abspath('')+f"/config/{entity}_Xpath.json"
            with open(path) as f:
                js = json.load(f)
            xpath = js.get(pub_map)
            parsed_entities[entity.lower()] = ''.join(tree.xpath(xpath))
        if not parsed_entities["article_body"]:
            raise Exception(f"Xpath available but No Article-Body scrapped for {url.split('//')[1].split('/')[0]}!!")
        self.crawled_by = 'xpath'
        if self.logger: self.logger.info("Scrapped by Xpath Successfully.")
        return parsed_entities

    def scraper_xpath1(self):
        """Scraping the articles using the xpath expressions

        Raises:
            Exception: If the xpath is not available for the particular article.
            Exception: If the articles_body have empty string and not the scrapped data.

        Returns:
            dict[Any,Any]: Returns the scraped aticles data.
        """
        session = HTMLSession()
        if self.logger: self.logger.info("Trying to scrap the article using xpath with js........")
        url = self.pubsub_response["url"]
        parsed_entities = {"url":url}
        # page = session.get(url,headers=self.headers,timeout=5)
        page = session.get(url,headers=self.headers,timeout=5)
        # page.html.render() 

        tree = html.fromstring(page.content)
        _, pub_map, pub_entities = self.get_entity_xpath()
        for entity in pub_entities:
            path = os.path.abspath('')+f"/config/{entity}_Xpath.json"
            with open(path) as f:
                js = json.load(f)
            xpath = js.get(pub_map)
            parsed_entities[entity.lower()] = ''.join(tree.xpath(xpath))
        if not parsed_entities["article_body"]:
            raise Exception(f"Xpath available but No Article-Body scrapped for {url.split('//')[1].split('/')[0]}!!")
        self.crawled_by = 'xpath_js'
        if self.logger: self.logger.info("Scrapped by Xpath with js Successfully.")
        return parsed_entities




    def is_entity_exists_regex(self, entity_name, pub_map):
        """Checking the regex json file is available or not for the particular publisher name.

        Args:
            entity_name (str): List of the entities getting crawled, like Article_Body, Author, Date_published etc.
            pub_map (str): Name of the publisher for the given entity

        Returns:
             1: if publisher name is available
             0: if publisher name is not available
        """
        path = os.path.abspath('')+f"/config/{entity_name}.json"
        with open(path) as f:
            js = json.load(f)
        if js.get(pub_map):
            return 1
        return 0

    def check_pub_regex(self):
        """Check if the regex for a publisher is available or not.

        Returns:
            msg (str): Returns True if a URL can be scraped using Regex else will return the Error Message.
        """
        url = self.pubsub_response["url"]
        pub = url.split('//')[1].split('/')[0]
        pub_map = html_parser_dict["publisher_mapping"].get(pub)
        pub_entities = html_parser_dict["publisher_entites"].get(pub_map)
        if not pub_map:
            msg = f"Publisher Regex Mapping not available for {pub}!"
        elif not pub_entities:
            msg = f"Publisher Regex Entities not available for {pub_map}"
        elif (
            len([self.is_entity_exists_regex(entity, pub_map) for entity in pub_entities]) 
            != sum([self.is_entity_exists_regex(entity, pub_map) for entity in pub_entities])
        ):
            msg = f"Regex Not Available for some Entities of {pub_map} Publisher!"
        else:
            msg = True
        return msg
    
    def scraper_regex(self):
        """Scraping the articles using the regex

        Raises:
            Exception: If the regex is not available for the particular article.
            Exception: If the articles_body have empty string and not the scrapped data.

        Returns:
            dict[Any,Any]: Returns the scraped aticles data.
        """
        if self.logger: self.logger.info("Trying to scrap the article using regex........")
        url = self.pubsub_response["url"]
        news_extraction_obj = NewsExtraction(
            url, 
            save_dom_Tree = False
        )
        if not news_extraction_obj.publisher_name:
            raise Exception(f"Regex Not Added for {url.split('//')[1].split('/')[0]}")
        # noise_removal_time.start_timer()
        parsed_entities = news_extraction_obj.save_to_db(False)
        parsed_entities_json = news_extraction_obj.get_JSON(parsed_entities)
        parsed_entities_json = json.loads(parsed_entities_json)
        # noise_removal_time.calculate_total_time()
        if not parsed_entities_json["article_body"]:
            raise Exception(f"Regex available but No Article-Body scrapped for {url.split('//')[1].split('/')[0]}!!")
        self.crawled_by = 'regex'
        if self.logger: self.logger.info("Scrapped by Regex Successfully.")
        return parsed_entities_json

    def scraper_newspaper(self):
        """Scraping the articles using newspaper3k module.

        Returns:
            parsed_entities_json (json): Returns the final output data which is scraped from the url
        """
        if self.logger: self.logger.info("Trying to scrap the article using newspaper........")
        url = self.pubsub_response["url"]
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
        config = Config()
        config.request_timeout = 20
        config.browser_user_agent = user_agent
        article = Article(url ,config=config)
        article.download()
        article.parse()
        # article.nlp()
        parsed_entities_json = {
            "url": article.url,
            "article_body" : article.text,
            "date_published" : article.publish_date,
            "author" : ",".join(article.authors) if ",".join(article.authors) else None
        }
        self.crawled_by = 'newspaper'
        return parsed_entities_json

    def schema_constraint(self, parsed_entities_json,model):
        """This method will assure to have same schema of the final output. 

        Args:
            parsed_entities_json (dict[Any][Any]): Attributes scraped by various methods.

        Returns:
            dict[Any][Any]: Final Output adhering to the defined schema
        """
        return {
            "url": parsed_entities_json.get("url",""),
            "headline": parsed_entities_json.get("headline",""),
            "article_body": parsed_entities_json.get("article_body",""),
            "author": parsed_entities_json.get("author",""),
            "date_published": str(parsed_entities_json.get("date_published","")),
            "createdAt": DT.datetime.now(),
            "timeout": parsed_entities_json.get("timeout",False),
            "model": str(model)
        }

    def main(self):
        """Scrapping the article using the regex from the scraper_regex function.
        If the scraper_regex function is not able to scrap the article, calling the scraper_newspaper function.

        Raises:
            Exception: If the response is not true

        Returns:
             json: Final Output
        """
        parsed_entities_json = {}
        # try scraping using Xpath
        try:
            response = self.check_pub_xpath()
            if response != True:
                raise Exception(response)
            parsed_entities_json = self.scraper_xpath()
        except Exception as e:
            self.crawled_by = None
            if self.logger: self.logger.error(traceback.format_exc())


        try:
            response = self.check_pub_xpath()
            if response != True:
                raise Exception(response)
            parsed_entities_json = self.scraper_xpath1()
        except Exception as e:
            self.crawled_by = None
            if self.logger: self.logger.error(traceback.format_exc())
            # self.logger.error(e)
        
        # try scraping using Regex
        try:
            if self.crawled_by is None:
                response = self.check_pub_regex()
                if response != True:
                    raise Exception(response)
                with set_timeout(12): # seconds
                    parsed_entities_json = self.scraper_regex()
        except Exception as e:
            self.crawled_by = None
            if self.logger: self.logger.error(traceback.format_exc())
            # self.logger.error(e)
        
        # try scraping using Newspaper
        try:
            if self.crawled_by is None:
                with set_timeout(12): # seconds
                    parsed_entities_json = self.scraper_newspaper()
        except TimeoutException:
            self.crawled_by = None
            parsed_entities_json["timeout"]=True
            if self.logger: self.logger.exception(f"TimeOut issue")
        except Exception as e:
            self.crawled_by = None
            if self.logger: self.logger.exception(traceback.format_exc())
            # self.logger.error(e)
        parsed_entities_json = self.schema_constraint(parsed_entities_json,self.crawled_by)
        return [parsed_entities_json, self.crawled_by]

