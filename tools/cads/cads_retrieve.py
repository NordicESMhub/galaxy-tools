import argparse
import ast
from os import environ, path

import cdsapi

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--request", type=str, help="input API request")
parser.add_argument("-o", "--output", type=str, help="output API request")
args = parser.parse_args()

with open(args.request) as f:
    req = f.read()
    f.close()
    mapped_chars = {
        '>': '__gt__',
        '<': '__lt__',
        "'": '__sq__',
        '"': '__dq__',
        '[': '__ob__',
        ']': '__cb__',
        '{': '__oc__',
        '}': '__cc__',
        '@': '__at__',
        '#': '__pd__',
        "": '__cn__'
    }

    # Unsanitize labels (element_identifiers are always sanitized by Galaxy)
    for key, value in mapped_chars.items():
        req = req.replace(value, key)

print("req = ", req)
c3s_type = req.split('c.retrieve')[1].split('(')[1].split(',')[0].strip(' "\'\t\r\n')

c3s_req = '{' + req.split('{', 1)[1].rsplit('}', 1)[0].replace('\n', '') + '}'
c3s_req_dict = ast.literal_eval(c3s_req)

c3s_output = req.rsplit('}', 1)[1].split(',')[1].split(')')[0].strip(' "\'\t\r\n')

with open(args.output, "w") as f:
    f.write(f'dataset to retrieve: {c3s_type}\nrequest: {c3s_req}\noutput filename: {c3s_output}')
    f.close()

print("start retrieving data...")

cdapi_file = path.join(environ.get('HOME'), '.cdsapirc')

if path.isfile(cdapi_file):
    c = cdsapi.Client()

    c.retrieve(
        c3s_type,
        c3s_req_dict,
        c3s_output)

    print("data retrieval successful")
