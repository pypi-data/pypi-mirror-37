class Differentiate:
    def __init__(self, x, y):
        """
        Retrieve a unique of list of elements that do not exist in both x and y.
        Capable of parsing one-dimensional (flat) and two-dimensional (lists of lists) lists.

        :param x: list #1
        :param y: list #2
        :return: list of unique values
        """
        self._x = x
        self._y = y
        self._input_type = None
        self._uniques = self._get_uniques(x, y)

    @property
    def uniques(self):
        """Retrieve unique values found in only X or only Y but not both."""
        return self._uniques

    @property
    def duplicates(self):
        """Retrieve non-unique values found in both X and Y."""
        return self._get_duplicates()

    @property
    def uniques_x(self):
        """Retrieve unique values found in sequence X."""
        return self._get_uniques_single(self._x)

    @property
    def uniques_y(self):
        """Retrieve unique values found in sequence Y."""
        return self._get_uniques_single(self._y)

    def _transform(self, x, y):
        """Transform a data sequence into a set of unique, immutable values for comparison."""
        _x = x
        _y = y

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
        if all(isinstance(i, dict) for i in [_x, _y]):
            self._input_type = dict
        else:
            try:
                self._input_type = type(x[0])
            except IndexError:
                self._input_type = type(y[0])

        # Dealing with a 2D dataset (list of lists)
        if self._input_type not in (str, int, float):
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
        return longest, shortest

    def _get_uniques(self, x, y):
        """Get unique values existing in only X or Y."""
        longest, shortest = self._transform(x, y)

        # Generate set of non-shared values and return list of values in original type
        uniques = {i for i in longest if i not in shortest}

        # Add unique elements from shorter list
        for i in shortest:
            if i not in longest:
                uniques.add(i)
        return uniques

    def _get_uniques_single(self, data_set):
        """Get unique values existing in only one of the data sets."""
        if self._input_type is dict:
            return [i for i in self._input_type(self.uniques) if i in data_set]
        else:
            return [self._input_type(i) for i in self.uniques if self._input_type(i) in data_set]

    def _get_duplicates(self):
        """Get repeated values found in both X and Y."""
        if self._input_type is dict:
            longest, shortest = self._transform(self._x, self._y)
            longest, shortest = self._input_type(longest), self._input_type(shortest)
        else:
            longest, shortest = self._transform(self._x, self._y)

        # Generate set of non-shared values and return list of values in original type
        duplicates = {i for i in longest if i in shortest}

        # Add unique elements from shorter list
        for i in shortest:
            if i in longest:
                duplicates.add(i)
        return duplicates


def diff(x, y, x_only=False, y_only=False, duplicates=False):
    d = Differentiate(x, y)

    # Return unique values from x, y or both
    if x_only:
        return d.uniques_x
    elif y_only:
        return d.uniques_y
    elif duplicates:
        return d.duplicates
    else:
        return d.uniques


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