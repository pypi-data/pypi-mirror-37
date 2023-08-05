# Config ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Config is a Python-based project for reading configurations from YAML files.

## Installation

### Requirements
- Python 2.7 and up
- pkg_resources
- pyYAML

```
$ pip install chance-config 
```

## Usage

```python
import chanconfig

# With package given
chanconfig.Config('test.yaml', 'foo.conf')

# With relative/absolute path
chanconfig.Config('foo/conf/test.yaml')

# With arguments and settings
# The priority is: Env > Args > Config files
# Settings should be a dict of key and env name, process method and default
# value. Notice that env name can be None adn process method should be callable. 
chanconfig.MultipleConfig(
    'test.yaml', 'foo.conf', {'test': 'test'}, {'test': ('TEST', int, 1)}
)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
