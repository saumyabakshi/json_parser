import unittest
from json_parser.json_parser import Lexer, Parser


class Test_JsonParser(unittest.TestCase):
    
    def parse_json(self, file_path):
        with open(file_path, "r") as f:
            text = f.read()
        lexer = Lexer(text)
        parser = Parser(lexer)
        return parser.parse()

    def test_step1(self):
        try:
            result = self.parse_json("tests/step1/valid.json")
            self.assertEqual(result, {})
        except Exception as e:
            self.fail("Unexpected exception: {}".format(e))

        with self.assertRaises(Exception):
            self.parse_json("tests/step1/invalid.json")

    def test_step2(self):
        try:
            result = self.parse_json("tests/step2/valid.json")
            self.assertEqual(result, {"key": "value"})
        except Exception as e:
            self.fail("Unexpected exception: {}".format(e))

        try:
            result = self.parse_json("tests/step2/valid2.json")
            self.assertEqual(result, {"key": "value", "key2": "value"})
        except Exception as e:
            self.fail("Unexpected exception: {}".format(e))

        with self.assertRaises(Exception):
            self.parse_json("tests/step2/invalid.json")

    def test_step3(self):
        try:
            result = self.parse_json("tests/step3/valid.json")
            self.assertEqual(
                result,
                {
                    "key1": True,
                    "key2": False,
                    "key3": None,
                    "key4": "value",
                    "key5": 101,
                },
            )
        except Exception as e:
            self.fail("Unexpected exception: {}".format(e))

        with self.assertRaises(Exception):
            self.parse_json("tests/step3/invalid.json")

    def test_step4(self):
        try:
            result = self.parse_json('tests/step4/valid.json')
            self.assertEqual(result, {"key": "value","key-n": 101,"key-o": {},"key-l": []})
        except Exception as e:
            self.fail('Unexpected exception: {}'.format(e))

        try:
            result = self.parse_json('tests/step4/valid2.json')
            self.assertEqual(result, {"key": "value","key-n": 101,"key-o": {"inner key": "inner value"},"key-l": ["list value"]})
        except Exception as e:
            self.fail('Unexpected exception: {}'.format(e))

        with self.assertRaises(Exception):
            self.parse_json('tests/step4/invalid.json')


if __name__ == "__main__":
    unittest.main()
