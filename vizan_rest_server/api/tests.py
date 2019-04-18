from django.test import TestCase
from django.urls import reverse
import base64
import json

test_model_filename = 'api/test_data/iML1515.json'
test_svg_filename = 'api/test_data/E_coli_source.svg'
test_result_svg_0_8 = b'<svg:svg'


# Create your tests here.
class JSONRequestViewTests(TestCase):
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
            model_filename=test_model_filename, svg_filename=test_svg_filename)
        response = self.client.post(reverse('api:json_request'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.accepted_media_type, 'application/json')
        decoded_content = self.parse_json_response_content(response.content)
        self.assertEqual(decoded_content[:8], test_result_svg_0_8)


class FormRequestViewTests(TestCase):
    def test_submit_form_data(self):
        data = {
            'model': open(test_model_filename, 'rb'),
            'svg': open(test_svg_filename, 'rb'),
            'analysis_type': 'FBA',
        }
        response = self.client.post(reverse('api:form_request'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.as_attachment, False)
        self.assertEqual(response.streaming, True)
        content = response.getvalue()
        self.assertEqual(content[:8], test_result_svg_0_8)
