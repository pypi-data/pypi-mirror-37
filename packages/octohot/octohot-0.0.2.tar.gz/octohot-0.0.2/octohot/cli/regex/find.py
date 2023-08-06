import click
import logging
from octohot.sh import sh


def _find(repo, find_str):
    # find_str = find_str.replace('|', '\|').replace('"', '\\"')
    find_str = find_str.replace("'", "\\x27")
    cmd = "grep -PRl '%s' %s --exclude-dir=.git"
    files = sh(cmd % (find_str, repo.folder))
    if files:
        logging.info(
            '\'%s\' found in repo %s: \n'
            '%s' % (find_str, repo.name, '\n'.join(files))
        )
        return files
    return []


def matches(files, find_str):
    all_matches = []
    for file in files:
        cmd = "grep -Pohn '%s' %s --exclude-dir=.git"
        all_matches += sh(cmd % (find_str, file))

        logging.info(
            'Patterns founded in file %s : \n'
            '%s' % (file, '\n'.join(files))
        )
    return all_matches


@click.command()
@click.argument('find_string')
@click.option('--only_filepath', '-p', is_flag=True,
              help='print only filepaths')
def find(find_string, only_filepath):
    """Find a regular expression in all repos"""
    from octohot.cli.config import repositories
    for repo in repositories:
        files = _find(repo, find_string)
        if files:
            click.echo('\n'.join(files))
            if not only_filepath:
                click.echo('\n'.join(matches(files, find_string)))
