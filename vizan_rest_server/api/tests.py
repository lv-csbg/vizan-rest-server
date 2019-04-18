from django.test import TestCase
from django.urls import reverse
import base64
import json
import os


# Create your tests here.
class JSONRequestViewTests(TestCase):
    def tearDown(self):
        os.remove("prod_subst_0.svg")

    @staticmethod
    def create_example_json_data_file(model_filename, svg_filename):
        with open(model_filename, "rb") as f:
            model = f.read()
        with open(svg_filename, "rb") as f:
            svg = f.read()
        svg_encoded = base64.b64encode(svg)
        res = {
            'model': model.decode("utf-8"),
            'svg': svg_encoded.decode("utf-8"),
            'analysis_type': 'FBA'
        }
        return res

    @staticmethod
    def parse_json_response_content(content):
        res = json.loads(content.decode('utf-8'))
        decoded_res = base64.b64decode(res["result"].encode("utf-8"))
        return decoded_res

    def test_submit_json_data(self):
        data = self.create_example_json_data_file(
            model_filename='api/test_data/iML1515.json', svg_filename='api/test_data/E_coli_source.svg')
        response = self.client.post(reverse('api:json_request'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, 'application/json')
        decoded_content = self.parse_json_response_content(response.content)
        self.assertEqual(decoded_content[:8], b'<svg:svg')
