import requests, traceback
from src.news_extraction.env import TRANSLATOR,LANGUAGECODES

def ms_translator(logger,
                str_list:list,
                lang_from:str,
                lang_to:str='english'
                ) -> list:
    """Translte the string

    Args:
        str_list (list): passing the string to translate by the API
        lang_from (str): From language 
        lang_to (str): To language
        logger (Object): Logger

    Returns:
        list: translted list
    """
    try:
        params = {
            'api-version': '3.0',
            'from': LANGUAGECODES.lang[lang_from.lower()]["l2"],
            'to': LANGUAGECODES.lang[lang_to.lower()]["l2"]
        }

        translate_list =[]
        for string in str_list:
            try:
                if string:
                    body = [{'text':str(string)}]
                    response = requests.post(TRANSLATOR.endpoint, params=params, headers=TRANSLATOR.headers, json=body).json()
                    translate_list.append(response[0]["translations"][0]["text"])
                else:
                    translate_list.append("")
            except:
                translate_list.append("")
                logger.info(lang_from)
                logger.info(f'Data : "{str(string)}"')
                logger.info(f"API Response: {response}")
                logger.error(traceback.format_exc())
    except:
        logger.error(traceback.format_exc())
    finally:
        return translate_list if len(translate_list) == len(str_list) else False
