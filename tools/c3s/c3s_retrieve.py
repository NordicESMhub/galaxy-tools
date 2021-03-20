import argparse
import ast
import cdsapi

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--request", type=str, help="input API request")
args = parser.parse_args()

f = open(args.request, "r")

req = f.read()

c3s_type=req.split('c.retrieve')[1].split('(')[1].split(',')[0].strip(' "\'\t\r\n')

c3s_req = '{' + req.split('{')[1].split('}')[0].replace('\n','') + '}'
c3s_req_dict = ast.literal_eval(c3s_req)

c3s_output = req.split('}')[1].split(',')[1].split(')')[0].strip(' "\'\t\r\n')

print("type of data to retrieve: ", c3s_type)
print("request: ", c3s_req_dict)
print("output filename: ", c3s_output)

print("start retrieving data...")
c = cdsapi.Client()

c.retrieve(
    c3s_type,
    c3s_req_dict,
    c3s_output)

print("data retrieval successful")