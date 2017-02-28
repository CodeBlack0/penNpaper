import json
from utility import debug


# @debug(prefix='***')
def parse(name, path):
    with open(path, 'r') as f:
        parser = get_parse_function(name)
        return [json.loads(line, object_hook=parser) for line in f]


@debug(prefix='***')
def get_parse_function(name):
    ''' Gets the parser-function for the given data type'''
    return {'complex': complex}.get(name, identity)


@debug(prefix='***')
def identity(dct):
    ''' Basic identity function '''
    return dct


@debug(prefix='***')
def complex(dct):
    if '__complex__' in dct:
        return complex(dct['real'], dct['imag'])
    return dct


print(json.loads('{"__complex__": true, "real": 1, "imag": 2}', object_hook=get_parse_function('complex')))
