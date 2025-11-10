import argparse
import chess
from typing import TextIO
from your_cli_tool import json_exporter

def parse_args():
    parser = argparse.ArgumentParser(description="Pgn to json/edn converter")
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('-i',
                        '--input',
                        type=argparse.FileType('r'),
                        help="The input file to be processed (use '-' for stdin)")
    parser.add_argument('-o',
                        '--output',
                        type=argparse.FileType('w'),
                        help="The output file for results (use '-' for stdout)")
    parser.add_argument('-b',
                        '--forblack',
                        action='store_true',
                        help='Board images are generated for black')
    parser.add_argument('-e',
                        '--edn',
                        action='store_true',
                        help='output is edn instead of json')
    return parser.parse_args()

def pgn_to_json(input_pgn: TextIO, output_json: TextIO, forblack: bool, edn: bool) -> None:
    #print(f"input_file[{input_pgn}], output_file[{output_json}], forblack[{forblack}], edn[{edn}]")
    extension = 'edn' if edn else 'json'
    print(f"Reading {input_pgn.name} and converting to {extension}")
    exporter = json_exporter.JsonExporter(headers=True, variations=True, comments=True, edn=edn, board_img_for_black=forblack)
    parsed_game = chess.pgn.read_game(input_pgn)
    game_json_edn = parsed_game.accept(exporter)
    print(game_json_edn, file=output_json, end="\n\n")
    print(f"Conversion to {extension} done, written to {output_json.name} ")

def cli():
    args = parse_args()
    #print(f"my args {args}")
    pgn_to_json(args.input, args.output, args.forblack, args.edn)

if __name__ == "__main__":
    cli()
