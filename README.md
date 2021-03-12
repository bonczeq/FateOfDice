# FateOfDice
Discord bot that allows rolling dices and perform tests for supported RPG systems.

## Table of Contents
* [Command usage](#Command-usage)  
* [Installation](#Installation)

## Command usage
Bot supports commands for the following RPG systems:
* common rolls - roll the defined dices
* Call of Cthulhu RPG - check Call of Cthulhu RPG skill
* Tales from the Loop RPG - check overcoming Tales From The Loop RPG troubles
* Alien RPG - check Alien RPG skill

### Common rolls
Supported aliases: `r`, `!`, `roll`
```
\r [dices ...] [-h] [-e value | --upper-than value | --lower-than value]
[-m | -x | -s | -r | --sum | --average-floor | --average-ceil] [--comment [text]]

Universal dice roll.

positional arguments:
dices                               rolls description (default: 1d100)

optional arguments:
-h, --help                          show this help message and exit
-e value, --equal value             show dices equal to given value
--upper-than value                  show dices upper than given value
--lower-than value                  show dices lower than given value
-m, --min                           show min dice
-x, --max                           show max dice
-s, --sort                          show sorted dices
-r, --reverse-sort                  show reverse sorted dices
--sum                               show sum of dices
--average-floor                     show dices average rounded down
--average-ceil                      show dices average rounded up
--comment [text]                    ignored comment
```

### Call of Cthulhu RPG
Supported aliases: `c`, `?`, `CoC`, `CallOfCthulhu`
```
\c [skill value] [-h] [-b [amount]] [-p [amount]] [--comment [text]]

Call of Cthulhu skill check.

positional arguments:
skill value                         keeper skill value (default: no result verification)

optional arguments:
-h, --help                          show this help message and exit
-b [amount], --bonus [amount]       amount of bonus dices
-p [amount], --penalty [amount]     amount of penalty dices
--comment [text]                    ignored comment
```

### Tales from the Loop RPG
Supported aliases: `t`, `TftL`, `TalesFromTheLoop`
```
\t [dice amount] [required number of successes] [-h] [--comment [text]]

Tales from the Loop roll check.

positional arguments:
dice amount                         number of dices to roll (default: 1)
required number of successes        number of dices to success (default: 1)

optional arguments:
-h, --help                          show this help message and exit
--comment [text]                    ignored comment

```

### Alien RPG
Supported aliases: `a`, `Alien`
```
\a [base dice amount] [stress dice amount] [-h] [--comment [text]]

Tales from the Loop roll check.

positional arguments:
base dice amount                    number of dices to roll (default: 1)
stress dice amount                  number of stress dices to roll (default: 0)

optional arguments:
-h, --help                          show this help message and exit
--comment [text]                    ignored comment
```

## Installation
Bot can be run by execution built exe file (Windows system) or execute python script 
`src/fate_of_dice/__main__.py` (required Python version `>= 3.8`).

[Mandatory property](#Required-properties) settings are required.

### Properties
Properties can be defined by setting an environment variable (it overrides other method of settings) 
or by editing [`config.ini`](src/fate_of_dice/resources/config.ini) file.

#### Required properties
`FATE_OF_DICE_TOKEN` discord bot token
* required bot permissions: `Send Messages` and `Read Message History`

#### Optional properties
`FATE_OF_DICE_PREFIX` list of FateOfDice bot prefixes
* default: `[/, \, fateOfDice]`
* supported format: `[prefixes_separated_by_commas]`

`FATE_OF_DICE_SIMPLE_PRESENTATION` if bot messages should present minimal information
* default: `False`
* supported value: `True` or `False`

`FATE_OF_DICE_PURELY_ASCII` if bot messages can use Unicode
* default: `False`
* supported value: `True` or `False`

`FATE_OF_DICE_URL_ICONS` if bot messages should use icons from URLs or from files attached to messages 
* default: `Default` URLs if online, otherwise files attached to messages
* supported value: `True`, `False` or `Default`

## License
[![GitHub](https://img.shields.io/github/license/bonczeq/FateOfDice?style=flat-square)](./LICENSE)

## Status
[![Code with](https://img.shields.io/badge/BUILT%20WITH%20SCIENCE%20%F0%9F%A7%AA-a832a0?style=for-the-badge)](https://github.com/bonczeq)
[![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/en/latest/#)
[![Python](https://img.shields.io/badge/Python-yellow?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Git](https://img.shields.io/badge/Git-F1502F?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com)

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bonczeq/FateOfDice?style=flat-square&label=official-release)](https://github.com/bonczeq/FateOfDice/releases)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/bonczeq/FateOfDice?include_prereleases&label=newest-release)](https://github.com/bonczeq/FateOfDice/releases)


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bonczeq/FateOfDice/FateOfDice%20push?style=flat-square)](https://github.com/bonczeq/FateOfDice/actions/workflows/on_push.yml?query=branch:master++)
[![GitHub issues](https://img.shields.io/github/issues/bonczeq/FateOfDice?style=flat-square)](https://github.com/bonczeq/FateOfDice/issues)
