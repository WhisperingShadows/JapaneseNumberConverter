# The list containing the main numbers 0 - 9
kanji_numbers = ["",    # None 
                 "一",   # One
                 "二",   # Two
                 "三",   # Three
                 "四",   # Four
                 "五",   # Five
                 "六",   # Six
                 "七",   # Seven
                 "八",   # Eight
                 "九",   # Nine
                 "ゼロ", # Zero
                 ]

# The list containing bases for the main numbers
bases = ["",     # None
         "万",   # Ten thousand
         "億",   # Hundred million
         "兆",   # Trillion
         "京"    # Etc.
         ]

# The list containing prepositions to base numbers
prep = ["",      # None
        "十",    # Ten
        "百",    # Hundred
        "千",    # Thousand
        ]

# Debug switch
DEBUG = False

# Handles OutOfRangeException exceptions, not used in this version; deprecated
class OutOfRangeException(Exception):
    pass

# Main conversion function
def convert_to_japanese(n):
    """ Converts arabic numerals (i.e those comprised of the numbers 0 - 9) to
        Japanese numbers (ex. 267 would be に百六十七). This works by utilizing
        the repeating number base pattern found in the Japanese number system.
        This pattern can be represented by the following sequence: AX BX CX Y,
        where A, B, and C are the "prepositions" 十 (ten), 百 (hundred), and
        千 (thousand), and X and Y the current number bases which are all
        consecutive powers of ten (of difference 10^4, ex. 10^0, 10^4, 10^8,
        10^12, 10^16 ...). This can be more easily explained by the following:

                x
                十x	10
                百x	100
                千x	1,000
                万	10,000
                十万	100,000
                百万	1,000,000
                千万	10,000,000
                億	100,000,000
                十億	1,000,000,000
                百億	10,000,000,000
                千億	100,000,000,000
                兆	1,000,000,000,000
                十兆	10,000,000,000,000
                百兆	100,000,000,000,000
                千兆	1,000,000,000,000,000
                
        **Note: The x's above are not a part of the Japanese number system and
        are used here to represent the base 10^0, or 1, which has no affect on
        a number and is thus ommitted

        I guess what I'm trying to say is that Japanese uses a different
        counting system for large numbers than English. In English, numbers
        increase by thousands, so one thousand, one million, then one billion,
        a thousand times a million. Japanese is based on the Chinese system
        which is weird and uses ten thousand as its basic unit. A man (万) is
        ten thousand, and then an oku (億) is ten thousand times ten thousand,
        or a hundred million. Increasing again, a chou (兆) is ten thousand
        times an oku, or a trillion. 
        """

    # Sanitizes input by removing all commas and surrounding whitespace
    try:
        n = str(int(str(n).strip().replace(",", "")))
        if DEBUG:
            print("Number:", n)
    # Catches an exception if an improper input is given
    except:
        print("Unreadable input, please enter an integer")
        return None

    # The length of a number (each digit is another power of 10, hence the name)
    power = len(n)

    # Converts numbers to a list of digits
    digits = list(map(int, str(n)))

    #Debug code
    if DEBUG:
        print("Digits:", digits)

    # Initializes output variable 
    out = ""

    # Converts each power of ten within the given number individually
    for level in range(power, 0, -1):

        # The main number of each power, i.e numbers 1 - 9 (zero not included)
        main = kanji_numbers[digits[::-1][level-1]]

        # Checks for zeroes and proceeds as normal if none are detected
        if digits[::-1][level-1] != 0:
            
            # The preposition is the number by which the base is multiplied to
            # equal the power; changes every power of ten
            preposition = prep[(level % 4)-1]
            
            # The base is the number by which the preposition is multiplied to
            # equal the power; changes every four powers of ten
            base = bases[((level-1)//4)]
        # Handles zeroes
        else:
            # If the main number is a zero then that power is blank
            if power != 1:
                main = ""
                preposition = ""
                base = ""
            # Unless the number is one digit long, i.e it equals zero
            else:
                main = kanji_numbers[10]
                preposition = ""
                base = ""
        
        # Debug code
        if DEBUG:
            print("Level:", level,
                  "Main:", main,
                  "Pre:", preposition,
                  "Base:", base
                  )
        # Combines the current power with all previous powers
        out += str(main)+ preposition + base + " "

    # Returns the converted number
    return out

# Main function
if __name__ == "__main__":
    # Imports for random integers and command line interfacing
    from random import randint
    from sys import argv

    # Checks if there is a command line flag for the maximum number
    if len(argv) >= 2:
        try:
            MAX_NUM = int(argv[1])
        except ValueError:
            MAX_NUM = -1

        # A little edge case handling
        if MAX_NUM > 1000000000000:
            print("Impossible - this program doesn't",
                  "work with numbers over 1,000,000,000,000.")
            exit(1)

    else:
        # If a max wasn't given, defaults to 1000000000000
        MAX_NUM = 1000000000000

    # The input given by the user
    given = ""
    # Numbers done so far
    done_so_far = []
    # How many numbers have been done so far
    number_done = 0

    while True:
        n = randint(0, MAX_NUM)
        # If and as long as n has already been done, get a new number.
        # Only allowed for number sets under 100 due to potential memory issues.
        if MAX_NUM <= 100:
            while n in done_so_far:
                n = randint(0, MAX_NUM)

        # Asks for number translation
        try:
            given = input("What is {} in Arabic numerals? ".format(
                convert_to_japanese(n)))
        # Catches KeyboardInterrupt exception
        except KeyboardInterrupt:
            print("またね!")
            exit(1)
        # Catches EOFError exception
        except EOFError:
            print("またね!")
            exit(1)
        # Allows the user to exit the program by typing "quit"
        if given.lower().strip() == 'quit':
            print("またね!")
            exit(0)
        # Exits the program once every number has been done
        if number_done >= MAX_NUM:
            print("You did all the numbers in that set!　")
            exit(0)

        # Attempts to convert given answer to integer
        try:
            given_n = int(given)
        except ValueError:
            given_n = -1

        # Checks whether given value is correct and updates the number_done and
        # done_so_far variables accordingly
        if given_n == n:
            print("You got it!")
            done_so_far.append(n)
            number_done += 1
        else:
            print("No, that's not quite right. This is {}.".format(n))
