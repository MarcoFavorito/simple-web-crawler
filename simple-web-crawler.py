import argparse

parser = argparse.ArgumentParser(description='A very simple web crawler')
parser.add_argument('url', metavar='URL', type=str, nargs=1,
                    help='The url of the page where to start.')

args = parser.parse_args()

def main():
    pass


if __name__ == '__main__':
    main()