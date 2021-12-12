# coinstar
A program to analyse bitcoin market value for a given date range.

It shows:
- Longest **bearish trend** within a *given date range*
- Date within a *given date range* with the **highest trading volume**
- The **best day** for **buying**, *and* the **best day** for **selling** the bought coin to ***maximize profits***.

## Dependencies ##
- [Python3](https://www.python.org/)
- [Requests: HTTP for Humans](https://docs.python-requests.org/en/master/)
- [CoinGecko HTTP API](https://www.coingecko.com/en/api/documentation).

## Full Setup ##

Original, platform independent Python program with both CLI and GUI options.

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
python3 coinstar.py -s <start date> -e <end date> <options>

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
python3 coinstar.py -s 2021.01.01 -e 2021.01.31
```

## Use in GUI ##

1. *A*) Run ```python3 coinstar.py``` with the ```-g``` or ```--gui``` flag
 
  **-- or --**

1. *B*) Run ```python3 gui.py```

2. Enter **start** and **end dates** in their respective fields
3. press **GET**

## Setup GUI only (Windows) ##

- [Download standalone Windows excecutible](https://www.dropbox.com/s/ou1eq90230b5qng/coinstar_gui.zip?dl=0)
- Extract the zip file and 
- run **coinstart_gui.exe**.

## GUI only features ##

**GUI only** **does** have features to show:
- Longest **bearish trend** within a *given date range*
- Date within a *given date range* with the **highest trading volume**
- The **best day** for **buying**, *and* the **best day** for **selling** the bought coin to ***maximize profits***.

**GUI only** setup does **not** have options to show:
- raw data
- formatted data points
- data per day

