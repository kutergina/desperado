import argparse

parser = argparse.ArgumentParser(description='Process bla bla bla')
parser.add_argument('--source', help='Is it start?')
parser.add_argument('--radius', help='Radius of action')

args = parser.parse_args()
print(args.accumulate(args.integers))
