def is_digits(text):
    for x in text:
        if x != ' ':
            if not x.isdigit():
                return 'error'
    return 'no_error'
