![Logo](resources/logo.png)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)

# Requirements

## MAC OS

### python 3

```bash
> brew install python3
```

### virtualenv
```bash
> sudo -H pip3 install virtualenv
``` 

### hub

```bash
> brew install hub
```

## environment variables
- Need to set an environment variable named CONFLUENCE_HOST with the value being the confluence host url


## Linux

### python 3
```bash
> sudo apt-get install python3
```

### pip

```bash
> sudo apt-get install python3-pip
```

### virtualenv
```bash
> sudo -H pip3 install virtualenv
```

### hub

Download a binary release from [https://github.com/github/hub/releases](https://github.com/github/hub/releases) and add /bin/hub to your PATH

or

```bash
# for hub version 2.4.0 & linux 64-bit
> wget https://github.com/github/hub/releases/download/v2.4.0/hub-linux-amd64-2.4.0.tgz -P /tmp/hub && cd /tmp/hub
> tar -xvzf hub-linux-*.tgz
# assuming that `/usr/local/bin` is in your PATH:
> sudo mv hub-linux-*/bin/hub /usr/local/bin
> rm -rf /tmp/hub
```

## environment variables
- Need to set an environment variable named CONFLUENCE_HOST with the value being the confluence host url

# Run

```bash
> git clone https://github.com/westwater/mtd-whitelisting.git
> cd mtd-whitelisting
> ./run.sh [options]
```

> ##### Note
>
> when running for the first time you will be asked for the following:
> - your confluence credentials
> - your github credentials

## options
```
(-t|--test) - stubs writes to git and confluence
(-d|--debug) - prints out key information for debugging
```

# Test
```bash
> tox
```

> ##### Note
>
> if using pyenv you will need to load multiple versions to test against both 3.5 and 2.7
>
>       > pyenv global 3.5.0 2.7.6