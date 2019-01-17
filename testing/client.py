

import subprocess
import requests
import urllib3


import uuid
import os
import json

from ga_service.ga_action import *
from py_client.population import *




args= {'id': str(uuid.uuid1()),
           'problem': {
             'name': 'BBOB',
             'function': 'FUNCTION' in os.environ and int(os.environ['FUNCTION']) or  3,
             'instance': 'INSTANCE' in os.environ and int(os.environ['INSTANCE']) or  1,
             'search_space': [-5, 5],
             'dim': 'DIM' in os.environ and int(os.environ['DIM']) or  3,
             'error': 1e-8
            },

        'population': [],
        'population_size':'POPULATION_SIZE' in os.environ and int(os.environ['POPULATION_SIZE']) or 1000,

        'experiment':
        {
             'experiment_id': 'dc74efeb-9d64-11e7-a2bd-54e43af0c111',
             'owner': 'mariosky',
             'type': 'benchmark'
        },

     'algorithm': {
         'name': 'GA',
         'iterations': 10,

         'selection': {
             'type': 'tools.selTournament',

             'tournsize': 12
         },
         'crossover': {'type': 'cxTwoPoint',
                        'random':True,
                       'CXPB_RND': [0.8, 1],
                       'CXP':0.5

                       },

         'mutation': {'type': 'mutGaussian',
                      'mu': 0,
                      'sigma': 0.5,
                      'indpb' : 0.05,
                       'MUTPB':0.5
                       }
        }
     }

pop = create_sample(args)
args['population'] = pop

print(json.dumps(args))


LOCAL_DEV = True


if  LOCAL_DEV:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    verify=False
    print('-- Ignoring SSL errors. --')
else:
    verify=True




APIHOST = 'https://localhost:31001'
AUTH_KEY = subprocess.check_output("wsk property get --auth", shell=True).decode('utf-8').split()[2]
print(AUTH_KEY)
NAMESPACE = 'guest'
ACTION = 'ga'
PARAMS = args

BLOCKING = 'true'
RESULT = 'true'

url = APIHOST + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION
user_pass = AUTH_KEY.split(':')
print(user_pass)
response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]), verify=verify )
print(response.text)




