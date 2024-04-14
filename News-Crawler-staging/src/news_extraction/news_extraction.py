import sys, json, re, urllib
sys.path.append("./../../")
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
from utilities.common import common
from src.news_extraction import env
from config.html_parser import html_parser_dict

class NewsExtraction(common):
    def __init__(self,url,**kwargs):
        """Initializing  a variable and fuctions
        Args:
            url (string): Article
        """
        self.url = url
        super().__init__()        
        self.soup_initialization()
        self.publisher_name = self.get_publisher_name(url)
        # print(self.publisher_name)
        if "save_dom_Tree" in kwargs.keys():
            self.get_DOM_tree_V2(save_dom_Tree = kwargs['save_dom_Tree'])
        else:
            self.get_DOM_tree_V2()
        if self.publisher_name is not None:
            self.get_url_data()
    
    def soup_initialization(self):
        """Request to the url"""
        self.request = urllib.request.urlopen(Request(self.url, headers = env.REQUESTS.HEADER))
 
    def get_publisher_name(self, url):
        """ Split the url and find the publisher name in the html_parser_dict 

        Args:
            url (string): Article

        Returns:
            string: publisher name
        """
        return html_parser_dict['publisher_mapping'].get(self.request.geturl().split("//")[1].split('/')[0], None)

    def get_DOM_tree_V2(self,save_dom_Tree = True):
        """Saving the data into dom_tree.txt and read the data in lxml formate

        Args:
            save_dom_Tree (bool):Save the data
        """
        soup = BeautifulSoup(self.request.read(),"lxml")

        data_nodes_list = []
        for descendants in (soup.descendants):
            cache_list = []
        #         cache_list.append(descendants)
        #     if (type(i.name)==type(None)):
            if not('children' in dir(descendants)):
                cache_list.append(descendants)
                if(''.join(descendants).strip() !=''):
                    for parents in descendants.findParents():
                        if not('document' in parents.name):
                            if('class' in parents.attrs.keys()):
                                if(parents.attrs['class']):
                                    cache_list.append(parents.name + "_" + " ".join(parents.attrs['class']))
                            elif not parents.name == 'a':
                                cache_list.append(parents.name)
                data_nodes_list.append(cache_list[::-1])
            else:
                if('img' in descendants.name):
                    if('data-lazy-src' in descendants.attrs.keys()):
                        if(descendants['data-lazy-src'].startswith('http')):
                            cache_list.append(descendants['data-lazy-src'])
                            for parents in descendants.parents:
                                if('class' in parents.attrs.keys()):
                                    if(parents.attrs['class']):
                                        cache_list.append(parents.name + "_" + " ".join(parents.attrs['class']))
                                else:
                                    cache_list.append(parents.name)
                    if('data-src' in descendants.attrs.keys() and len(cache_list) == 0):
                        if(descendants['data-src'].startswith('http')):
                            cache_list.append(descendants['data-src'])
                            for parents in descendants.parents:
                                if('class' in parents.attrs.keys()):
                                    if(parents.attrs['class']):
                                        cache_list.append(parents.name + "_" + " ".join(parents.attrs['class']))
                                else:
                                    cache_list.append(parents.name)
                    if('src' in descendants.attrs.keys() and len(cache_list) == 0):
                        if(descendants['src'].startswith('http')):
                            cache_list.append(descendants['src'])
                            for parents in descendants.parents:
                                if('class' in parents.attrs.keys()):
                                    if(parents.attrs['class']):
                                        cache_list.append(parents.name + "_" + " ".join(parents.attrs['class']))
                                else:
                                    cache_list.append(parents.name)
                if('figcaption' in descendants.name):
                    cache_list.append(descendants.text)
                    for parents in descendants.parents:
                        if('class' in parents.attrs.keys()):
                            if(parents.attrs['class']):
                                cache_list.append(parents.name + "_" + " ".join(parents.attrs['class']))
                        else:
                            cache_list.append(parents.name)
                if(descendants.name):
                    if(descendants.name == 'a'):
                        if 'href' in descendants.attrs.keys():
                            cache_list.append(descendants['href'])
                            cache_list.append('a')
                            for parents in descendants.parents:
                                if('class' in parents.attrs.keys()):
                                    if(parents.attrs['class']):
                                        cache_list.append(parents.name + "_" + " ".join(parents.attrs['class']))
                                else:
                                        cache_list.append(parents.name)
                        elif descendants.text !='':
                            cache_list.append(descendants.text)
                            for parents in descendants.parents:
                                if('class' in parents.attrs.keys()):
                                    if(parents.attrs['class']):
                                        cache_list.append(parents.name + "_" + " ".join(parents.attrs['class']))
                                else:
                                        cache_list.append(parents.name)
                if(cache_list):
                    cache_list = cache_list[:-1]
                    data_nodes_list.append(cache_list[::-1])
                    
        # once the data_nodes list is formed next is to form the relationship
        tuple_list = []
        for item in data_nodes_list:
            if("->".join(item[:-1])):
                tuple_list.append((("->".join(item[:-1])),item[-1]))
        # return tuple_list
        self.dom_tree = tuple_list
        if save_dom_Tree:
            f = open(env.COMMON.DATA_DIR_PATH+'dom_tree.txt', 'w')
            for t in tuple_list:
                line = ':'.join(str(x) for x in t)
                f.write(line + '\n')
            f.close()
    def get_url_data(self,save_to_db=False):
        """Getting the extract data using regex

        Args:
            save_to_db (bool):
        """
        url_data = dict()
        entities = html_parser_dict['publisher_entites'].get(self.publisher_name)
        if not entities:
            raise Exception(f"Regex Not Added for {self.url.split('//')[1].split('/')[0]}")
        # url_data['url'] = url
        # url_data['publisher_name'] = publisher
        keywords_outlink_indices = []
        for entity in entities:
        #     open the config file for the entity
            with open(env.COMMON.CONFIG_DIR_PATH+entity+'.json') as json_file:
                entity_config = json.load(json_file)
        #     get the config for the publisher
            entity_config_publisher_pattern = entity_config[self.publisher_name]
            compiled_regex = re.compile(entity_config_publisher_pattern)
            data_list = []
            for index,item in enumerate(self.dom_tree):
                matches = compiled_regex.finditer(item[0])
                #print(item[0])
                for mat in matches:
                    data_list.append(item[1])
                    #print(item[1])
                    if entity == 'Outlinks':
                        #TODO why storing indices
                        keywords_outlink_indices.append(index+1)
            if(entity == 'Article_Body'):
                setattr(self,entity.lower()," ".join(self.flatten(data_list)))
                # url_data[entity.lower()] = unidecode.unidecode(" ".join(self.flatten(data_list)))
            elif(entity == 'Date'):
                self.identify_published_updated_datetime(url_data,data_list)
    #             url_data[entity.lower()] = ",".join(flatten(data_list))
            elif(entity == 'Publisher_Tags' and data_list):
                data_list = [data for data in data_list if not  "Tag" in data]
                setattr(self,entity.lower(),(data_list))
                # url_data[entity.lower()] = ",".join(self.flatten(data_list))
            elif(entity == 'Author'and data_list):
                data_list = [data for data in data_list if not  "By" in data]
                setattr(self,entity.lower(),",".join(self.flatten(data_list)))
                # url_data[entity.lower()] = ",".join(self.flatten(data_list))
            elif(entity == 'Outlinks' and data_list):
                pass
                # url_data[entity.lower()] = ",".join(self.flatten(data_list))
                setattr(self, entity.lower(), (data_list))
                self.Keywords_Outlink = [self.dom_tree[keywords_outlinks][1] for keywords_outlinks in keywords_outlink_indices]
                # url_data['Keywords_Outlink'] = [tuple_list[keywords_outlinks][1] for keywords_outlinks in keywords_outlink_indices]
            elif(data_list):
                setattr(self,entity.lower(),",".join(self.flatten(data_list)))
                # self[entity.lower()] = ",".join(self.flatten(data_list))
                # url_data[entity.lower()] = ",".join(self.flatten(data_list))

        #TODO why this return requied ?
        return(url_data,keywords_outlink_indices)

    
    def identify_published_updated_datetime(self,url_data,data_list):
        """Checking the data is updated or published

        Args:
            url_data (string): Article
            data_list (string):Extracted data
        """
        for data in data_list:
            if "updated" in data.lower() and self.convert_to_datetime(data) != '':
                pass
                self.date_updated = self.convert_to_datetime(data)
                # url_data["date_updated"] = self.convert_to_datetime(data)
            elif "published" in data.lower() and self.convert_to_datetime(data) != '':
                self.date_published = self.convert_to_datetime(data)
                # url_data["date_published"] = self.convert_to_datetime(data)
            elif self.convert_to_datetime(data)!= '':
                self.date_published = self.convert_to_datetime(data)
                # url_data["date_published"] = self.convert_to_datetime(data)