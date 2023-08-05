from docopt import docopt
from mfetcher import fetcher

def main():
    args = docopt(fetcher.__doc__)
    fetcher.main(args)
