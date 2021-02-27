![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white) 
![Python](https://img.shields.io/badge/Python-yellow?style=for-the-badge&logo=python&logoColor=white) 
![Git](https://img.shields.io/badge/Git-F1502F?style=for-the-badge&logo=git&logoColor=white)

# FateOfDice
Discord bot that allows rolling dices and perform tests for supported RPG systems.

## Command usage
Bot supports commands for the following RPG systems:
* common rolls - roll described dices
* Call of Cthulhu - skill check

### Common rolls
Supported aliases: `r`, `!`, `roll`
```
\r [dices ...] [-h] [-m] [-x] [-s] [-r] [-u] [-c COMMENT [COMMENT ...]]

Universal dice roll.

positional arguments:
dices                   rolls description (default: 1d100)

optional arguments:
-h, --help              show this help message and exit

optional result presentation arguments:
-m, --min               show min dice
-x, --max               show max dice
-s, --sort              show sorted dices
-r, --reverse-sort      show reverse sorted dices
-u, --sum               show sum of dices
-c COMMENT [COMMENT ...], --comment COMMENT [COMMENT ...]       ignored comment
```

### Call of Cthulhu skill check
Supported aliases: `c`, `?`, `CoC`, `CallOfCthulhu`
```
\c [skill_value] [-h] [-b [BONUS_DICE_AMOUNT]] [-p [PENALTY_DICE_AMOUNT]] [-c COMMENT [COMMENT ...]]

Call of Cthulhu skill check.

positional arguments:
skill_value         keeper skill value (default: no result verification) 

optional arguments:
-h, --help                                                      show this help message and exit
-b [BONUS_DICE_AMOUNT], --bonus [BONUS_DICE_AMOUNT]             amount of bonus dices
-p [PENALTY_DICE_AMOUNT], --penalty [PENALTY_DICE_AMOUNT]       amount of penalty dices
-c COMMENT [COMMENT ...], --comment COMMENT [COMMENT ...]       ignored comment
```

## Installation
Bot can be run by execution built exe file (Windows system) or execute python script 
`src/fate_of_dice/__main__.py` (required Python version `>= 3.8`).

[Mandatory property](#Required-properties) settings are required.

### Properties
Properties can be defined by setting an environment variable (it overrides other method of settings) 
or by editing [`config.ini`](resources/config.ini) file.

#### Required properties
`FATE_OF_DICE_TOKEN` discord bot token
* required bot permissions: `Send Messages` and `Read Message History`

#### Optional properties
`FATE_OF_DICE_PREFIX` list of FateOfDice bot prefixes
* default: `[/, \, fateOfDice]`
* supported format: `[prefixes_separated_by_commas]`

`FATE_OF_DICE_SIMPLE_PRESENTATION` if bot message should present minimal information
* default: `False`
* supported value: `True` or `False`

## License
![GitHub](https://img.shields.io/github/license/bonczeq/FateOfDice?style=flat-square)

## Status
![Code with](https://img.shields.io/badge/CODE%20WITH%20%20%20%E2%99%A5-a832a0?style=for-the-badge)

![GitHub release (latest by date)](https://img.shields.io/github/v/release/bonczeq/FateOfDice?style=flat-square)

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bonczeq/FateOfDice/FateOfDice%20push?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/bonczeq/FateOfDice?style=flat-square)
