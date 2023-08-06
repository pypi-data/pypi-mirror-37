name = "hemlock_io"

import requests
import codecs
import pickle

def push_model(ip_address, model_object, model_name, model_description, variables, auth_token, version):
    pickled = codecs.encode(pickle.dumps(model_object), "base64").decode()
    
    var_list = []
    for variable in variables:
        var_list.append(variable)
    var_list = str(var_list)
    
    r = requests.post('https://' + str(ip_address) + '/api/models/'
                        ,headers={'Authorization': 'Token ' + str(auth_token)}
                        ,data={
                                'description': model_description
                               ,'version': 0
                               ,'user': 'default'
                               ,'name': model_name
                               ,'model': pickled
                               ,'variables': var_list
                               #,'hits': 0
                               }
                        )
    return r