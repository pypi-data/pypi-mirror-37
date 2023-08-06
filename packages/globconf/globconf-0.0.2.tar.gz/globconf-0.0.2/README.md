# globconf

Creates a global configparser object, regardless of the project and module in need of it

## Getting Started
In project using globconf:
```
from globconf import config
# config will attempt to read local config.ini file if present - required options are verified using.
from globconf import verify_required_options
cfg = verify_required_options('Section name', ['list', 'of', 'required', 'options', 'for', 'the', 'section'])
 
# if config.ini is not found, then defaults can be read from a string, within the module relying on globconf like so:
if 'Section name' not in config.sections():
    config.read_string("""
    [important section]
    host = critical-system.com
    user = REST_USER
    pwd = REST_PASSWORD
    verify_ssl = false
    """)
# or 
config.read('some_other_config.ini')
```

In modules:
```
from globconf import config, verify_required_options
class module(object):
    def __init__(self):
        sec = 'service now'
        self.cfg = verify_required_options(sec, ['host', 'user', 'pwd'])
        if not self.cfg.getboolean('verify_ssl', fallback=True):
            import urllib3
            urllib3.disable_warnings(InsecureRequestWarning)
```

And your module is happy as long as someone has initialised the needed section in the global config.

### Prerequisites

configparser


### Building
Build:
```
sudo python setup.py sdist bdist_wheel
twine upload dist/*
```



End with an example of getting some data out of the system or using it for a little demo

## Authors

* **Steffen Schumacher** - *Initial work* - [steffenschumacher](https://github.com/steffenschumacher)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
