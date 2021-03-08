from discord.ext.commands import Bot, Context

from fate_of_dice.system import DiceResult
from fate_of_dice.system.alien import check_action
from fate_of_dice.system.call_of_cthulhu import check_skill
from fate_of_dice.system.tales_from_the_loop import overcome_trouble
from fate_of_dice.system.universal import roll

from fate_of_dice.common import log
from fate_of_dice.discord_bot.mapper import crate_embed
from .environment import BOT_TOKEN, COMMAND_PREFIXES, SIMPLE_PRESENTATION

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
    discord_result = crate_embed("Please check: [help](https://github.com/bonczeq/FateOfDice/blob/master/README.md")
    await ctx.send(discord_result)


@bot.command(aliases=['r', '!', 'roll'])
async def universal_roll(ctx: Context, *arguments: str) -> None:
    command_prefix: str = ctx.prefix + ctx.invoked_with
    roll_result = roll(ctx.author.name, command_prefix, arguments)
    discord_result = crate_embed(roll_result, ctx.message, SIMPLE_PRESENTATION)
    await _send_message(ctx, discord_result, roll_result)


@bot.command(aliases=['c', '?', 'CoC', 'CallOfCthulhu'])
async def call_of_cthulhu_check(ctx: Context, *arguments: str) -> None:
    command_prefix: str = ctx.prefix + ctx.invoked_with
    skill_result = check_skill(ctx.author.name, command_prefix, arguments)
    discord_result = crate_embed(skill_result, ctx.message, SIMPLE_PRESENTATION)
    await _send_message(ctx, discord_result, skill_result)


@bot.command(aliases=['t', 'TftL', 'TalesFromTheLoop'])
async def tales_from_the_loop_check(ctx: Context, *arguments: str) -> None:
    command_prefix: str = ctx.prefix + ctx.invoked_with
    roll_result = overcome_trouble(ctx.author.name, command_prefix, arguments)
    discord_result = crate_embed(roll_result, ctx.message, SIMPLE_PRESENTATION)
    await _send_message(ctx, discord_result, roll_result)


@bot.command(aliases=['a', 'Alien'])
async def alien_check(ctx: Context, *arguments: str) -> None:
    command_prefix: str = ctx.prefix + ctx.invoked_with
    check_result = check_action(ctx.author.name, command_prefix, arguments)
    discord_result = crate_embed(check_result, ctx.message, SIMPLE_PRESENTATION)
    await _send_message(ctx, discord_result, check_result)


async def _send_message(ctx: Context, discord_result, dice_result: DiceResult) -> None:
    await ctx.send(**discord_result)

    if dice_result.priv_request:
        await ctx.author.send(**discord_result)


@bot.event
async def on_command_error(ctx, error):
    original = error.original
    await ctx.send(**crate_embed(original))


def run_bot():
    if BOT_TOKEN:
        bot.run(BOT_TOKEN)
    else:
        raise Exception('Bot token has not be defined')
