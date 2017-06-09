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
                    #это ведь наверное не правильно так делать?
                    return str(chunk)
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
#а это я просто скопировала и не доконца понимаю, что тут происходит
#может можно проще как-то сделать?
class MyHTMLParser(HTMLParser):
    #например, вот в этой части (зачем все это)
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []  
  #а здесь вопросов нет) все понятно
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            try:
                self.links.append(attrs['href'])
            except:
                pass

    
if check_robots(args.source, agent):
    data = dowload_source(args.source, args.timeout, args.chunk_size, agent)
    parser = MyHTMLParser()
    parser.feed(data)
 
