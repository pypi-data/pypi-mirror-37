def diff(x, y, x_only=False, y_only=False):
    """
    Retrieve a unique of list of elements that do not exist in both x and y.
    Capable of parsing one-dimensional (flat) and two-dimensional (lists of lists) lists.

    :param x: list #1
    :param y: list #2
    :param x_only: Return only unique values from x
    :param y_only: Return only unique values from y
    :return: list of unique values
    """
    # Validate both lists, confirm neither are empty
    if len(x) == 0 and len(y) > 0:
        return y  # All y values are unique if x is empty
    elif len(y) == 0 and len(x) > 0:
        return x  # All x values are unique if y is empty
    elif len(y) == 0 and len(x) == 0:
        return []

    # Convert dictionaries to lists of tuples
    if isinstance(x, dict):
        x = list(x.items())
    if isinstance(y, dict):
        y = list(y.items())

    # Get the input type to convert back to before return
    try:
        input_type = type(x[0])
    except IndexError:
        input_type = type(y[0])

    # Dealing with a 2D dataset (list of lists)
    if input_type not in (str, int, float):
        # Immutable and Unique - Convert list of tuples into set of tuples
        first_set = set(map(tuple, x))
        secnd_set = set(map(tuple, y))

    # Dealing with a 1D dataset (list of items)
    else:
        # Unique values only
        first_set = set(x)
        secnd_set = set(y)

    # Determine which list is longest
    longest = first_set if len(first_set) > len(secnd_set) else secnd_set
    shortest = secnd_set if len(first_set) > len(secnd_set) else first_set

    # Generate set of non-shared values and return list of values in original type
    uniques = {i for i in longest if i not in shortest}
    # Add unique elements from shorter list
    for i in shortest:
        if i not in longest:
            uniques.add(i)

    # Return unique values from x, y or both
    if x_only:
        return [input_type(i) for i in uniques if i in x]
    elif y_only:
        return [input_type(i) for i in uniques if i in y]
    else:
        return [input_type(i) for i in uniques]


def differentiate(x, y):
    """Wrapper function for legacy imports of differentiate."""
    return diff(x, y)


def main():
    from argparse import ArgumentParser

    # Declare argparse argument descriptions
    usage = 'Compare two files text files and retrieve unique values'
    description = 'Compare two data sets or more (text files or lists/sets) and return the unique elements that are ' \
                  'found in only one data set.'
    helpers = {
        'files': "Input two text file paths",
    }

    # construct the argument parse and parse the arguments
    ap = ArgumentParser(usage=usage, description=description)
    ap.add_argument('files', help=helpers['files'], nargs='+')
    args = vars(ap.parse_args())

    data = []
    # Read each text file
    for tf in args['files']:
        with open(tf, 'r') as f:
            # Remove whitespace and \n
            data.append([l.strip() for l in f.readlines()])

    # Run differentiate
    d = diff(data[0], data[1])
    print('\nUnique Items ({}):\n-------------------'.format(len(d)))
    for i in d:
        print(i)


if __name__ == '__main__':
    main()
