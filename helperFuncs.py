from pathlib import Path
import os

import os
import re
import unicodedata

def check_exists_file(_file, path2check=''):
    dict_result = {'exists': False, 'pathFound':''}
    """if path2chek is empty, it will search for the file in root project foulder
         """
    str_path = _file
    if len(path2check) > 0:
        path_w10 = Path(str_path)
        exists = os.path.exists(path_w10)
        dict_result['exists'] = exists
        dict_result['pathFound'] = path_w10
        return dict_result
    str_path = fr'{Path().absolute()}\{str_path}'
    print(str_path)
    path_w10 = Path(str_path)
    exists = os.path.exists(path_w10)

    dict_result['exists'] = exists
    dict_result['pathFound'] = path_w10

    return dict_result


def strip_accents(text):
    '''Retorna string limpa, sem acentos e caracteres especiais
    '''
    try:
        text = str(text, 'iso-8859-1')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass

    text = re.sub('[º°]', 'o', text)
    text = re.sub('[ª]', 'a', text)
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("iso-8859-1")
    return str(text)


def strip_no_unicode(text):
    '''Retorna string sem caracteres unicode
    '''
    text = strip_none_empty(text)
    text = str(text).strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    text = text.decode('utf-8')
    text = str(text)
    return text

def strip_none_empty(text):
    if text is None:
        return ""
    else:
        if text:
            text = text.strip()
            return text
    return ""

def clean_data_str(value,**kwargs):
    #todo accept multiple regex patterns by **kwargs
    """
    :param value: must reccieve an str
    :return: a str without accents, double spaces and special caracter
    """
    result = strip_no_unicode(value)
    result = strip_accents(result)
    return result