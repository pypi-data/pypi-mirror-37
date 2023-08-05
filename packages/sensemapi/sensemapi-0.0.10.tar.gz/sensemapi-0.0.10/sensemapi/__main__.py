# system modules
import argparse

# internal modules
import sensemapi

# external modules

parser = argparse.ArgumentParser(
    prog = "python3 -m sensemapi",
    description = "Command-line interface to the OpenSenseMap API",
    epilog = "This CLI is not yet implemented."
    )
args = parser.parse_args()
parser.print_help()
