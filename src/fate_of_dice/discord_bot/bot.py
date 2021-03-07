from discord.ext.commands import Bot, Context

from fate_of_dice.system.call_of_cthulhu import check_skill
from fate_of_dice.system.tales_from_the_loop import roll_check
from fate_of_dice.system.universal import roll
from fate_of_dice.common import log, DiceException
from .environment import BOT_TOKEN, COMMAND_PREFIXES, SIMPLE_PRESENTATION
from .mapper import crate_embed

bot = Bot(case_insensitive=True, command_prefix=COMMAND_PREFIXES)


@bot.event
async def on_ready():
    log('Bot ready')
    log(f'Bot token: {BOT_TOKEN}')
    log(f'Bot prefixes: {" or ".join(COMMAND_PREFIXES)}')
    log(f'Simple presentation: {SIMPLE_PRESENTATION}')


@bot.command()
async def info(ctx: Context) -> None:
    log("Received info command")
    await ctx.send(
        embed=crate_embed("Please check: [help](https://github.com/bonczeq/FateOfDice/blob/master/README.md"))


@bot.command(aliases=['r', '!', 'roll'])
async def universal_roll(ctx: Context, *arguments: str) -> None:
    command_prefix: str = ctx.prefix + ctx.invoked_with
    roll_result = roll(ctx.author.name, command_prefix, arguments)
    discord_result = crate_embed(ctx.message, roll_result, SIMPLE_PRESENTATION)
    await ctx.send(**discord_result)


@bot.command(aliases=['c', '?', 'CoC', 'CallOfCthulhu'])
async def call_of_cthulhu_test(ctx: Context, *arguments: str) -> None:
    command_prefix: str = ctx.prefix + ctx.invoked_with
    skill_result = check_skill(ctx.author.name, command_prefix, arguments)
    discord_result = crate_embed(ctx.message, skill_result, SIMPLE_PRESENTATION)
    await ctx.send(**discord_result)


@bot.command(aliases=['t', 'TftL', 'TalesFromTheLoop'])
async def tales_from_the_loop_test(ctx: Context, *arguments: str) -> None:
    command_prefix: str = ctx.prefix + ctx.invoked_with
    roll_result = roll_check(ctx.author.name, command_prefix, arguments)
    discord_result = crate_embed(ctx.message, roll_result, SIMPLE_PRESENTATION)
    await ctx.send(**discord_result)


@bot.event
async def on_command_error(ctx, error):
    original = error.original
    await ctx.send(**crate_embed(original))

    if not isinstance(original, DiceException):
        raise error


def run_bot():
    if BOT_TOKEN:
        bot.run(BOT_TOKEN)
    else:
        raise Exception('Bot token has not be defined')
