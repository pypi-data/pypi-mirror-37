# Installation

`pip install bamboo-lib`

## Additional Steps

If you will need to use the distributed locking functionality, you will need to install
some additional software. Below are the instructions for macOS

### Installing Sherlock on macOS.

```brew install libmemcached```

```pip install pylibmc --install-option="--with-libmemcached=/usr/local/Cellar/libmemcached/1.0.18_2"```

```pip install sherlock```

# Running tests

To run the tests, simply run:
`pytest`

Alternatively, if you would like to display all log/print statements run:
`pytest -s`
