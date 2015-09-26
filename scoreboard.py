"""
Contains the scoreboard class

Created by Maxeonyx
maxeonyx@gmail.com
"""

import templates
from player import Player

def zip_lists(*lists):
    """
    takes any number of EQUAL LENGTH lists and zips their elements together.
    """

    length = len(lists[0])
    for lis in lists:
        if len(lis) != length:
            raise IndexError("Lists not equal length")
    zipped = []
    for i in range(length):
        for lis in lists:
            zipped.append(lis[i])
    return zipped

class Scoreboard:
    """
    A class to control the game's scoreboard.

    public fields:
        - players : a list of the game's players (between 1 and 4 players inclusive)

    public methods:
        - begin_turn : None : Prints the new turn message.
        - next_turn : None : Changes to the next turn
        - save_game : None : outputs the current game state to savegame.sav
        - load_game : None : loads a game from savegame.sav should only be used
                             from an empty scoreboard
        - display : None : prints the scoreboard to the screen
        - check_if_combo_used : calls a similar method in the given player. If
                                no player is given, use the current player.

        - set : None : Set the score of a player and
    """

    def __init__(self, players):
        """
        initialises the scoreboard, takes a list of players.
        """
        self.players = players
        self.num_players = len(players)
        self.curr_player_index = -1

    def next_turn(self):
        """
        Changes the game turn over, and prints a message.
        """

        self.next_player()

        self.begin_turn()

    def next_player(self):
        """
        changes the current player to the next one
        """

        if self.curr_player_index + 1 > self.num_players - 1:
            self.curr_player_index = 0
        else:
            self.curr_player_index += 1


    def begin_turn(self):
        """
        prints a lovely message to signal the beginning of a turn.

        This is automatically called by next_turn
        """
        print("It's {}'s turn!".format(self.players[self.curr_player_index].name))


    def save_game(self):
        """
        saves the game state to savegame.sav
        can be loaded with load_game
        """

        out = open("savegame.sav", 'w')

        out.write(str(self.curr_player_index)+'\n')
        out.write(str(self.num_players)+'\n')
        for player in self.players:
            out.write(player.name+'\n')
            for combo_score in player.combos:
                out.write(str(combo_score)+'\n')

        out.close()

    def load_game(self):
        """
        loads the game state from the file savegame.sav
        returns False if the file does not exist.

        returns True if nothing failed.

        This will probably cause bugs if called from a non-empty scoreboard.
        It will also fail if the save file is modified/corrupted
        """
        try:
            in_file = open("savegame.sav")
        except FileNotFoundError:
            return False

        self.curr_player_index = int(in_file.readline())
        self.num_players = int(in_file.readline())

        for _ in range(self.num_players):

            player_name = in_file.readline().strip()
            player = Player(player_name)

            for combo_index in range(len(templates.COMBO_INDICES)):
                player.combos[combo_index] = int(in_file.readline())

            self.players.append(player)

        return True


    def __str__(self):
        """
        returns the string representation of the score board, ready to print.
        """

        none_player = Player("Empty")

        temp_players = []
        temp_players += self.players
        while len(temp_players) < 4:
            temp_players.append(none_player)

        players_categories = [player.get_all_categories() for player in temp_players]

        filled_scoreboard = templates.SCOREBOARD.format(*zip_lists(*players_categories))

        return filled_scoreboard

    def display(self):
        """
        prints the scoreboard to the screen
        """

        print(str(self))

    def check_if_combo_used(self, combo, player_index="default"):
        """
        takes a VALID combo and an optional player index.
        returns whether that player has used the given combo.

        If no player index is given, this uses the current player.
        """
        if player_index == "default":
            player_index = self.curr_player_index

        return self.players[player_index].check_if_combo_used(combo)

    def set(self, combo, score):
        """
        takes a VALID combo and score, and sets the current player's score for
        that combo to the given score.
        """

        self.players[self.curr_player_index].set_combo(combo, score)
