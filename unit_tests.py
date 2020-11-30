import requests

"""Testing Routes"""
url = 'http://127.0.0.1:5000/'
uri = 'http://127.0.0.1:5000/feira-livre/1234-6'
requests.get(url=uri)

data_post = {'cod_registro':'1234-6'}
requests.post(url=url, data=data_post)

