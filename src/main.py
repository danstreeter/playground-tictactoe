# System Imports
import sys

# Framework / Library Imports

# Application Imports

# Local Imports

game_state = {
    "board_state": [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ],
    "plays": 0,
    "available_spaces": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "active_player": 0,  # int(bool) used here as can 'not-flip-flop', see play() active player swapping
    "p1_marker": True,
    "win_matrices": (
        ("1", "2", "3"),
        ("4", "5", "6"),
        ("7", "8", "9"),
        ("1", "4", "7"),
        ("2", "5", "8"),
        ("3", "6", "9"),
        ("1", "5", "9"),
        ("3", "5", "7"),
    ),
}


def _main():
    try:
        print("Welcome to Tic-Tac-Dan 1.0")

        player_token = (
            input("Player 1, please choose your marker, 'O' or 'X' (Defults to O): ")
            or "O"
        )
        if player_token not in ("X", "O"):
            print("Dont mess with me fool")
            sys.exit(1)
        elif player_token == "X":
            game_state["p1_marker"] = False

        while len(game_state["available_spaces"]) > 0:
            print_board(game_state)

            print(f"Player {int(game_state['active_player']+1)}, make your move!")

            play_position = input(f"Enter a number: {game_state['available_spaces']}")

            play(game_state, play_position)

    except ValueError:
        print("Whoops, try again...")
        pass

    except KeyboardInterrupt:
        print("\nThanks for playing Tic-Tac-Dan")
        sys.exit()


def play(game_state, position):
    # Handle a non value
    if position is None or position == "":
        return

    # Increase the play count
    game_state["plays"] += 1

    # Remove the played positiion from the available positions
    game_state["available_spaces"].remove(int(position))

    # Get the marker for the player
    if not game_state["active_player"]:  # Player 1
        marker = game_state["p1_marker"]
    else:
        marker = not game_state["p1_marker"]

    # Mark the position with the player counter
    _position_setter(game_state, position, marker)

    (win, who) = _win_checker(game_state)
    if win == True:
        print_board(game_state)
        print(
            f"We have a winner!!!\nPlayer {int(who)+1}, congratulations!!!\nYou are the champion of Tic-Tac-Dan!!!\n\n"
        )
        sys.exit(0)

    # Swap the active player
    game_state["active_player"] = not game_state["active_player"]

    return None


def print_board(game_state):
    """
    Prints the board out to screen
    """
    board_output = ""
    for row in game_state["board_state"]:
        board_output += ""
        board_row = []
        for col_val in row:
            board_row.append(_marker_symbol(game_state["p1_marker"], col_val))
        board_output += "|".join(board_row)

        board_output += "\n"
        board_output += "-----\n"

    # TODO - Remove the last line of lines
    print(board_output)


def _marker_symbol(p1_marker, value):
    """
    Determines the marker to use for a value on the board
    """
    if value is None:
        return " "
    elif value == True:
        return "O"
    elif value == False:
        return "X"
    else:
        return "!"


def _position_resolver(position):
    pos = {
        "1": (0, 0),
        "2": (0, 1),
        "3": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "7": (2, 0),
        "8": (2, 1),
        "9": (2, 2),
    }
    return pos[position]


def _position_setter(game_state, position, value):
    # print(f"Setting {position} to {value}")
    game_state["board_state"].__getitem__(_position_resolver(position)[0]).__setitem__(
        _position_resolver(position)[1], value
    )


def _position_getter(game_state, position):
    return (
        game_state["board_state"]
        .__getitem__(_position_resolver(position)[0])
        .__getitem__(_position_resolver(position)[1])
    )


def _win_checker(game_state):
    for combo in game_state["win_matrices"]:
        # print(f"Checking {combo}")
        a, b, c = (
            _position_getter(game_state, combo[0]),
            _position_getter(game_state, combo[1]),
            _position_getter(game_state, combo[2]),
        )

        if (a == b == c) and None not in (a, b, c):
            # print(f"WINNER: {a}")
            # print(f"P1 Token {game_state['p1_marker']}")
            if a == game_state["p1_marker"]:
                return (True, 0)  # Player 1
            else:
                return (True, 1)  # Player 2

    return (False, None)


if __name__ == "__main__":
    _main()
