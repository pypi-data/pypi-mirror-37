import json
from rest_framework.test import APITestCase

class APITestCaseExtend(APITestCase):

    def assertDictEqualWith(self, d1, d2, value_parser=lambda v: v, msg=None):
        self.assertDictEqual(
            d1={k: value_parser(v) for k, v in d1.items()},
            d2={k: value_parser(v) for k, v in d2.items()},
            msg=msg
        )

    def assertDictIntersectEqual(self, d1, d2, value_parser=lambda v: v, msg=None):
        key_set = set(d1.keys()) & set(d2.keys())
        self.assertDictEqual(
            d1={k: value_parser(v) for k, v in d1.items() if k in key_set},
            d2={k: value_parser(v) for k, v in d2.items() if k in key_set},
            msg=msg
        )

    def assertJSONEqual(self, raw, expected_data, msg=None):
        if isinstance(raw, str):
            raw = json.loads(raw)
        self.assertDictEqualWith(raw, expected_data, value_parser=str, msg=msg)

    def assertJSONIntersectEqual(self, j1, j2, msg=None):
        self.assertDictIntersectEqual(j1, j2, value_parser=str, msg=msg)


