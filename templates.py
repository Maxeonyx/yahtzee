HELP_TEXT = """
Type "help commands" for command help.
Type "help rules" for the rules of yahtzee.
The scoring rules are displayed on the scoreboard. Type "print" to show
the scoreboard.
"""

HELP_TEXT_RULES = """
A game of yahtzee is played by rolling five dice, and collecting combos.
At the start of each turn, a player rolls the dice. They can then choose which
dice to keep and which to reroll. Each player gets three rolls per turn.

After any roll, players can choose to collect a combo. For example, a player
has rolled these dice:

-----------  -----------  -----------  -----------  -----------
|  0   0  |  |  0   0  |  |  0   0  |  |  0   0  |  |  0   0  |
|    0    |  |    0    |  |  0   0  |  |  0   0  |  |  0   0  |
|  0   0  |  |  0   0  |  |  0   0  |  |  0   0  |  |  0   0  |
-----------  -----------  -----------  -----------  -----------

This roll has a pair of fives and a triple of sixes, so the following five
combos are valid:

Full House (always worth 25 points)
- Full House is valid for a roll that contains a PAIR and a TRIPLE

Three of a kind (worth 28 points, the sum of the dice in this roll)
- Three of a kind is valid for a roll that contains a TRIPLE

Sixes (worth 18 points, the sum of the sixes in this roll)
- Sixes is valid for any roll that contains a 6

Fives (worth 10 points, the sum of the fives in this roll)
- Fives is valid for any roll that contains a 5

Chance (worth 28 points, the sum of the dice in this roll)
- Chance is valid for ANY roll

A combo can only be collected ONCE.
If no combo can be collected, then you must BLOCK a combo.

The only exception is a Yahtzee, which can be collected multiple times unless
it is Blocked.

Type "help commands" to learn how to play.
"""

HELP_TEXT_COMMANDS = """
The commands are as follows:

    roll
        - Rolls all five dice. Generally the first command in a turn.


    keep (dice one) [dice two, dice three, ...]
        - Rolls some of the dice. Specify which ones to keep by entering the numbers
        of the dice. E.G. :

            keep 4 5 6

        Rolls the other two dice and keeps a Four, a Five and a Six.


    ANY COMBO COMMAND:

        - If the combo is valid for your roll, the game calculates the score and
        you collect the combo. That combo cannot be used again.
        The combo commands are lowercase with spaces removed:

        ones
        twos
        threes
        fours
        fives
        sixes
        threeofakind
        fourofakind
        fullhouse
        shortstraight
        longstraight
        yahtzee
        chance


    block (combo)
        - Blocks the specified combo. Used if your roll has no valid combos.


    print
    - Prints the scoreboard.


    save
    - Saves the game. Overwrites any other savegame.


    finish
    - Ends the game, summing the scores and displaying the final scoreboard.


    exit
    - Closes the game. Prompts to save the game.

    help [help type]
    - Displays the help for a specified topic.
"""

HELP_PARAMETERS = {
                   '' : HELP_TEXT,
                   'rules' : HELP_TEXT_RULES,
                   'commands' : HELP_TEXT_COMMANDS
                  }

DICE_ONE = """-----------
|         |
|    0    |
|         |
-----------"""
DICE_TWO = """-----------
|  0      |
|         |
|      0  |
-----------"""
DICE_THREE = """-----------
|  0      |
|    0    |
|      0  |
-----------"""
DICE_FOUR = """-----------
|  0   0  |
|         |
|  0   0  |
-----------"""
DICE_FIVE = """-----------
|  0   0  |
|    0    |
|  0   0  |
-----------"""
DICE_SIX = """-----------
|  0   0  |
|  0   0  |
|  0   0  |
-----------"""

DICE_DICT = {
             1 : DICE_ONE,
             2 : DICE_TWO,
             3 : DICE_THREE,
             4 : DICE_FOUR,
             5 : DICE_FIVE,
             6 : DICE_SIX
            }

UPPER_COMBO_COMMANDS = {
                        'ones',
                        'twos',
                        'threes',
                        'fours',
                        'fives',
                        'sixes'
                       }

LOWER_COMBO_COMMANDS = {
                        'threeofakind',
                        'fourofakind',
                        'fullhouse',
                        'shortstraight',
                        'longstraight',
                        'yahtzee',
                        'chance'
                       }

COMBO_COMMANDS = UPPER_COMBO_COMMANDS.union(LOWER_COMBO_COMMANDS)

OTHER_COMMANDS = {
            'save',
            'exit',
            'roll',
            'keep',
            'block',
            'finish',
            'print',
            'help'
           }

COMMANDS = OTHER_COMMANDS.union(COMBO_COMMANDS)

COMBO_OUTLINES = {
             'ones'             : '111**',
             'twos'             : '222**',
             'threes'           : '333**',
             'fours'            : '444**',
             'fives'            : '555**',
             'sixes'            : '666**',
             'threeofakind'     : 'aaa**',
             'fourofakind'      : 'aaaa*',
             'fullhouse'        : 'aaabb',
             'shortstraight'    : 'abcd*',
             'longstraight'     : 'abcde',
             'yahtzee'          : 'aaaaa',
             'chance'           : '*****'
            }

COMBO_INDICES = {
             'ones'             : 0,
             'twos'             : 1,
             'threes'           : 2,
             'fours'            : 3,
             'fives'            : 4,
             'sixes'            : 5,
             'threeofakind'     : 6,
             'fourofakind'      : 7,
             'fullhouse'        : 8,
             'shortstraight'    : 9,
             'longstraight'     : 10,
             'yahtzee'          : 11,
             'chance'           : 12
            }

SCOREBOARD = """-----------------|--------------|------------|------------|------------|------------|
Combo            | Score Type   | {:<10} | {:<10} | {:<10} | {:<10} |
-----------------|--------------|------------|------------|------------|------------|
#################|##############|############|############|############|############|
-----------------|--------------|------------|------------|------------|------------|
Upper Section - Sum dice of the specified type.
-----------------|--------------|------------|------------|------------|------------|
Ones             | Sum Ones     | {:>10} | {:>10} | {:>10} | {:>10} |
Twos             | Sum Twos     | {:>10} | {:>10} | {:>10} | {:>10} |
Threes           | Sum Threes   | {:>10} | {:>10} | {:>10} | {:>10} |
Fours            | Sum Fours    | {:>10} | {:>10} | {:>10} | {:>10} |
Fives            | Sum Fives    | {:>10} | {:>10} | {:>10} | {:>10} |
Sixes            | Sum Sixes    | {:>10} | {:>10} | {:>10} | {:>10} |
-----------------|--------------|------------|------------|------------|------------|
Subtotal         | Sum combos   | {:>10} | {:>10} | {:>10} | {:>10} |
-----------------|--------------|------------|------------|------------|------------|
Bonus - Add 35 points if Subtotal is 63 or more
-----------------|--------------|------------|------------|------------|------------|
Bonus            | 35 points    | {:>10} | {:>10} | {:>10} | {:>10} |
-----------------|--------------|------------|------------|------------|------------|
#################|##############|############|############|############|############|
-----------------|--------------|------------|------------|------------|------------|
Lower Section - Scoring varies between Combos
-----------------|--------------|------------|------------|------------|------------|
Three of a mind  | Sum all dice | {:>10} | {:>10} | {:>10} | {:>10} |
Four of a kind   | Sum all dice | {:>10} | {:>10} | {:>10} | {:>10} |
Full House       | 25 points    | {:>10} | {:>10} | {:>10} | {:>10} |
Short Straight   | 30 points    | {:>10} | {:>10} | {:>10} | {:>10} |
Long Straight    | 40 points    | {:>10} | {:>10} | {:>10} | {:>10} |
Yahtzee          | 50 points ea | {:>10} | {:>10} | {:>10} | {:>10} |
Chance           | Sum all dice | {:>10} | {:>10} | {:>10} | {:>10} |
-----------------|--------------|------------|------------|------------|------------|
Subtotal         | Sum combos   | {:>10} | {:>10} | {:>10} | {:>10} |
-----------------|--------------|------------|------------|------------|------------|
#################|##############|############|############|############|############|
-----------------|--------------|------------|------------|------------|------------|
Total            | Overall Sum  | {:>10} | {:>10} | {:>10} | {:>10} |
-----------------|--------------|------------|------------|------------|------------|
"""
