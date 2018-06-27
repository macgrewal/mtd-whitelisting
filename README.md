![Logo](resources/logo.png)

# Requirements

## python 3

**MAC OS**
```bash
> brew install python3
```

**Linux**
```bash
> sudo apt-get install python3
```

## pip

**MAC OS**

installed with python3

**Linux**
```bash
> sudo apt-get install python3-pip
```

## virtualenv
```bash
> sudo -H pip3 install virtualenv
``` 

## hub

**MAC OS**
```bash
> brew install hub
```

**Linux**

Download a binary release from [https://github.com/github/hub/releases](https://github.com/github/hub/releases) and add /bin/hub to your PATH

or 

```bash
# for hub version 2.4.0 & linux 64-bit 
> wget https://github.com/github/hub/releases/download/v2.4.0/hub-linux-amd64-2.4.0.tgz -P /tmp/hub && cd /tmp/hub
> tar -xvzf hub-linux-*.tgz
# assuming that `~/bin` is in your PATH:
> sudo mv hub-linux-*/bin/hub ~/bin
> rm -rf /tmp/hub
```

# Run

```bash
> git clone https://github.com/westwater/mtd-whitelisting.git
> cd mtd-whitelisting
> ./run.sh
```