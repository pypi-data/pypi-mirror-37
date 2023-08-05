char2morse = {
            'A': (False, True),
            'B': (True, False, False, False),
            'C': (True, False, True, False),
            'D': (True, False, False),
            'E': (False,),
            'F': (False, False, True, False),
            'G': (True, True, False),
            'H': (False, False, False, False),
            'I': (False, False),
            'J': (False, True, True, True),
            'K': (True, False, True),
            'L': (False, True, False, False),
            'M': (True, True),
            'N': (True, False),
            'O': (True, True, True),
            'P': (False, True, True, False),
            'Q': (True, True, False, True),
            'R': (False, True, False),
            'S': (False, False, False),
            'T': (True,),
            'U': (False, False, True),
            'V': (False, False, False, True),
            'W': (False, True, True),
            'X': (True, False, False, True),
            'Y': (True, False, True, True),
            'Z': (True, True, False, False),

            '1': (False, True, True, True, True),
            '2': (False, False, True, True, True),
            '3': (False, False, False, True, True),
            '4': (False, False, False, False, True),
            '5': (False, False, False, False, False),
            '6': (True, False, False, False, False),
            '7': (True, True, False, False, False),
            '8': (True, True, True, False, False),
            '9': (True, True, True, True, False),
            '0': (True, True, True, True, True)
        }

morse2char = {
            (False, True): 'A',
            (True, False, False, False): 'B',
            (True, False, True, False): 'C',
            (True, False, False): 'D',
            (False,): 'E',
            (False, False, True, False): 'F',
            (True, True, False): 'G',
            (False, False, False, False): 'H',
            (False, False): 'I',
            (False, True, True, True): 'J',
            (True, False, True): 'K',
            (False, True, False, False): 'L',
            (True, True): 'M',
            (True, False): 'N',
            (True, True, True): 'O',
            (False, True, True, False): 'P',
            (True, True, False, True): 'Q',
            (False, True, False): 'R',
            (False, False, False): 'S',
            (True,): 'T',
            (False, False, True): 'U',
            (False, False, False, True): 'V',
            (False, True, True): 'W',
            (True, False, False, True): 'X',
            (True, False, True, True): 'Y',
            (True, True, False, False): 'Z',
            (False, True, True, True, True): '1',
            (False, False, True, True, True): '2',
            (False, False, False, True, True): '3',
            (False, False, False, False, True): '4',
            (False, False, False, False, False): '5',
            (True, False, False, False, False): '6',
            (True, True, False, False, False): '7',
            (True, True, True, False, False): '8',
            (True, True, True, True, False): '9',
            (True, True, True, True, True): '0',
        }

def encode(txt, dot='.', line='_', delimiter='/'):
    """Encodes the given text in morse.
    Uses the given characters or . , - , and /
    
    raises ValueError if the strings passed as a parameter is not valid to be encoded as morse
    raises TypeError if the given parameters is not a string"""

    for parameter in (txt, dot, line, delimiter):
        if not type(parameter) == str:
            raise TypeError('Type str excepted as parameter, got {}'.format(type(parameter)))

    txt = txt.upper() #Let's take care of capitals here.

    output = ''
    
    for char in txt:
        seq = char2morse.get(char)

        if char == ' ':
            output += delimiter * 2
        elif char == '.':
            output += delimiter*3
        else:
            if not char:
                raise ValueError("Character '{}' cannot be encoded as morse".format(char))
            for bit in seq:
                if bit:
                    output += line
                else:
                    output += dot
            output += delimiter

    return output

def encode2bool(txt, endletter=3, endword=7):
    """Encodes the given text in morse using booleans.
    Returns a tuple, where False means not transmitting for one period and True transmitting for one
    
    raises ValueError if the strings passed as a parameter is not valid to be encoded as morse
    raises TypeError if the given parameters is not a string"""

    for parameter in (endletter, endword):
        if not type(parameter) == int:
            raise TypeError('Type int excepted as parameter, got {}'.format(type(parameter)))

    if type(txt) != str:
        raise TypeError('Type str excepted as parameter, got {}'.format(type(txt)))

    txt = txt.upper() #Let's take care of capitals here.

    output = []
    
    for char in txt:

        if char == ' ':
            output.extend((False,)*endword)
        else:
            seq = char2morse.get(char)

            if not char:
                raise ValueError("Character '{}' cannot be encoded as morse".format(char))
            for bit in seq:
                if bit:
                    output.extend((True,)*3)
                else:
                    output.append(True)
                output.append(False)
            output.extend((False,)*endletter)

    return tuple(output)


def decodefrombool(seq):
    out = ''
    for letter in seq:
        if letter == ():
            out.append(' ')
        else:
            char = morse2char.get(letter)
            if char == None:
                raise ValueError('Invalid morse sequence: {}'.format(letter))
            out.append(char)


def decode2bool(txt, lines=('-', '_'), dots=('.',), endletter=('/', ' '), endword=('\n'), ignore=False):
    seq = []
    letter = []
    for char in txt:
        if char in lines:
            letter.append(True)
        elif char in dots:
            letter.append(False)
        elif char in endletter:
            if letter == []:
                seq.append(())
            else:
                seq.append(tuple(letter))
                letter = []
        elif not ignore:
            raise ValueError('char {} cannot be decoded as morse.'.format(char))
    return tuple(seq)


def decode(txt):
    return decodefrombool(decode2bool(txt))
