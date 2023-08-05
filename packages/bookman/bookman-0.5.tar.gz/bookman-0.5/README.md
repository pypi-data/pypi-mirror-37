# bookman

bookman is a non-webapp, standalone bookmark managing software. It gives you the ability to store any link you want and open it instantly.


## Dependencies

* Python 3
* Python 3 - GTK3
* Python 3 - Yaml
* Python 3 - SQL Alchemy

## Building packages

To build bookman you will need:
* A private GPG-Key
* Make
* Python 3
* [stdeb](https://pypi.org/project/stdeb/)

### Building for Debian

```bash
make deb
```

### Building for Fedora/Redhat

```bash
make rpm
```

The package created stores everything under /usr/local. Therefore you might add
following to your ~/.bashrc file to actually use bookman:

```bash
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.5/dist-packages
```

## Author

Richard Baeck <richard.baeck@free-your-pc.com>

## License

MIT License
