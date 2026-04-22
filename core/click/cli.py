from operator import is_

import click

import core.ansible.inventory as inv
import core.dock.container as dops

cp = dops.ContainerConfigProvider()
cc = dops.ContainerController()


@click.group()
def cli():
    pass


@cli.group()
def lab():
    pass


@lab.command()
@click.option("--name", required=True, help="Name for the container.")
@click.option("--host", default="localhost", help="Host IP.")
def init(name, host):
    i = inv.EvLabInventory()
    i.group_insert(name)
    host_vars = {"ansible_host": host} if host is not None else None
    host_vars = {"ansible_connection": "local"} if host == "localhost" else host_vars
    if host is not None and host_vars is not None:
        i.host_insert_update(host, name, host_vars=host_vars)


@cli.group()
def service():
    pass


@service.command()
@click.option("--host", default="localhost", help="Target host from inventory.")
@click.option("--image", required=True, help="Docker image to pull/run.")
@click.option("--name", required=True, help="Name for the container.")
def start(host, image, name):
    click.echo(f"Running {image} on {host}...")
    res = cc.Run(cp.Start(host, image, name))

    if res[0]:
        click.secho("Success!", fg="green")
        click.secho(res[1], fg="green")
    else:
        click.secho("Failed. Check the output above for details.", fg="red")


@service.command()
@click.option("--host", default="localhost", help="Target host from inventory.")
@click.option("--name", required=True, help="Name for the container.")
def stop(host, name):
    click.echo(f"Stopping container {name} on {host}...")
    res = cc.Run(cp.Stop(host, name))

    if res[0]:
        click.secho("Success!", fg="green")
        click.secho(res[1], fg="green")
    else:
        click.secho("Failed. Check the output above for details.", fg="red")


@service.command()
@click.option("--host", default="localhost", help="Target host from inventory.")
@click.option("--name", required=True, help="Name for the container.")
def pause(host, name):
    click.echo(f"Pausing container {name} on {host}...")
    res = cc.Run(cp.Pause(host, name))

    if res[0]:
        click.secho("Success!", fg="green")
        click.secho(res[1], fg="green")
    else:
        click.secho("Failed. Check the output above for details.", fg="red")


@service.command()
@click.option("--host", default="localhost", help="Target host from inventory.")
@click.option("--name", required=True, help="Name for the container.")
def unpause(host, name):
    click.echo(f"Resuming container {name} on {host}...")
    res = cc.Run(cp.Unpause(host, name))

    if res[0]:
        click.secho("Success!", fg="green")
        click.secho(res[1], fg="green")
    else:
        click.secho("Failed. Check the output above for details.", fg="red")


@service.command()
@click.option("--host", default="localhost", help="Target host from inventory.")
@click.option("--name", required=True, help="Name for the container.")
@click.option(
    "-force",
    required=False,
    default=False,
    is_flag=True,
    help="Image to use for the container.",
)
def destroy(host, name, force):
    click.echo(f"Destorying container {name} on {host}...")
    res = cc.Run(cp.Destroy(host, name, force))

    if res[0]:
        click.secho("Success!", fg="green")
        click.secho(res[1], fg="green")
    else:
        click.secho("Failed. Check the output above for details.", fg="red")
