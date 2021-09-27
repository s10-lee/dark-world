import click
from app.src.user.models import User
from app.src.functions import coro


@click.group()
@click.pass_context
async def command_group(ctx: click.Context):
    pass


@command_group.command(name='project')
@click.option('-u', '--username', required=True)
@click.option('-s', '--slug', required=True)
@click.option('-n', '--name', default='')
@coro(keep_alive=True)
async def grab_project(username: str, slug: str, name: str = ''):
    user = await User.get_or_none(username=username)
    if not user:
        return click.secho(f'User with name "{username}" not found', fg='yellow', bold=True)

    try:
        project = GrabberProject(name=name, slug=slug, user=user)
        await project.save()
    except Exception as e:
        return click.secho(f'Error {e}', fg='red', bold=True)
    click.secho(f'Project {project.id} was created', fg='green', bold=True)


@command_group.command(name='run')
@click.option('-p', '--project', 'project_id', required=True, type=click.types.INT)
@click.option('-v', '--var', nargs=2, multiple=True, type=(str, str), required=False)
@coro(keep_alive=True)
async def grab_run(project_id, var):

    project = await GrabberProject.get_or_none(id=project_id)
    if not project:
        return click.secho(f'Project ID {project.id} not found', fg='yellow', bold=True)

    await project.fetch_related('requests')

    # Set variables
    variables = dict()
    for name, value in var:
        variables[name] = value

    for request in project.requests:

        prepared = await prepare_request(request=request)
        resp = await make_request(**prepared)

        print(prepared['url'])
        print(prepared['headers'])
        print(' ----->  ', resp['content_type'])
        print(resp['status'])

        response = GrabberResponse(request=request,
                                   headers=resp['headers'],
                                   data=resp['data'],
                                   status=resp['status'])
        await response.save()

        parsed_body = convert_response_to_dict(resp['data'], resp['content_type'])


@command_group.command(name='req')
@click.option('-p', '--project', 'project_id', required=True, type=click.types.INT)
@click.option('-m', '--method', default='get')
@click.option('--url', required=True)
@click.option('--name', default='')
@click.option('--parent', 'parent_id', default=None, type=click.types.INT)
@coro(keep_alive=True)
async def grab_request(project_id: int, method: str, url: str, name: str, parent_id: int = None):
    project = await GrabberProject.get_or_none(id=project_id)
    if not project:
        return click.secho(f'Project ID {project.id} not found', fg='yellow', bold=True)

    parent = None
    if parent_id:
        parent = await GrabberRequest.filter(id=parent_id, project_id=project_id).first()
        if not parent:
            return click.secho(f'Parent Request {parent.id} not found', fg='yellow', bold=True)

    method = method.upper()

    try:
        request = GrabberRequest(name=name, method=method, url=url, project=project, parent=parent)
        await request.save()
    except Exception as e:
        return click.secho(f'Error {e}', fg='red', bold=True)
    click.secho(f'Request {project.id} was created', fg='green', bold=True)