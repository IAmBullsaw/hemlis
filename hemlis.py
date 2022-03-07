import argparse
from sys import stderr
from os.path import isfile

charToMorse = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    'Å':'.--.-', 'Ä':'.-.-', 'Ö':'---.',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ',':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}


def get_args():
    """Return arguments passed to the script"""
    parser = argparse.ArgumentParser(prog='hemlis.py')
    parser.add_argument('message', type=str, help='message to encode, could be a file')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-d', '--decode', action='store_true', dest='decode',
                        help='if the message should be decoded')

    args = parser.parse_args()
    return args


def main(message: str, isDecode: bool):
    """prints the result from an encoding/decoding"""

    if isDecode:
        res = decode(message)
    else:
        res = encode(message.upper())

    print(res)


def toMorse(message: str) -> str:
    """encodes a message into morse code"""
    res = ''
    for c in message:
        if c == ' ':
            res += ' / '
        else: 
            res += charToMorse.get(c,'X')
            res += ' '
            if res[-2] == 'X':
                print( "# Warning: {} not correctly translated".format(c) ,file=stderr)

    return res


def fromMorse(message: str) -> str:
    """decodes morse code into a message"""
    morseToChar = {v: k for k,v in charToMorse.items()}
    morseToChar['/'] = ' '
    res = ''
    
    for c in message.split():
        res += morseToChar.get(c,'_')
        if res[-1] == '_':
            print("# Warning: {} not correctly translated".format(c),file=stderr)
    return res


def toWhitespace(message: str) -> str:
    """encodes morse code into whitespace characters
        starts with chr(82139) as a marker
    """
    return '{}'.format(chr(8239)) + message.translate(message.maketrans('.-/ ',' \t{}{}'.format(chr(160), chr(8194))))


def fromWhitespace(message: str) -> str:
    """decodes whitespace morse code into other notation"""
    return message.translate(message.maketrans(' \t{}{}{}'.format(chr(160), chr(8194), chr(8239)),'.-/  '))


def decode(message: str) -> str:
    """decodes a message from whitespace morse code"""
    res = fromWhitespace(message)
    res = fromMorse(res)
    return res


def encode(message: str) -> str:
    """encodes a message into morse code written in whitespace"""
    res = toMorse(message)
    res = toWhitespace(res)
    return res


def simpleTest(message):
    """basic test just to see it passes"""
    encodedMessage = toMorse(message)
    whitespace = toWhitespace(encodedMessage)
    decodedWhitespace = fromWhitespace(whitespace)
    decodedMessage = fromMorse(decodedWhitespace)
    
    print('# Encoded', encodedMessage == decodedWhitespace)
    print('# Success', message.upper() == decodedMessage)
    

if __name__ == '__main__':
    args = get_args()
    messages = []
    # find all messages in a file
    if isfile(args.message):
        with open(args.message,'r') as f:
            for line in f:
                # messages start with a chr(8239)
                if '{}'.format(chr(8239)) in line:
                    messages.append(line.split('{}'.format(chr(8239)))[1])
    else:
        messages.append(args.message)
    for message in messages:
        main(message, args.decode)
