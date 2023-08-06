import click
import keyring

from .config import Config
from .akashi import akashi

config = Config()

@click.group()
def login_cmd():
    pass

@login_cmd.command()
@click.option('--company', '-c', prompt=True)
@click.option('--username', '-u', prompt=True)
@click.option('--password', '-p', prompt=True, hide_input=True)
def login(company, username, password):
    """Login to akashi"""
    keyring.set_password('akashi-cli', username, password)
    config.set({'company': company, 'username': username})
    print("Sucessed to login.")

@click.group()
def logout_cmd():
    pass

@logout_cmd.command()
def logout():
    """Logout to akashi"""
    data = config.get()
    if data:
        keyring.delete_password('akashi-cli', data['username'])
        config.delete()
    print('Logout.')

@click.group()
def attend_cmd():
    pass

@attend_cmd.command()
@click.option('--no-headless', is_flag=True, default=False)
@click.option('--audio', is_flag=True, default=False)
def attend(no_headless, audio):
    """Attend to akashi"""
    data = config.get()
    if data:
        password = keyring.get_password('akashi-cli', data['username'])
        akashi('attend', data['company'], data['username'], password, headless=not(no_headless), mute_audio=not(audio))
    else:
        print('Please login first.')

@click.group()
def leave_cmd():
    pass

@leave_cmd.command()
@click.option('--no-headless', is_flag=True, default=False)
@click.option('--audio', is_flag=True, default=False)
def leave(no_headless, audio):
    """Leave to akashi"""
    data = config.get()
    if data:
        password = keyring.get_password('akashi-cli', data['username'])
        akashi('leave', data['company'], data['username'], password, headless=not(no_headless), mute_audio=not(audio))
    else:
        print('Please login first.')

cli = click.CommandCollection(sources=[login_cmd, logout_cmd, attend_cmd, leave_cmd])
cli()
