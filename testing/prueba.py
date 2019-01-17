import uuid
import os
import json

from ga_google.ga_deap import *

with open('parameters.json') as json_file:
    data = json.load(json_file)




worker = GA_Worker(data)
worker.setup()
result = worker.run()

    # Return with a format for writing to MessageHub
print(  json.dumps(result, indent=2))


