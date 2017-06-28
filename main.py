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
            for chunk in r.iter_content(chunk_size, decode_unicode=True):
                if chunk:
                    return chunk
                else:
                    print ("Page is empty")
        else:
            print ("This is not text!")

def check_robots(source, agent):
    url = urlparse(source).scheme + "://" + urlparse(source).netloc + "/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url)
    rp.read()
    return rp.can_fetch(agent, source)


from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, source_name):
        super().__init__()
        self.links = []
        self.source_name = source_name
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            try:
                self.links.append(attrs['href'])
            except:
                pass
#Удаление дубликатов
def unique(lst):
    seen = set()
    result = []
    for x in lst:
        if x in seen:
            continue
        seen.add(x)
        result.append(x)
    return result

def write_to_file(lst):
     f = open('links.txt', 'w')
     f.write('\n'.join(sorted(lst)))
     f.close()

if check_robots(args.source, agent):
    data = dowload_source(args.source, args.timeout, args.chunk_size, agent)
    parser = MyHTMLParser(args.source)
    parser.feed(data)
    print (parser.links)
    print (parser.source_name)
    write_to_file (unique(parser.links))
