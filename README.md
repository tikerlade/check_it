# Check updates of websites with `check_it` :sparkles:
Python script which will check update of websites for you.
![pic](pics/img.png)

## Installation
```shell
git clone https://github.com/tikerlade/check_it.git
cd check_it
pip install -r requirements.txt
```

## Usage
You have two options:
1. You can modify `config.yaml`
2. Set parameters in CLI


In `1` case, before running you need to specify data in `config.yaml`:
```yaml
urls: [https://bit.ly/3PYpifA,
       https://bit.ly/3P0YNFe,
       https://bit.ly/3QajC2e,
       https://abit.itmo.ru/rating/master/budget/15840,
       https://abit.itmo.ru/rating/master/budget/15845]
request_int: 1
symbols_diff: 0
str_to_find: "166*183*422*74"
```

and after thath you could run script as:
```shell
python3 check_it.py
```


In `2` option:
```shell
python3 check_it.py --urls https://abit.itmo.ru/rating/master/budget/16077 https://leetcode.com/ https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1214/index.html
```

## Enable Telegram bot :robot:
If there will be changes in specified urls you can get message from YOUR telegram bot.
Define two environmental variables:
* `BOT_TOKEN` (get from [BotFather](https://telegram.me/BotFather))
* `MY_TELEGRAM_ID` (get from [here](https://telegram.me/getmyid_bot) for example)