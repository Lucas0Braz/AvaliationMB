import requests
import json

"""Testing Routes"""
url = 'http://127.0.0.1:5000/1235-11'
uri = 'http://127.0.0.1:5000/feira-livre/1235-11'
requests.get(url=uri)

data_post = {
	"name_feira": "vl-formosa",
	"latitude": -23.558733,
	"longitude": -46.550164,
	"setor_censitario": 355030885000099,
	"area_ponderada": 3550308005049,
	"endereco": "amazing adress3",
	"numero": "333b",
	"referencia": "nenhuma",
	"bairro": "Jururu"
}

headers = {'Content-type': 'application/json'}
response = requests.post(url=uri, data=json.dumps(data_post), headers=headers)
print(response.json())




