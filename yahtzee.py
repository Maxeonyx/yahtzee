"""
Play a game of Yahtzee. I made this as a small project, and got it reasonably
nice and polished.

Created by Maxeonyx
"""

import templates
import random

from scoreboard import Scoreboard
from player import Player


def main():
    """
    the main function. The game logic begins here.
    """

    players = []
    num_players = get_int("Input the number of players or 0 to load a game: ")

    for i in range(num_players):
        player_name = get_string("Input player {}'s name: ".format(i+1), 10)
        players.append(Player(player_name))

    board = Scoreboard(players)
    if num_players == 0:
        succeeded = board.load_game()
        if not succeeded:
            print("There is no savegame. The game will now quit")
            exit()

    last_roll = []
    num_rolls = 0

    board.begin_turn()

    while True:
        params = get_command(': ', last_roll, num_rolls, board)

        command = params[0]
        args = params[1:]

        if command == 'keep':
            last_roll = roll_dice(args)
            print_dice(last_roll)
            num_rolls += 1

        elif command == 'roll':
            last_roll = roll_dice([])
            print_dice(last_roll)
            num_rolls += 1

        elif command in templates.COMBO_COMMANDS:
            score = get_combo_score(command, last_roll)
            board.set(command, score)
            num_rolls = 0
            last_roll = []
            board.next_turn()

        elif command == 'block':
            combo = args[0]
            board.set(combo, "Blocked")
            num_rolls = 0
            last_roll = []
            board.next_turn()

        elif command == 'print':
            board.display()

        elif command == 'save':
            board.save_game()
            print("Saved the game.")

        elif command == 'load':
            board.load_game()
            print("Loaded a game save.")

        elif command == 'help':
            parameter = args[0]
            print(templates.HELP_PARAMETERS[parameter])

        elif command == 'exit':
            y_or_n = input("Save game? (y/n): ")

            while not y_or_n in 'yn':
                y_or_n = input("Save game? (y/n): ")

            if y_or_n == 'y':
                board.save_game()

            exit()

        elif command == 'finish':

            for player in board.players:
                player.sum_sections()

            board.display()

            exit()


def get_combo_score(combo, dice):
    """
    takes a VALID combo name and a valid list of dice for that combo,
    and returns an int, the score of that combo.
    """

    if combo in templates.UPPER_COMBO_COMMANDS:
        dice_num = templates.COMBO_INDICES[combo] + 1 # NOTE REPLACE THIS LINE NOTE
        dice_to_sum = [d for d in dice if d == dice_num]
        return sum(dice_to_sum)

    elif combo == 'fullhouse':
        return 25

    elif combo == 'threeofakind' or combo == 'fourofakind' or combo == 'chance':
        return sum(dice)

    elif combo == 'shortstraight':
        return 30

    elif combo == 'longstraight':
        return 40

    elif combo == 'yahtzee':
        return 50


def check_valid_combo(combo, dice):
    """
    takes a VALID combo, and a list of dice, and checks whether the combo is
    valid for those dice.
    """
    nums_dict = {}

    for die in dice:
        nums_dict[die] = nums_dict.get(die, 0) + 1

    run = 0
    has_pair = False
    has_triple = False
    has_quadruple = False
    has_quintuple = False
    has_short_straight = False
    has_long_straight = False

    for die, count in sorted(nums_dict.items()):

        if count == 0:
            run = 0
        else:
            run += 1

        if run == 4:
            has_short_straight = True

        if run == 5:
            has_long_straight = True

        if count == 2:
            has_pair = True

        elif count == 3:
            has_triple = True

        elif count == 4:
            has_quadruple = True

        elif count == 5:
            has_quintuple = True

    if combo in templates.UPPER_COMBO_COMMANDS:
        dice_num = templates.COMBO_INDICES[combo] + 1 # NOTE REPLACE THIS LINE NOTE
        if nums_dict.get(dice_num, 0) > 0:
            return True

    elif combo == 'fullhouse':
        if has_pair and has_triple:
            return True

    elif combo == 'threeofakind':
        if has_triple or has_quadruple or has_quintuple:
            return True

    elif combo == 'fourofakind':
        if has_quadruple or has_quintuple:
            return True

    elif combo == 'yahtzee':
        if has_quintuple:
            return True

    elif combo == 'shortstraight':
        if has_short_straight:
            return True

    elif combo == 'longstraight':
        if has_long_straight:
            return True

    elif combo == 'chance':
        return True

    return False


def check_valid_keep(kept_dice, rolled_dice):
    """
    takes a list of dice that the player chose to keep, and checks whether those
    dice exist in the actual rolled dice.

    returns True if the dice exist, and False if the kept dice are invalid.
    """
    kept_dice = list(kept_dice)
    rolled_dice = list(rolled_dice)
    try:
        for die in kept_dice:
            rolled_dice.pop(rolled_dice.index(die))
    except ValueError:
        return False
    return True


def check_valid_help(help_parameters):
    """

    :param help_parameters: a list of strings given with the 'help' command
    :return: True if the
    """
    if len(help_parameters) > 1:
        return False

    if len(help_parameters) == 0:
        return True

    if help_parameters[0] in templates.HELP_PARAMETERS:
        return True

    return False


def roll_dice(dice):
    """
    takes a valid set of kept dice, and rerolls the remaining dice.

    to roll all new dice, pass this function an empty list.

    returns a list of five integers betwenn 1 and 6 inclusive, representing 5
    dice rolls
    """
    dice = list(dice) # prevents mutability shit. maybe I should be using tuples?

    num_to_roll = max(0, 5-len(dice))

    for _ in range(num_to_roll):
        new_die = random.randint(1, 6)
        dice.append(new_die)

    dice.sort()

    return dice


def print_dice(dice):
    """
    takes a list of dice (a list of 5 ints between 1 and 6)
    and prints a fancy looking image using the dice templates
    """

    print()

    num_lines = len(templates.DICE_DICT[1].split("\n"))
    separator = '  '
    for i in range(num_lines):
        line = ''
        for die in dice:
            line += templates.DICE_DICT[die].split("\n")[i] + separator
        print(line)


def get_command(prompt, last_roll, num_rolls, board):
    """
    This function is really big and yucky.
    It takes a prompt, the last roll, the number of times the current player has
    rolled, and returns a 100% valid command. That's all you need to know.

    The return value is a list. the first value is the command name,
    and the remaining values are valid parameters for that command.

    e.g. for the keep command, a valid return value from this function might be:
        ['keep', 1, 1, 5]
        in this instance, this is only valid if the original dice rolled
        contained two 1's and a 5
        If this function returns it, you can assume to be valid.
    """
    params = input(prompt).strip().split()

    while not params[0] in templates.COMMANDS:
        print("Please enter a valid command.")
        return get_command(prompt, last_roll, num_rolls, board)

    if params[0] == 'keep':

        if len(params[1:]) < 1 or len(params[1:]) > 5:
            print("Invalid arguments for 'keep'. Too many or too few dice.")
            return get_command(prompt, last_roll, num_rolls, board)

        for kept_die in params[1:]:
            if not kept_die.isdigit():
                print("Invalid arguments for 'keep'. Must be valid numbers.")
                return get_command(prompt, last_roll, num_rolls, board)

            if int(kept_die) < 1 or int(kept_die) > 6:
                print("Invalid arguments for 'keep'. Please enter numbers " +
                      "between 1 and 6 inclusive."
                     )
                return get_command(prompt, last_roll, num_rolls, board)

        kept_dice = [int(d) for d in params[1:]]

        if not check_valid_keep(kept_dice, last_roll):
            print("Invalid arguments for 'keep'. You can't keep dice that aren't there!")
            return get_command(prompt, last_roll, num_rolls, board)

        params = [params[0]] + kept_dice

    if params[0] == 'keep' or params[0] == 'roll':
        if num_rolls > 2:
            print("You have used all your rolls!")
            return get_command(prompt, last_roll, num_rolls, board)

    if params[0] == 'block':

        combo = params[1]

        if len(params) != 2:
            print("Invalid arguments for 'block'. Must specify exactly one combo.")
            return get_command(prompt, last_roll, num_rolls, board)

        if not combo in templates.COMBO_INDICES:
            print("Invalid arguments for 'block'. Must specify a valid combo.")
            return get_command(prompt, last_roll, num_rolls, board)

        if not board.check_if_combo_used(combo):
            print("This combo is already used.")
            return get_command(prompt, last_roll, num_rolls, board)

    if params[0] in templates.COMBO_COMMANDS:

        combo = params[0]

        if not board.check_if_combo_used(combo):
            print("This combo is already used.")
            return get_command(prompt, last_roll, num_rolls, board)

        if not check_valid_combo(combo, last_roll):
            print("You cannot use this combo.")
            return get_command(prompt, last_roll, num_rolls, board)

    if params[0] == 'help':

        if not check_valid_help(params[1:]):

            valid_params = sorted(templates.HELP_PARAMETERS.keys())

            print("Invalid help parameter. Use one of: (blank)" + ', '.join(valid_params))
            return get_command(prompt, last_roll, num_rolls, board)

        if len(params[1:]) == 0:
            params.append('')

    return params


def get_int(prompt=': '):
    """
    gets a valid int from the player
    """
    failed = True
    while failed:
        try:
            integer = int(input(prompt))
            failed = False
        except ValueError:
            print("Please input a valid integer")
    return integer


def get_string(prompt=': ', maxsize=-1):
    """
    gets a valid string from the player. optional: take a maximum length for that
    string.
    :param prompt: a string to present to the user when taking input
    :param maxsize: prevent the user from entering strings more than a certain character length
    :return: the string obtained from the user
    """
    failed = True
    while failed:
        string = input(prompt)
        if len(string) < maxsize or maxsize == -1:
            failed = False
        else:
            print("Please input a valid string less than {} chars long".format(maxsize))

    return string


if __name__ == '__main__':
    main()
