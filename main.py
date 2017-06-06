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

def dowload_source(source, timeout, chunk_size, agent):
    local_filename = 'test.html'
    headers = {
    'User-Agent': agent
    }
    with closing(requests.get(source, headers=headers, stream=True, timeout=timeout)) as r:
        if 'text/html' in r.headers['Content-Type']:
            for chunk in r.iter_content(chunk_size):
                if chunk:
                    print("Ok")
                    return chunk
                else:
                    print ("Page is empty")
        else:
            print ("This is not text!")

def check_robots(source, agent):
    url = urlparse(source).scheme + "://" + urlparse(source).netloc + "/robots.txt"
    print (url)
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url)
    rp.read()
    return rp.can_fetch(agent, source)



if check_robots(args.source, agent):
    dowload_source(args.source, args.timeout, args.chunk_size, agent)
