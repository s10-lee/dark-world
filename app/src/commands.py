import json
import asyncio
from functools import wraps
from aerich import Command
from click import (
    group,
    argument,
    option,
    Context,
    pass_context,
    confirmation_option,
    style,
    UsageError,
    echo,
    secho,
)
# from app.src.functions import import_driver, save_to_file, get_timestamp
from app.src.security import get_password_hash, generate_private_public_keys
from app.src.models import User, Permission, SignUpToken, APIKeys, RefreshToken
from typing import Optional
from datetime import datetime, timedelta
import time
from tortoise import Tortoise, BaseDBAsyncClient
from app.src.settings import ORM
from pathlib import Path

# def get_connection(name: str = None) -> BaseDBAsyncClient:
#     return Tortoise.get_connection(name or 'default')


def validate_password(ctx, param, value):
    if len(value) < 6:
        raise UsageError('Must be greater than 6 characters', ctx=ctx)
    return value


def track_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        print('--- ', time.strftime('%H:%M:%S'), ' ---')
        result = f(*args, **kwargs)
        print(f'---  {round(time.time() - start, 2)} sec  ---')
        print('--- ', time.strftime('%H:%M:%S'), ' ---')
        return result
    return wrapper


def coro(function=None, keep_alive=False):
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            try:
                echo(f.__name__)
                loop.run_until_complete(f(*args, **kwargs))
            finally:
                if not keep_alive:
                    loop.run_until_complete(Tortoise.close_connections())
                loop.run_until_complete(asyncio.sleep(0.5))
        return wrapper
    if callable(function):
        return decorate(function)
    return decorate


@group(context_settings={'help_option_names': ['--help']})
@option('-l', '--location', required=False, default='./app/db/migrations')
@pass_context
@coro(keep_alive=True)
async def cli(ctx: Context, location: str):
    ctx.ensure_object(dict)
    subcommand = ctx.invoked_subcommand
    command = Command(tortoise_config=ORM, location=location, app='models')
    # command = Migrate.init(ORM, 'models', './app/db/migrations')
    ctx.obj['command'] = command
    if subcommand != 'init':
        await command.init()
    # await Tortoise.init(config=ORM)
    # await Tortoise.init(db_url=DATABASE_URL, modules={'models': ['app.src.models']})


# @cli.command()
# @argument('name')
# @option('--start', default=0, type=types.INT)
# @option('--stop', default=0, type=types.INT)
# @option('--batch', default=1, type=types.INT)
# @option('--delay', default=1, type=types.INT)
# @track_time
# @coro
# async def run(name, **kwargs):
#     constructor = import_driver(name)
#     driver = constructor()
#     await driver.fetch_all(**kwargs)


# @cli.command(help='Merge json files')
# @argument('source', nargs=-1, type=Path())
# @option('--dst', 'destination', default=None)
# @option('--file', '--filename', 'filename', default=None)
# @option('--limit', default=None, type=types.INT)
# @option('--clear', default=False, is_flag=True)
# def merge(source, destination=None, filename=None, limit=None, clear=False):
#     import os
#     dirname = ''
#     index = 0
#     content = ''
#     for index, file in enumerate(source):
#         print(file, ' ')
#         with open(file, 'r') as fp:
#             text = fp.read()
#             content += text[1:-1] + ', '
#         if clear:
#             os.unlink(file)
#         if limit and index >= limit:
#             break
#
#         dirname = os.path.dirname(file)
#
#     content = '[' + content[:-2] + ']'
#     print('Merged = ', index + 1)
#     if destination:
#         dirname = destination
#     if not filename:
#         filename = f'merge_{get_timestamp()}'
#
#     save_to_file(content, dirname, filename=filename)
#     print(style('Saved', 'bright_green', bold=True))


# @cli.command()
# @argument('file', nargs=1, type=File('r'))
# @argument('keys', nargs=-1, required=False, default=None)
# @option('-i', '--index', default=None, type=types.INT)
# @option('--offset', default=0, type=types.INT)
# @option('--limit', default=None, type=types.INT)
# @option('--finish', default=None, type=types.INT)
# @option('-v', '--verbose', is_flag=True, default=False)
# @pass_context
# @track_time
# def load(ctx: Context, file, keys=None, index=None, offset=0, limit=None, finish=None, verbose=False, **kwargs):
#     ctx.ensure_object(dict)
#     data = json.load(file)
#     length = len(data)
#     if isinstance(index, int):
#         print('--- index', index, ' ---')
#         data = [data[index]]
#         verbose = True
#     else:
#         if finish and finish <= len(data):
#             data = data[:finish]
#         elif limit and offset + limit > offset:
#             data = data[:offset + limit]
#
#         if offset > 0:
#             data = data[offset:]
#
#         print('--- slice', len(data), ' ---')
#
#     if verbose:
#         display_items = data
#         if keys:
#             display_items = []
#             for data_item in data:
#                 display_items += [{key: value for key, value in data_item.items() if key.lower() in keys}]
#         result = json.dumps(display_items, indent=4)
#         print(result)
#     print('--- ', length, 'items  ---')

@cli.group(name='user')
@pass_context
@coro(keep_alive=True)
async def user_group(ctx: Context):
    pass


@cli.group(name='db', help='Aerich wrapper')
@pass_context
@coro(keep_alive=True)
async def db_group(ctx: Context):
    pass


@user_group.command(name='add', help='Create user')
@option('-u', '--username', prompt='Username')
@option('-e', '--email', prompt='Email', required=False, default='')
@option('-p', '--password', prompt='Password', hide_input=True, confirmation_prompt=True, callback=validate_password)
@option('-s', '--staff', required=False, default=False, is_flag=True)
@coro
async def create_user(username: str,
                      password: str,
                      email: Optional[str] = '',
                      staff: Optional[str] = False):
    try:
        await User.create(
            username=username,
            password=get_password_hash(password),
            email=email,
            is_staff=staff,
            is_active=True,
        )

    except Exception as e:
        secho('Error:', fg='red', bold=True)
        echo(e)
    else:
        secho('User was created !', fg='green', bold=True)


@user_group.command(name='del', help='Delete user.')
@option('-u', '--username', required=False, default=None)
@option('-e', '--email', required=False, default=None)
@confirmation_option(prompt='Are you sure?')
@coro
async def delete_user(username: str, email: str):
    try:
        if username:
            ret = await User.filter(username=username).delete()
        elif email:
            ret = await User.filter(email=email).delete()
        else:
            return secho('At least one condition !', fg='red', bold=True)
    except Exception as e:
        secho('Error:', fg='red', bold=True)
        echo(e)
    else:
        secho(f'User record was deleted - {ret} !', fg='green', bold=True)


@cli.command(name='perm', help='Create permission.')
@option('-s', '--slug', prompt='Slug', required=True)
@coro
async def create_permission(slug: str):
    try:
        await Permission.create(slug=slug)
    except Exception as e:
        secho('Error:', fg='red', bold=True)
        echo(e)
    else:
        secho('Permission created !', fg='green', bold=True)


@user_group.command(name='sing', help='Generate sign up link.')
@option('-e', '--expire', 'hours', required=False, type=int, default=None, help='Hours before expire.')
@pass_context
@coro
async def create_signup_link(ctx: Context, hours: Optional[int] = None):
    expires_at = None
    if hours:
        expires_at = datetime.utcnow() + timedelta(hours=hours)

    try:
        token = await SignUpToken.create(expires_at=expires_at)
    except Exception as e:
        echo(style(f'Error:', fg='red', bold=True))
        echo(e)
    else:
        echo(style('Sign up hash:', fg='green', bold=True))
        echo(token.id)


@user_group.command(name='noref', help='Clear refresh tokens.')
@pass_context
@coro
async def delete_refresh_tokens(ctx: Context):
    await RefreshToken.all().delete()
    secho('Refresh tokens were deleted', fg='green', bold=True)


@cli.command(name='keygen', help='Generate and rotate key pairs.')
@pass_context
@coro
async def rotate_api_keys(ctx: Context):
    private, public = generate_private_public_keys()
    await APIKeys.create(
        private_key=private.decode(),
        public_key=public.decode()
    )
    secho('API Key was created', fg='green', bold=True)


@db_group.command(name='init', help='Generate schema and generate app migrate location.')
@option('--safe', default=True, help='Creates tables if it does not exist.', show_default=True)
@pass_context
@coro
async def init_db_aerich(ctx: Context, safe: bool):
    command = ctx.obj['command']
    app = command.app
    dirname = Path(command.location, app)
    try:
        await command.init_db(safe)
        secho(f'Migration {dirname}', fg='green', bold=True)
        secho(f'Schema generated "{app}"', fg='green', bold=True)
    except FileExistsError:
        return secho(
            f'"{app}" - already exists. Delete {dirname} and try again.', fg='yellow', bold=True
        )


@db_group.command(name='migrate', help='Create migration file.')
@option('--name', default='update', show_default=True, help='Migration name.')
@pass_context
@coro
async def create_db_migration(ctx: Context, name: str):
    command = ctx.obj['command']
    ret = await command.migrate(name)
    if not ret:
        return secho('No changes detected', fg='yellow', bold=True)
    secho(f'Success migrate {ret}', fg='green', bold=True)


@db_group.command(name='up', help='Upgrade DB.')
@pass_context
@coro
async def upgrade_db_migration(ctx: Context):
    command = ctx.obj['command']
    migrated = await command.upgrade()
    if not migrated:
        secho('No upgrade items found', fg='yellow')
    else:
        for version_file in migrated:
            secho(f'Success upgrade {version_file}', fg='green', bold=True)


@db_group.command(name='down', help='Downgrade DB.')
@option('-v', '--version', default=-1, type=int, show_default=True, help='Specified version, default to last.')
@option('-c', '--clear', is_flag=True, default=False, show_default=True, help='Delete migration files.')
@pass_context
@confirmation_option(prompt='Are you sure?')
@coro
async def downgrade_db_migration(ctx: Context, version: int, clear: bool):
    command = ctx.obj['command']
    try:
        files = await command.downgrade(version, clear)
    except Exception as e:
        return secho(str(e), fg='yellow', bold=True)
    for file in files:
        secho(f'Success downgrade {file}', fg='green', bold=True)
