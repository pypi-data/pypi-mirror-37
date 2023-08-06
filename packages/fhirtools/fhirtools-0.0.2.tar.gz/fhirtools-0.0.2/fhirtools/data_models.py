import json
import jsonschema
import os

class data_models(object):

    def __init__(self):
        pass


    def load(self, resource_type):

        module_path = os.path.dirname(os.path.abspath(__file__))
        schema = json.loads(open(module_path + '/schemas/' + resource_type + '.schema.json', 'rb').read())
        return schema

    def validate(self, resource):

        try:
            resource_type = resource['resourceType']
            schema = self.load(resource_type)
            jsonschema.validate(resource, schema)
            return True
        except:
            return False