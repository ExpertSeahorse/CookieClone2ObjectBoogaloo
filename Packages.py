import re
import pandas
from smtplib import SMTP
# 07/16/2019


def float_input():
    type_match = False
    while not type_match:
        try:
            strin = float(input())
        except ValueError:
            print("Please enter a valid float")
        else:
            type_match = True
    return strin


def int_input():
    type_match = False
    while not type_match:
        try:
            strin = int(input())
        except ValueError:
            print("Please enter a valid int")
        else:
            type_match = True
    return strin


def expression_converter(expr):
    """
    Replaces #(, )#, #x, x#, and ^ with the equivalent in python
    :param expr:
    :return:
    """
    expr = str(expr)
    mult_err_code = re.compile(r'\w\(|\)\w|\w[a-z]|[a-z]\d')

    # if the entry is only 1 character long...
    if not (len(expr) - 1):
        # there can't be an error with only one number
        return expr

    # check through every char in the entry...
    for i in range(len(expr) - 1):
        # if between two characters...
        eqw = expr[i] + expr[i + 1]
        # there is one of the errors listed in the err_list...
        if mult_err_code.match(eqw):
            # Add a multiplication symbol to fix the offence
            expr = expr[:i + 1] + "*" + expr[i + 1:]

    # And add the fixed entry to this new list and replaces all of the '^'s with '**'s
    return expr.replace('^', '**')


def database(arr, titles=False):
    """
    Creates a Pandas Database for use in graphing; akin to the stats button on a TI-84 Calculator
    Also used to transform an array into a DB for graphing
    :param arr:
    :param titles:
    :return:
    """
    if not titles:
        if isinstance(arr[0], list) or isinstance(arr[0], tuple):
            if len(arr) == 2:
                indx = ["x", "y"]
            elif len(arr) == 3:
                indx = ["x", "y", "z"]
            else:
                indx = range(1, len(arr) + 1)
            cols = range(1, len(arr[0])+1)

        elif isinstance(arr[0], float):
            indx = ["y"]
            cols = range(1, len(arr)+1)

        else:
            indx = range(1, len(arr) + 1)
            cols = range(1, len(arr[0])+1)
    else:
        indx = titles
        cols = range(1, len(arr[0]) + 1)

    return pandas.DataFrame(arr, index=indx, columns=cols).T


def time_delta_display(sec):
    """
    Converts a number of seconds into a string of how many weeks, days, etc it represents
    :param sec:
    :return:
    """
    # Conversion key
    intervals = (('years', 31536000),   # 60 * 60 * 24 * 365
                 ('months', 2628288),   # 60 * 60 * 24 * 30.42     (30.42 is the avg number of days in a month)
                 ('weeks', 604800),     # 60 * 60 * 24 * 7
                 ('days', 86400),       # 60 * 60 * 24
                 ('hours', 3600),       # 60 * 60
                 ('minutes', 60),
                 ('seconds', 1),)
    result = []
    # For each of the above categories...
    for name, count in intervals:
        # Divide the input number of seconds by the counter from the list
        value = sec // count
        # If that value is > 0...
        if value:
            # Subtract the whole number amount from the inputted number (we use the remainder in later iterations)
            sec -= value * count
            # If there is only 1 instance of the unit (1 week, 1 hour, ...)...
            if value == 1:
                # Remove the 's' from the displayed name
                name = name.rstrip('s')
            # Add the unit and amount to an array
            result.append("{} {}".format(value, name))
    # Return the array as a string
    return ', '.join(result)


def display_num(num):
    """
    Formats numbers to use the format ###.## <Name> after 1,000,000 > 1.00 million
    :param num:
    :return:
    """
    if 1 <= num / (1*10**3) < 1000:
        str_num = str(round(num, 2))
        r_str_num = str_num[::-1]
        if '.' in r_str_num:
            start_position = r_str_num.index(".")
        else:
            start_position = -1
        o = r_str_num[:start_position + 4] + "," + r_str_num[start_position + 4:]
        return o[::-1]

    elif 1 <= num / (1*10**6) < 1000:
        return str(round(num/(1*10**6), 2)) + " million"

    elif 1 <= num / (1*10**9) < 1000:
        return str(round(num/(1*10**9), 2)) + " billion"

    elif 1 <= num / (1*10**12) < 1000:
        return str(round(num/(1*10**12), 2)) + " trillion"

    elif 1 <= num / (1*10**15) < 1000:
        return str(round(num/(1*10**15), 2)) + " quadrillion"

    elif 1 <= num / (1*10**18) < 1000:
        return str(round(num/(1*10**18), 2)) + " quintillion"

    elif 1 <= num / (1*10**21) < 1000:
        return str(round(num/(1*10**21), 2)) + " sextillion"

    else:
        return str(num)


def send_sms(message):
    carriers = {'att': '@mms.att.net',
                'tmobile': '@tmomail.net',
                'verizon': '@vtext.com',
                'sprint': '@page.nextel.com'}

    # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = '000-000-0000{}'.format(carriers['att'])
    auth = ('**email**', '**password**')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, message)

    """
    import SMS

    some_text = 'Blah, blah'

    SMS.send(some_text)
    """
