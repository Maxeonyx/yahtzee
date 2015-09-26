"""
The player class for the Yahtzee game.

A player holds all of the scores and rolls a player has made so far.

"""


import templates

class Player:
    """
    A player is mainly a wrapper for the score data for a specific player.

    public fields:
        - name : string
        - bonus : int
        - total : int
        - upper_subtotal : int
        - lower_subtotal : int

    public methods:
        - check_if_combo_used : boolean
        - get_all_categories : list
        - sum_sections : None
    """


    def __init__(self, name):
        """
        Initialise a new player instance. Takes the player's name.

        There is no implementation to initialise a player with score. Use the
        scoreboard to do so.
        """
        self.name = name
        self.combos = [0]*13
        self.upper_subtotal = 0
        self.lower_subtotal = 0
        self.bonus = 0
        self.total = 0

    def check_if_combo_used(self, combo_name):
        """
        Takes a VALID combo name and returns a boolean, false if the
        player has used that combo, and true otherwise.
        """

        combo_index = templates.COMBO_INDICES[combo_name]

        if self.combos[combo_index] != 0 and combo_name != "yahtzee":
            return False

        if self.combos[combo_index] == "Blocked":
            return False

        return True


    def set_combo(self, combo_name, score):
        """
        Takes a VALID combo name and a score for that combo, and adds it to
        the player's record.

        This will print status messages to the screen.
        """

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
        """
        Returns the player's total for the upper section of the scoreboard.
        (ones to sixes)
        """

        total = 0
        for val in self.combos[:6]:
            if val != "Blocked":
                total += val
        return total


    def get_lower_subtotal(self):
        """
        Returns the player's total for the lower section of the scoreboard.
        (threeofakind to chance)
        """
        total = 0
        for val in self.combos[6:]:
            if val != "Blocked":
                total += val
        return total


    def get_bonus(self):
        """
        Returns an integer, the value of the player's bonus for the upper
        section.

        35 if the player has 63 or more points in the upper section, else 0
        """

        if self.get_upper_subtotal() > 62:
            return 35

        return 0


    def get_total(self):
        """
        returns the player's total score.
        """

        total = self.get_upper_subtotal() + self.get_lower_subtotal() + self.get_bonus()
        return total

    def sum_sections(self):
        """
        sums the player's score.

        This should not be called until the game ends
        """
        self.upper_subtotal = self.get_upper_subtotal()
        self.bonus = self.get_bonus()
        self.lower_subtotal = self.get_lower_subtotal()
        self.total = self.get_total()

    def get_all_categories(self):
        """
        returns a list of the player's scores, to be given to the scoreboard.

        this does not sum the scores to give the subtotals, totals and bonus.

        The structure of the resulting list is as follows:
        INDEX   | VALUE
        0       : name
        1 - 6   : ones - sixes
        7       : upper_subtotal
        8       : bonus
        9       : threeofakind
        10      : fourofakind
        11      : fullhouse
        12      : shortstraight
        13      : longstraight
        14      : yahtzee
        15      : chance
        16      : lower_subtotal
        17      : total
        """

        all_categories = []

        all_categories += [self.name]
        all_categories += self.combos[:6]
        all_categories += [self.upper_subtotal]
        all_categories += [self.bonus]
        all_categories += self.combos[6:]
        all_categories += [self.lower_subtotal]
        all_categories += [self.total]

        return all_categories
