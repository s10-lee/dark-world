import os
import json
from click import group, argument, option, command, Context, pass_context, style, Path, File, types
from .functions import track_time, coro, import_driver, save_to_file, get_timestamp


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