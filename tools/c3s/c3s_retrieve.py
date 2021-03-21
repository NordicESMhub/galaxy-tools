from os import path
import argparse
import ast

import cdsapi

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--request", type=str, help="input API request")
parser.add_argument("-o", "--output", type=str, help="output API request")
args = parser.parse_args()

if path.isfile(args.request):
   f = open(args.request, "r")
   req = f.read()
   f.close()
else:
   req = args.request

c3s_type = req.split('c.retrieve')[1].split('(')[1].split(',')[0].strip(' "\'\t\r\n')

c3s_req = '{' + req.split('{')[1].split('}')[0].replace('\n', '') + '}'
c3s_req_dict = ast.literal_eval(c3s_req)

c3s_output = req.split('}')[1].split(',')[1].split(')')[0].strip(' "\'\t\r\n')

f = open(args.output, "w")
f.write("dataset to retrieve: " + c3s_type + "\n")
f.write("request: " + c3s_req + "\n")
f.write("output filename: " + c3s_output)
f.close()

print("start retrieving data...")
c = cdsapi.Client()

c.retrieve(
    c3s_type,
    c3s_req_dict,
    c3s_output)

print("data retrieval successful")
