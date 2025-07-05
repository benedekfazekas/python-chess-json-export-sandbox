import chess
import typing
import json
from chess.pgn import BaseVisitor, SKIP, SkipType, NAG_GOOD_MOVE, NAG_MISTAKE, NAG_BRILLIANT_MOVE, NAG_BLUNDER, NAG_SPECULATIVE_MOVE, NAG_DUBIOUS_MOVE
from typing import Optional, List, Union, Callable, Any

if typing.TYPE_CHECKING:
    from typing_extensions import Self, override
else:
    F = typing.TypeVar("F", bound=Callable[..., Any])
    def override(fn: F, /) -> F:
        return fn

def _standardize_comments(comment: Union[str, list[str]]) -> List[str]:
    # This function ensures comments are always a list of strings
    if isinstance(comment, str):
        return [comment]
    elif isinstance(comment, list):
        return comment
    return []

def to_edn(obj, str_as_keyword: bool = False):
    """Recursively convert Python data structures to EDN strings."""
    if isinstance(obj, dict):
        return '{' + ' '.join(f'{to_edn(k, True)} {to_edn(v)}' for k, v in obj.items()) + '}'
    elif isinstance(obj, list):
        return '[' + ' '.join(to_edn(x) for x in obj) + ']'
    elif isinstance(obj, str):
        if str_as_keyword:
            return f':{obj.replace("_", "-")}'
        else:
            return f'"{obj}"'
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif obj is None:
        return 'nil'
    else:
        return str(obj)

# to easily map back to NAG string representation
NAG_TO_PGN_STRING = {NAG_GOOD_MOVE: "!",
                     NAG_MISTAKE: "?",
                     NAG_BRILLIANT_MOVE: "!!",
                     NAG_BLUNDER: "??",
                     NAG_SPECULATIVE_MOVE: "!?",
                     NAG_DUBIOUS_MOVE: "?!"}

class JsonExporter(BaseVisitor[str]):
    def __init__(self, *, headers: bool = True, comments: bool = True, variations: bool = True, edn: bool
                 = False, concise: bool = False):
        self.headers_flag = headers
        self.comments_flag = comments
        self.variations_flag = variations
        self.edn_flag = edn
        self.indent = None if concise else 2

        self.reset_game()

    def reset_game(self):
        self.game_data = {
            "headers": {},
            "moves": [],
            "result": None,
        }
        self.current_variation = self.game_data["moves"]
        self.variation_stack = []
        self.variation_depth = 0

    def begin_headers(self) -> None:
        self.game_data["headers"] = {}

    def visit_header(self, tagname: str, tagvalue: str) -> None:
        if self.headers_flag:
            self.game_data["headers"][tagname] = tagvalue

    def end_headers(self) -> None:
        pass  # Nothing needed here

    def begin_variation(self) -> Optional[SkipType]:
        self.variation_depth += 1
        if not self.variations_flag:
            return SKIP
        variation = []
        move_entry = {"variation": variation}
        self.current_variation.append(move_entry)
        self.variation_stack.append(self.current_variation)
        self.current_variation = variation

    def end_variation(self) -> None:
        self.variation_depth -= 1
        if self.variation_stack:
            self.current_variation = self.variation_stack.pop()

    def visit_comment(self, comment: Union[str, list[str]]) -> None:
        if self.comments_flag:
            comments = _standardize_comments(comment)
            if self.current_variation:
                if "comments" not in self.current_variation[-1]:
                    self.current_variation[-1]["comments"] = []
                self.current_variation[-1]["comments"].extend(comments)

    def visit_nag(self, nag: int) -> None:
        if self.comments_flag:
            if self.current_variation:
                if "nags" not in self.current_variation[-1]:
                    self.current_variation[-1]["nags"] = []
                self.current_variation[-1]["nags"].append({nag: NAG_TO_PGN_STRING.get(nag)})

    def visit_move(self, board: chess.Board, move: chess.Move) -> None:
        move_entry = {
            "move_number": board.fullmove_number,
            "turn": "white" if board.turn == chess.WHITE else "black",
            "san": board.san(move),
            "uci": move.uci(),
        }
        self.current_variation.append(move_entry)

    def visit_result(self, result: str) -> None:
        self.game_data["result"] = result

    @override
    def result(self) -> str:
        if self.edn_flag:
            result_string = to_edn(self.game_data)
        else:
            result_string = json.dumps(self.game_data, indent=self.indent)
        self.reset_game()
        return result_string

    def __str__(self) -> str:
        return self.result()
