import argparse

from mambas.server.database import MambasDatabase
from mambas.server.webserver import MambasWebserver

def main():
    args = parse_args()
    database = MambasDatabase()
    webserver = MambasWebserver(database)
    webserver.run(server="paste", host="0.0.0.0", port=args.port, debug=args.debug)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", default=False, action="store_true", help="Debug flag")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Mambas port")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()