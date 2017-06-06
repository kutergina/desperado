import argparse
import requests
from contextlib import closing
from urllib.parse import urlparse
import urllib.robotparser

parser = argparse.ArgumentParser(description='Process bla bla bla')
parser.add_argument('--source', required=True, help='Is it start?')
parser.add_argument('--radius', type=int, default=2, help='Radius of action')
parser.add_argument('--chunk_size', type=int, default=1048576, help='Size of chunk')
parser.add_argument('--timeout', type=int, default=10, help='Timeout')

args = parser.parse_args()
agent = 'Desperado'

def dowload_source(args):
    local_filename = 'test.html'
    headers = {
    'User-Agent': agent
    }
    with closing(requests.get(args.source, headers=headers, stream=True, timeout=args.timeout)) as r:
        if 'text/html' in r.headers['Content-Type']:
            with open(local_filename, 'wb') as output_file:
                for chunk in r.iter_content(args.chunk_size):
                    if chunk:
                        output_file.write(chunk)
                        output_file.close()
                        print("Ok")
        else:
            print ('This is not text!')

def check_robots(source):
    url = urlparse(source).scheme + "://" + urlparse(source).netloc + "/robots.txt"
    print (url)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url)
    rp.read()
    return rp.can_fetch(agent, source)


dowload_source(args)
print (check_robots(args.source))
