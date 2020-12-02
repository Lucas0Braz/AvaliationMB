import json

from tests.BaseTest import BaseCase
#todo tests with unittest
class TestFeiraModel(BaseCase):

    def test_successful_get(self):


        payload = json.dumps({
	    "name_feira": "vl-formosa",
	    "latitude": -23.558733,
	    "longitude": -46.550164,
	    "setor_censitario": 355030885000099,
	    "area_ponderada": 3550308005049,
	    "endereco": "just a test",
	    "numero": "333b",
	    "referencia": "nenhuma",
	    "bairro": "Jururu"
        })

        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)