import json


class JsonReference(object):
    def __init__(self, json_data):
        self.json_data = json_data
        
        # Feed the json_data to parser for futher processing. 
        self.parser(self.json_data)

    def __getattr__(self, attr):
            return None


    def parser(self, json_data, reference=None):
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if reference:
                    reference = "{}_{}".format(reference, key)
                else:
                    reference = key

                setattr(JsonReference, reference, value)
                self.parser(value, reference=reference)

        elif any(isinstance(json_data, list_or_tuble) for list_or_tuble in (list, tuple)):
            for key, value in enumerate(json_data):
                if reference:
                    reference = "{}_{}".format(reference, key)
                else:
                    reference = key

                setattr(JsonReference, reference, value)
                self.parser(value, reference=reference)