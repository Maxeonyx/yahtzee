import templates
import random


def zip_lists(*lists):

    length = len(lists[0])
    for l in lists:
        if len(l) != length:
            raise IndexError("Lists not equal length")
    zipped = []
    for i in range(length):
        for l in lists:
            zipped.append(l[i])
    return zipped


class Player:



    def __init__(self, name):
        self.name = name
        self.combos = [0]*13
        self.upper_subtotal = 0
        self.lower_subtotal = 0
        self.bonus = 0
        self.total = 0

    def check_if_combo_used(self, combo_name):

        combo_index = templates.COMBO_INDICES[combo_name]

        if self.combos[combo_index] != 0 and combo_name != "yahtzee":
            return False

        if self.combos[combo_index] == "Blocked":
            return False

        return True


    def set_combo(self, combo_name, score):

        combo_index = templates.COMBO_INDICES[combo_name]

        if combo_name == "yahtzee" and score != "Blocked":
            self.combos[combo_index] += score
            print("Congratulations on the Yahtzee!")
        elif score == "Blocked":
            self.combos[combo_index] = score
            print("{} has blocked their '{}' combo".format(self.name, combo_name))
        else:
            self.combos[combo_index] = score
            print("{} now has {} points for their '{}' combo".format(self.name, score, combo_name))

    def get_upper_subtotal(self):

        total = 0
        for val in self.combos[:6]:
            if val != "Blocked":
                total += val
        return total


    def get_lower_subtotal(self):

        total = 0
        for val in self.combos[6:]:
            if val != "Blocked":
                total += val
        return total


    def get_bonus(self):

        if self.get_upper_subtotal() > 62:
            return 35

        return 0


    def get_total(self):

        total = self.get_upper_subtotal() + self.get_lower_subtotal() + self.get_bonus()
        return total

    def sum_sections(self):
        self.upper_subtotal = self.get_upper_subtotal()
        self.bonus = self.get_bonus()
        self.lower_subtotal = self.get_lower_subtotal()
        self.total = self.get_total()

    def get_all_categories(self):

        all_categories = []

        all_categories += [self.name]
        all_categories += self.combos[:6]
        all_categories += [self.upper_subtotal]
        all_categories += [self.bonus]
        all_categories += self.combos[6:]
        all_categories += [self.lower_subtotal]
        all_categories += [self.total]

        return all_categories


class Scoreboard:

    def __init__(self, players):

        self.players = players
        self.num_players = len(players)
        self.curr_player_index = -1

    def next_turn(self):

        self.next_player()

        self.begin_turn()

    def next_player(self):

        if self.curr_player_index + 1 > self.num_players - 1:
            self.curr_player_index = 0
        else:
            self.curr_player_index += 1


    def begin_turn(self):
            print("It's {}'s turn!".format(self.players[self.curr_player_index].name))


    def save_game(self):

        out = open("savegame.sav",'w')

        out.write(str(self.curr_player_index)+'\n')
        out.write(str(self.num_players)+'\n')
        for player in self.players:
            out.write(player.name+'\n')
            for combo_score in player.combos:
                out.write(str(combo_score)+'\n')

        out.close()

    def load_game(self):

        try:
            in_file = open("savegame.sav")
        except FileNotFoundError:
            return False

        self.curr_player_index = int(in_file.readline())
        self.num_players = int(in_file.readline())

        for player_index in range(self.num_players):

            player_name = in_file.readline().strip()
            player = Player(player_name)

            for combo_index in range(len(templates.COMBO_INDICES)):
                player.combos[combo_index] = int(in_file.readline())

            self.players.append(player)

        return True


    def __str__(self):

        none_player = Player("Empty")

        temp_players = []
        temp_players += self.players
        while len(temp_players) < 4:
            temp_players.append(none_player)

        players_categories = [player.get_all_categories() for player in temp_players]

        filled_scoreboard = templates.SCOREBOARD.format(*zip_lists(*players_categories))

        return filled_scoreboard

    def display(self):

        print(str(self))

    def check_if_combo_used(self, combo, player_index="default"):
        if player_index == "default":
            player_index = self.curr_player_index

        return self.players[player_index].check_if_combo_used(combo)

    def set(self, combo, score):

        self.players[self.curr_player_index].set_combo(combo, score)


def main():

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

    nums_dict = {}

    for d in dice:
        nums_dict[d] = nums_dict.get(d, 0) + 1

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
    kept_dice = list(kept_dice)
    rolled_dice = list(rolled_dice)
    try:
        for die in kept_dice:
            rolled_dice.pop(rolled_dice.index(die))
    except ValueError:
        return False
    return True

def check_valid_help(help_parameters):

    if len(help_parameters) > 1:
        return False

    if len(help_parameters) == 0:
        return True

    if help_parameters[0] in templates.HELP_PARAMETERS:
        return True

    return False


def roll_dice(dice=[]):
    dice = list(dice) # prevents mutability shit. maybe I should be using tuples?

    r = random.Random()

    num_to_roll = max(0,5-len(dice))

    for i in range(num_to_roll):
        new_die = r.randint(1,6)
        dice.append(new_die)

    dice.sort()

    return dice


def print_dice(dice):

    print()

    num_lines = len(templates.DICE_DICT[1].split("\n"))
    separator = '  '
    for i in range(num_lines):
        line = ''
        for die in dice:
            line += templates.DICE_DICT[die].split("\n")[i] + separator
        print(line)


def get_command(prompt, last_roll, num_rolls, board):

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
                print("Invalid arguments for 'keep'. Please enter numbers between 1 and 6 inclusive.")
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
            #gets the valid help parameters except the blank one
            valid_params = sorted(templates.HELP_PARAMETERS.keys())[1:]

            print("Invalid help parameter. Use one of: (blank)", *valid_params, sep=', ')
            return get_command(prompt, last_roll, num_rolls, board)

        if len(params[1:]) == 0:
            params.append('')

    return params


def get_int(prompt=': '):
    failed = True
    while failed:
        try:
            integer = int(input(prompt))
            failed = False
        except ValueError:
            print("Please input a valid integer")
    return integer


def get_string(prompt=': ', maxsize=-1):
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
