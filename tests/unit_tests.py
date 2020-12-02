import requests
import json

"""Testing Routes"""
uri = 'http://127.0.0.1:5000/'
url = f'{uri}feira-livre/1235-11'


data_post = {
	"name_feira": "vl-formosa",
	"latitude": -23.558733,
	"longitude": -46.550164,
	"setor_censitario": 355030885000099,
	"area_ponderada": 3550308005049,
	"endereco": "just a test",
	"numero": "333b",
	"referencia": "nenhuma",
	"bairro": "Campo Limpo"
}

headers = {'Content-type': 'application/json'}
response = requests.post(url=url, data=json.dumps(data_post), headers=headers)
print(response.status_code)
print('post body:', response.json())


response_get = requests.get(url)
print(response_get.status_code)
print('get body:', response_get.json())

url = f'{uri}feira-livre/1235-111'
data_post = {
	"name_feira": "vl-formosa",
	"latitude": -23.558733,
	"longitude": -46.550164,
	"setor_censitario": 355030885000099,
	"area_ponderada": 3550308005049,
	"endereco": "just a test of put",
	"numero": "333b",
	"referencia": "nenhuma",
	"bairro": "Campo Limpo"
}
response_put = requests.put(url=url, data=json.dumps(data_post), headers=headers)
print(response.status_code)
print('put body:', response.json())


url = f'{uri}feira-livre/1235-111'
response_delete = requests.delete(url)
print(response_delete.status_code)
print('delete body:', response_get.json())


