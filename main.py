import random
import re
import io

from framework import Bot, Context

from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters.img import ImageFormatter

from config import token, owners

CODEBLOCK_REGEX = re.compile(r'/codeblock (\w+)((?:.|\n)+)')

bot = Bot(token=token, owners=owners)

@bot.command()
def hello(ctx: Context):
    ctx.reply("Hello! I'm a robot! NCPlayz and Ilya made me.")

@bot.command(owner_only=True)
def eval(ctx: Context):
    ctx.send('super secret data shh')

@bot.command(owner_only=True)
def add_owner(ctx: Context):
    bot.owners.append(int(ctx.args[0]))
    ctx.send('added to owner list.')

tags = {
    'zws': 'Zero Width Samus',
    'ayysyncio': 'https://cdn.discordapp.com/attachments/84319995256905728/360193276004794378/unknown.png',
}

# TODO: Move to a db (sqlite?)

@bot.command()
def tag(ctx: Context):
    if not ctx.args:
        return
    
    try:
        ctx.send(tags[ctx.args[0]])
    except:
        ctx.send('Tag not found.')

@bot.command()
def tag_create(ctx: Context):
    if not ctx.args:
        return
    
    if len(ctx.args) > 1:
        name, content = ctx.args[0], ctx.args[1:]
        if name in tags:
            ctx.send(f'Tag {name} already exists.')
        else:
            tags[name] = ' '.join(content)
            ctx.send(f'Tag {name} successfully created.')

@bot.command()
def choose(ctx: Context):
    choices = ctx.args
    chosen = random.choice(choices)
    ctx.send(f'```{chosen}```', markdown=True)

@bot.command()
def codeblock(ctx: Context):
    content = ctx.content
    if not content:
        return ctx.send('Content not found.')

    match = CODEBLOCK_REGEX.search(content)

    if match:
        try:
            lexer = get_lexer_by_name(match.group(1), stripall=True)
        except ClassNotFound:
            return ctx.send('Language could not be recognised.')

        formatter = ImageFormatter(image_format="PNG")

        file = io.BytesIO()
        result = highlight(match.group(2), lexer, formatter, outfile=file)

        file.seek(0)
        ctx.send(photo=file)
    else:
        return ctx.send('Could not recognise content.')

bot.run()
