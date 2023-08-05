# Differentiate

Compare multiple data sets and retrieve the unique, non-repeated elements.

Package features:

* Retrieve unique elements
* Importable
* Command line callable

## Propose/Rational
Initially, differentiate was built in conjunction with a proprietary MySQL migration toolkit in order to compare query results and that the database/table was succesfully migrated.  Differentiate has become its own project due to the wide variety of potential use cases.

## Usage
Compare two data sets or more (text files or lists/sets) and return the unique elements that are found in only one data set.  Differentiate can be called from a command line interface or imported as a package.

### Import examples
```python
# Retreive  unique values from two flat lists.
from differentiate import diff


x = [0, 1, 2, 3, 4]
y = [3, 4, 5, 6, 7]

uniques = diff(x, y)
print(uniques)  # [0, 1, 2, 5, 6, 7]
```

```python
# Retrieve unique values from two nested lists.
from differentiate import diff


x = [[0, 1, 2, 3, 4],
     [5, 6, 7, 8, 9],
     [10, 11, 12, 13, 14]]
y = [[5, 6, 7, 8, 9],
     [10, 11, 12, 13, 14],
     [15, 16, 17, 18, 19]]

uniques = diff(x, y)
print(uniques)  # [[15, 16, 17, 18, 19], [0, 1, 2, 3, 4]]
```

### Command line example
```bash
>>> differ require1.txt require2.txt
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

In order to utilize this package/repository you will need to have a Python (only tested on 3.6+ as of now) interpreter installed on your machine.

#### PyPi installation
```
pip install differentiate
```

#### PyPi update
```
pip install --upgrade --no-cache-dir differentiate
```


### Project Structure

```
differentiate
├── __init__.py
├── _version.py
└── differentiate.py

```

## Contributing

Please read [CONTRIBUTING.md](https://github.com/mrstephenneal/differentiate/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/mrstephenneal/differentiate). 

## Authors

* **Stephen Neal** - *Initial work* - [synfo](https://github.com/mrstephenneal)

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details
