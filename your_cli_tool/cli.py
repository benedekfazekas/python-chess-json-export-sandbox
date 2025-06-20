import argparse
import chess
#from .main import main_function

def parse_args():
    parser = argparse.ArgumentParser(description="Your CLI Tool")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('input', help='Input argument')
    return parser.parse_args()

def cli():
    args = parse_args()
    main_function(args.input)
