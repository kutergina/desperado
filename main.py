import argparse

parser = argparse.ArgumentParser(description='Process bla bla bla')
parser.add_argument('--source', required=True, help='Is it start?')
parser.add_argument('--radius', type=int, default=2, help='Radius of action')
parser.add_argument('--chunk_size', type=int, default=1048576, help='Size of chunk')
parser.add_argument('--timeout', type=int, default=10, help='Timeout')

args = parser.parse_args()

import requests
from contextlib import closing

local_filename = 'test.html'
#r = requests.get(args.source, stream=True, timeout=args.timeout)
with closing(requests.get(args.source, stream=True, timeout=args.timeout)) as r:
    if 'text/html' in r.headers['Content-Type']:
        with open(local_filename, 'wb') as output_file:
            for chunk in r.iter_content(args.chunk_size):
                if chunk:
                    output_file.write(chunk)
                    output_file.flush()
        print(r.headers)
    else:
        print ('This is not text!')



