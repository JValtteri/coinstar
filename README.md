# coinstar
A program to analyse bitcoin market value for a given date range.

## Dependencies ##
- [Python3](https://www.python.org/)
- [Requests: HTTP for Humans](https://docs.python-requests.org/en/master/)
- [CoinGecko HTTP API](https://www.coingecko.com/en/api/documentation).

## Setup ##

### Make sure you have [***Python 3.6***](https://www.python.org/downloads/) or newer Installed ###

**Windows:**
```
python3
```

**Linux:**
```
$ apt-get install python3
```

### Install requirements ###

**Windows:**
```
install.bat
```

**Linux:**
```
$ install.sh
```

**Manual:**
```
sudo apt-get -y install python3-pip
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## Use in CLI ##

```
coinstar.py -s <start date> -e <end date> <options>

  -s    --start  <start date> YYYY.MM.DD
  -e    --end    <end date>   YYYY.MM.DD
  -r    --raw                 Show raw data
  -f    --format              Show formatted datapoints
  -d    --days                Show day values:
                              Open, Close, Volume, Bearish
  -h    --help                Show this help
```

For example:
```
coinstar.py -s 2021.01.01 -e 2021.01.31
```
