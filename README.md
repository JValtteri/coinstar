# coinstar
A program to analyse bitcoin market value for a given date range

## Setup ##

### Make sure you have [***Python 3.6***](https://www.python.org/downloads/) or newer Installed ###

**Windows**
```
python3
```

**Linux**
```
$ apt-get install python3
```

### Install requirements ###

**Windows**
```
install.bat
```

**Linux**
```
$ install.sh
```

## Use in CLI ##

```
coinstar.py <opts>

  -s    --start  <start date> YYYY.MM.DD
  -e    --end    <end date>   YYYY.MM.DD
  -r    --raw                 Show raw data
  -h    --help                Show this help
```

For example:
```
coinstar.py -s 2021.01.01 -e 2021.01.31
```
