import argparse

parser = argparse.ArgumentParser(description='Process bla bla bla')
parser.add_argument('--source', required=True, help='Is it start?')
parser.add_argument('--radius', type=int, default=2, help='Radius of action')

args = parser.parse_args()

import requests
r = requests.get(args.source, stream=True, timeout=10)
if r.headers['Content-Type'].find('text/html') != -1:
    print(r.headers)
else:
    print ('This is not text!')

