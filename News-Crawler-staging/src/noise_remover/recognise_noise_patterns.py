import unidecode, json, re
import pandas as pd
from collections import Counter
from datetime import datetime, timedelta
from utilities.common import timeit, common
from src.news_extraction.news_extraction import NewsExtraction

blacklist_items = ['html_parser','request','dom_tree']
THRESHOLD = 50

class NoiseRemoval(NewsExtraction,common):
    @timeit
    def __init__(self,**kwargs):
        """In the fuction encode the full text and removing the noise call a other fuction
        """
        if ('article_body' in kwargs.keys()):
            self.article_body = kwargs['article_body']
            self.publisher_name = kwargs['publisher_name']
            self.remove_encoding_errors()
            self.remove_noise_from_content()

    def remove_encoding_errors(self):
        """Using unidecode translate a language
        """
        try:
            self.article_body = unidecode.unidecode(self.article_body)
        except UnicodeDecodeError:
            # self.logger.exception("")
            pass
        else:
            pass
    @timeit
    def get_content(self):
        return self.article_body
    def remove_punctuations(self,value):
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punc = ""
        for char in value:
            if char not in punctuations:
                no_punc = no_punc + char
        return no_punc
        
    def remove_noise_from_content(self):
        """make it static rather than reading per each publisher & each article
        """
        try:
            noise_list = self.get_connection("noise_config").find({ "publisher_name": self.publisher_name})[0]['noise_pattern']
            if noise_list!=[]:
                for noise in noise_list:
                    self.article_body = re.sub(noise, '', self.article_body, flags = re.IGNORECASE)
        except IndexError: #IndexError:
            # self.logger.exception(traceback.format_exc())
            # print("IndexError")
            pass
        except Exception as e: #IndexError:
            pass
            # traceback.print_exc()
            # print("No Noise pattern for publisher identitfied")
            # #print(e)
    @timeit
    def identitfy_noise_pattern(self):
        """Identity the noise pattern and join the data
        """
        publishers_list = self.get_publishers_list()
        # analysis_df = pd.DataFrame()
        for publisher_name in publishers_list:
            analysis_df = pd.DataFrame()
            query = { "publisher_name": publisher_name ,'date': {'$lt':datetime.now(), '$gte': (datetime.now()-timedelta(hours=+24)) }}
            df = pd.DataFrame.from_records(self.get_connection("latest_links").find(query,{'url': 1}))
            # ("{} number of articles for last 24 hrss for publisher = {} ".format(df.shape[0],publisher_name))
            if df.shape[0] == 0:
                continue
            urls = df['url'].values
            list_NewsExtraction = []
            number_of_articles = len(urls)
            for url in urls:
                try:
                    newsExtraction = NewsExtraction(url)
                    list_NewsExtraction.append(newsExtraction)
                except:
                    pass
            tuple_list = []
            for newsitem in list_NewsExtraction:
                tuple_list.append(newsitem.dom_tree)
            common = common()
            tuple_list = common.flatten(tuple_list)
            with open('config/'+'Article_Body'+'.json') as json_file:
                entity_config = json.load(json_file)
        #     get the config for the publisher
            entity_config_publisher_pattern = entity_config[publisher_name]
            compiled_regex = re.compile(entity_config_publisher_pattern)
            data_list = []
            for index,item in enumerate(tuple_list):
                matches = compiled_regex.finditer(item[0])
                for mat in matches:
                    data_list.append(item[1])
            for item in Counter(data_list).most_common(30):
                if item[1]>2:
                    temp_df = pd.DataFrame([publisher_name,item[0].lower().strip(),item[1]]).T
                    if not "" == self.remove_punctuations(temp_df.iloc[0][1]):
                        # check whether the strip lower key is present if there in the pattern column of analysis dataframe
                        if analysis_df.shape[0]>0:
                            if (analysis_df[analysis_df[1] == temp_df.iloc[0][1]].shape[0] == 1):
                            # if present get the value and add the current item count to the existing value
                            # getting the current value 
                                current_value = analysis_df[analysis_df[1] == temp_df.iloc[0][1].lower().strip()][2]
                                analysis_df.loc[analysis_df[analysis_df[1] == temp_df.iloc[0][1]].index,2] = current_value+item[1]
                            else:
                                analysis_df = analysis_df.append(temp_df)
                        else:
                            analysis_df = analysis_df.append(temp_df)
            analysis_df.rename(columns = {0:"Publisher_name",1:"Pattern",2:"Count"},inplace=True)
            analysis_df.to_excel("Analysis/"+str(publisher_name)+"_Noise_Analysis.xlsx",index=False)
