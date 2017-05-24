import argparse

parser = argparse.ArgumentParser(description='Process bla bla bla')
parser.add_argument('--source', required=True, help='Is it start?')
parser.add_argument('--radius', type=int, default=2, help='Radius of action')

args = parser.parse_args()

import requests

r = requests.get(args.source, stream=True, timeout=10)
if 'text/html' in r.headers['Content-Type']:
    with open('test.html', 'w') as output_file:
          output_file.write(r.text)
    print(r.headers)
else:
    print ('This is not text!')

