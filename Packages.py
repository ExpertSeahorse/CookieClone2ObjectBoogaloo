import re
import pandas
from smtplib import SMTP


# 07/28/2019


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
            cols = range(1, len(arr[0]) + 1)

        elif isinstance(arr[0], float):
            indx = ["y"]
            cols = range(1, len(arr) + 1)

        else:
            indx = range(1, len(arr) + 1)
            cols = range(1, len(arr[0]) + 1)
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
    intervals = (('years', 31536000),  # 60 * 60 * 24 * 365
                 ('months', 2628288),  # 60 * 60 * 24 * 30.42     (30.42 is the avg number of days in a month)
                 ('weeks', 604800),  # 60 * 60 * 24 * 7
                 ('days', 86400),  # 60 * 60 * 24
                 ('hours', 3600),  # 60 * 60
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
    name_bank = ['million',
                 'billion',
                 'trillion',
                 'quadrillion',
                 'quintillion',
                 'sextillion',
                 'septillion',
                 'octillion',
                 'nonillion',
                 'decillion',
                 'undecillion',
                 'duodecillion',
                 'tredecillion']

    # if the number is in the thousands...
    if 1 <= num / (1 * 10 ** 3) < 1000:

        # The num is converted to a string and rounded to the .01
        str_num = str(round(num, 2))
        # The string is reversed
        r_str_num = str_num[::-1]

        # If the number was has a decimal...
        if '.' in r_str_num:
            # Start from the decimal when counting for the comma
            start_position = r_str_num.index(".")
        else:
            # Otherwise start from -1 (Needed later)
            start_position = -1

        # The new number is the last 3 digits (starting from -1) then a comma then the rest of the number
        o = r_str_num[:start_position + 4] + "," + r_str_num[start_position + 4:]
        # Unreverse the number and return it
        return o[::-1]

    # If the string is in the millions +...
    else:
        for i, word in name_bank:
            # The power associated with the word is: ex. trillion == 1*10**12
            power = 6 + (3 * i)
            # if the number falls within the power for the word...
            if 1 <= num / 1*10**power < 1000:
                # Return the number rounded to the .01 and the word (ex. 1,550,000,000 == 1.55 billion)
                return str(round(num / (1 * 10 ** power), 2)) + " " + word

        # If the number hasn't been added yet, return it as a string
        return str(num)


def undisplay_num(num):
    """
    Unformats a number created by display num
    :type num: str
    :param num:
    :return:
    """
    num = num.lower()
    name_bank = ['million',
                 'billion',
                 'trillion',
                 'quadrillion',
                 'quintillion',
                 'sextillion',
                 'septillion',
                 'octillion',
                 'nonillion',
                 'decillion',
                 'undecillion',
                 'duodecillion',
                 'tredecillion']
    # If the number has a comma in it... (ex. 1,000)
    if ',' in num:
        # Remove the comma and return it as a float
        return float(num.replace(',', '').strip())

    else:
        for i, word in enumerate(name_bank):
            # if the word is in the number...
            if ' ' + word in num:
                # Return the number * 10**word (ex. 1.55 trillion == 1.55 * 10**12)
                return float(num.replace(word, '').strip()) * 10**(6 + (3*i))

        # If the number hasn't been added, try to return as a float
        return float(num)


def float_extract(s):
    """
    Gets all numbers from a string, including only decimals in the number, not at the end of words
    :param s:
    :return:
    """
    l = []
    in_num = False
    # For every character in the string...
    for i, char in enumerate(s):

        # If the char is the first digit in a number, add it and start considering the string like a number
        if char.isdigit():
            l.append(char)
            in_num = True

        # Add the . if in a current number
        elif in_num and char == '.':
            l.append(char)

        # If the character is not a . not a digit and at the end of a current number, end the number
        elif char != '.' and not char.isdigit() and in_num:
            in_num = False

            # If the sentence ended with the number, remove the last period
            if char == ' ' and s[i-1] == '.':
                l.pop()
    # Return the float of the collected digits put together
    return float(''.join(l))


def send_sms(message, number='813-352-2669', carrier='verizon'):
    # Cannot send non alphanumeric characters (ex. ":)")
    # TODO: Upgrade with Gmail API
    carriers = {'att': '@mms.att.net',
                'tmobile': '@tmomail.net',  # Not working , blocking MX, DNS mismatch
                'verizon': '@vtext.com',  # Working
                'sprint': '@messaging.sprintpcs.com',  # Working
                'at&t': '@txt.att.net',
                'boost': '@myboostmobile.com',
                'cricket': '@sms.mycricket.com',
                'metropcs': '@mymetropcs.com',
                'tracfone': '@mmst5.tracfone.com',
                'uscell': '@email.uscc.net',
                'virgin': '@vmobl.com'}
    # BUILD THE MESSAGE
    # Removes all formatting from the phone number
    number = number.replace('-', '').replace('(', '').replace(')', '')
    # Adds the carrier extention to the phone number
    to_number = number + '{}'.format(carriers[carrier])
    # Sets the id and password to the email acct
    auth = ('dfeldmansfakeemail@gmail.com', privacy_decoder('ÜÐÚÚÜÓºâÊíâå', "password"))
    # Refuses the message if the length is too long
    if len(message) > 128:
        print("Message too long (>128)")
        return "Message too long (>128)"

    # SEND THE MESSAGE
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
    # Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, message)
    server.quit()
    print("Sent SMS")
    """
    import Package

    some_text = 'Blah, blah'

    Package.send(some_text, number, carrier)

    find any number's carrier using https://freecarrierlookup.com/
    """
    return "Sent SMS"


def send_email(message, address='dtfeldman@verizon.net'):
    # login to the gmail acct
    auth = ('dfeldmansfakeemail@gmail.com', privacy_decoder('ÜÐÚÚÜÓºâÊíâå', "password"))

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    # server.sendmail(auth[0], to_number, message)
    server.sendmail(auth[0], address, message)
    server.quit()


def privacy_encoder(message, key):
    encoded_chars = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(message[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    return "".join(encoded_chars)


def privacy_decoder(encoded_message, key):
    decoded_chars = []
    for i in range(len(encoded_message)):
        key_c = key[i % len(key)]
        decoded_c = chr(ord(encoded_message[i]) - ord(key_c) % 256)
        decoded_chars.append(decoded_c)
    return ''.join(decoded_chars)


def string_chunker(strin, char_num):
    return [strin[i:i + char_num] for i in range(0, len(strin), char_num)]


if __name__ == '__main__':
    print(undisplay_num('1 million'))
    """
    for x in dns.resolver.query('gmail.com', 'MX'):
        print(x.to_text())
    """
