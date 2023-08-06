import json
import fhirtools

with open('test.conf', 'r') as config_file:
    settings = json.loads(config_file.read())

fhir_client = fhirtools.fhir_client(settings)
r = fhir_client.search('Patient', {})
print(r)