import click
import logging

from octohot.cli.regex.find import _find
from octohot.sh import sh


def _replace(repo, files, find_str, replace_str):
    """
        using regex groups:
            value = "1teste2"
            old = "[0-9](.*)[0-9]"
            new = "W\1Q"
            result = "WtesteQ"
    :param files:
    :param find_str:
    :param replace_str:
    :return:
    """
    find_str = find_str.replace('|', '\|').replace('"', '\\"')
    replace_str = replace_str.replace('|', '\|').replace('"', '\\"')
    find_str = find_str.replace("'", "\\x27")
    cmd = """sed -Ei "s|%s|%s|g" %s"""
    [sh(cmd % (find_str, replace_str, arq)) for arq in files]

    info = "Replaced '%s' to '%s' in repo %s:\n%s"
    info = info % (find_str, replace_str, repo.name, '\n'.join(files))
    logging.info(info)
    print(info)


@click.command()
@click.argument('find_string')
@click.argument('replace_string')
def replace(find_string, replace_string):
    """Find and replace a string in all repos"""
    from octohot.cli.config import repositories
    for repo in repositories:
        files = _find(repo, find_string)
        if len(files):
            _replace(repo, files, find_string, replace_string)
            click.echo('Replacing files:'+'\n'.join(files))