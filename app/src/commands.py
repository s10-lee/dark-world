import os
import json
from click import (
    group, argument, option, command, Context, pass_context, style, Path, File, types, UsageError, echo, secho
)
from .functions import track_time, coro, import_driver, save_to_file, get_timestamp
from .models import User, Permission, SignUpToken, APIKeys, RefreshToken
from .security import get_password_hash, generate_private_public_keys
from typing import List, Optional, Any
from datetime import datetime, timedelta
from tortoise import Tortoise


def get_connection(context):
    return Tortoise.get_connection('default')


def validate_password(ctx, param, value):
    if len(value) < 6:
        raise UsageError(
            message='Must be greater than 6 characters',
            ctx=ctx,
        )
    return value


@group(context_settings={"help_option_names": ["--help"]})
@pass_context
@coro
async def cli(ctx: Context):
    ctx.ensure_object(dict)


@cli.command()
@argument("name")
@option("--start", default=0, type=types.INT)
@option("--stop", default=0, type=types.INT)
@option("--batch", default=1, type=types.INT)
@option("--delay", default=1, type=types.INT)
@track_time
@coro
async def run(name, **kwargs):
    constructor = import_driver(name)
    driver = constructor()
    await driver.fetch_all(**kwargs)


@cli.command(help="Merge json files")
@argument("source", nargs=-1, type=Path())
@option("--dst", "destination", default=None)
@option("--file", "--filename", "filename", default=None)
@option("--limit", default=None, type=types.INT)
@option("--clear", default=False, is_flag=True)
def merge(source, destination=None, filename=None, limit=None, clear=False):
    dirname = ""
    index = 0
    content = ""
    for index, file in enumerate(source):
        print(file, " ")
        with open(file, "r") as fp:
            text = fp.read()
            content += text[1:-1] + ", "
        if clear:
            os.unlink(file)
        if limit and index >= limit:
            break

        dirname = os.path.dirname(file)

    content = "[" + content[:-2] + "]"
    print("Merged = ", index + 1)
    if destination:
        dirname = destination
    if not filename:
        filename = f"merge_{get_timestamp()}"

    save_to_file(content, dirname, filename=filename)
    print(style("Saved", "bright_green", bold=True))


@cli.command()
@argument("file", nargs=1, type=File("r"))
@argument("keys", nargs=-1, required=False, default=None)
@option("-i", "--index", default=None, type=types.INT)
@option("--offset", default=0, type=types.INT)
@option("--limit", default=None, type=types.INT)
@option("--finish", default=None, type=types.INT)
@option("-v", "--verbose", is_flag=True, default=False)
@pass_context
@track_time
def load(ctx: Context, file, keys=None, index=None, offset=0, limit=None, finish=None, verbose=False, **kwargs):
    ctx.ensure_object(dict)
    data = json.load(file)
    length = len(data)
    if isinstance(index, int):
        print("--- index", index, " ---")
        data = [data[index]]
        verbose = True
    else:
        if finish and finish <= len(data):
            data = data[:finish]
        elif limit and offset + limit > offset:
            data = data[:offset + limit]

        if offset > 0:
            data = data[offset:]

        print("--- slice", len(data), " ---")

    if verbose:
        display_items = data
        if keys:
            display_items = []
            for data_item in data:
                display_items += [{key: value for key, value in data_item.items() if key.lower() in keys}]
        result = json.dumps(display_items, indent=4)
        print(result)
    print("--- ", length, "items  ---")


@cli.command(help='Create user')
@option('-u', '--username', prompt='Username')
@option('-e', '--email', prompt='Email', required=False, default='')
@option('-p', '--password', prompt='Password', hide_input=True, confirmation_prompt=True, callback=validate_password)
@option('--perm', required=False, default=None)
@pass_context
@coro
async def add_user(ctx: Context, username: str, password: str, email: Optional[str] = '', perm: Optional[str] = None):
    get_connection(ctx)

    try:
        user = await User.create(
            username=username,
            password=get_password_hash(password),
            email=email,
            is_active=True,
        )
        if perm:
            for pid in perm.replace(' ', '').split(','):
                permission = await Permission.get(id=int(pid))
                if permission:
                    await permission.users.add(user)
                    echo(style(f'{permission.slug} was added !', fg='green'))

    except Exception as e:
        secho('Error:', fg='red', bold=True)
        echo(e)
    else:
        secho('User was created !', fg='green', bold=True)


@cli.command(help='Create permission')
@option('--slug', prompt='Slug', required=True)
@pass_context
@coro
async def add_perm(ctx: Context, slug: str):
    get_connection(ctx)
    slug = slug.lower().strip().replace(' ', '_')

    try:
        await Permission.create(slug=slug)
    except Exception as e:
        secho('Error:', fg='red', bold=True)
        echo(e)
    else:
        secho('Permission created !', fg='green', bold=True)


@cli.command(help='Generate sign up link')
@option('--exp', 'exp', required=False, type=int)
@pass_context
@coro
async def sign_up(ctx: Context, exp: Optional[int] = None):
    get_connection(ctx)
    expires = None

    if exp:
        expires = datetime.utcnow() + timedelta(hours=exp)

    try:
        token = await SignUpToken.create(expires_at=expires)
    except Exception as e:
        echo(style(f'Error:', fg='red', bold=True))
        echo(e)
    else:
        echo(style('Sign up hash:', fg='green', bold=True))
        echo(token.id)


@cli.command(help='Generate key pair')
@pass_context
@coro
async def rotate_keys(ctx: Context):
    get_connection(ctx)

    private, public = generate_private_public_keys()
    await APIKeys.create(
        private_key=private.decode(),
        public_key=public.decode()
    )
    secho('API Keys:', fg='green', bold=True)


@cli.command(help='Delete all refresh tokens')
@pass_context
@coro
async def del_refresh(ctx: Context):
    get_connection(ctx)
    await RefreshToken.all().delete()
    secho('Deleted !', fg='green', bold=True)
