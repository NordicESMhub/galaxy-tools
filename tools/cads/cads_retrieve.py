import argparse
import ast
import sys
from os import environ

import cdsapi

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--request", type=str, help="input API request")
parser.add_argument("-o", "--output", type=str, help="output API request")
args = parser.parse_args()

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

with open(args.request) as f:
    req = f.read()

    # Unsanitize labels (element_identifiers are always sanitized by Galaxy)
    for key, value in mapped_chars.items():
        req = req.replace(value, key)

print("req = ", req)

c3s_type = req.split('dataset')[1].split('=')[1].split('\n')[0].strip(' "\'\t\r\n')
c3s_req = '{' + req.split('request', 1)[1].split('{', 1)[1].rsplit('}', 1)[0].replace('\n', '') + '}'
c3s_req_dict = ast.literal_eval(c3s_req)

print("start retrieving data...")

api_key = environ.get("CADS_API_KEY")

if not api_key:
    sys.stderr.write(
        "CADS retrieval failed, make sure you filled in your CADS API Key\n"
    )
    sys.exit(1)

try:
    c = cdsapi.Client(
        url="https://ads.atmosphere.copernicus.eu/api",
        key=api_key
    )

    result = c.retrieve(c3s_type, c3s_req_dict)
    c3s_output = result.download()

    print("data retrieval successful")
except Exception:
    raise RuntimeError(
        "CADS retrieval failed, make sure you filled in your CADS API Key"
    )

with open(args.output, "w") as f:
    f.write(f'dataset to retrieve: {c3s_type}\nrequest: {c3s_req}\noutput filename: {c3s_output}')
