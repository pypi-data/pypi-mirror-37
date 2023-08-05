def is_palindrome(arg):
    """A palindrome is a word, number, phrase,
    or other sequence of characters which reads
    the same backward as forward (from Wikipedia).

    Args:
        arg (int or str): what we are testing as a palindrome
            If arg is an integer, it will be interpreted as a decimal number.

    Returns:
        bool: True if arg is a palindrome, false otherwise

    Raises:
        TypeError: If arg is not int or str
    """

    if type(arg) == int:
        return is_palindrome(str(arg))
    elif type(arg) == str:
        if arg[::-1] == arg:
            return True
        else:
            return False
    else:
        raise TypeError('Arg should be int or str, not {}'.format(type(arg)))
