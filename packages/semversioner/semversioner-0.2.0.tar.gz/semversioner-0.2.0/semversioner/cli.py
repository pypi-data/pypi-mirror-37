#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert next release changes to version releases.
At any given time, the ``.changes/`` directory looks like:
    .changes
    |
    └── next-release
        ├── bugfix-BP-2012.json
        └── feature-BP-2011.json
    ├── 1.1.0.json
    ├── 1.1.1.json
    ├── 1.1.2.json
This script takes everything in ``next-release`` and aggregates them all
together in a single JSON file for that release (e.g ``1.12.0.json``).  This
JSON file is a list of all the individual JSON files from ``next-release``.
This is done to simplify changelog generation.  Rather than have hundreds of
individual files, we now have 1 file per release.  This also makes the
rendering process for changelogs easier.
Usage
=====
::
    $ semversioner release
    $ semversioner changelog
"""

import os
import sys
import json
import click
import datetime
from distutils.version import StrictVersion
import re

ROOTDIR = os.getcwd()

@click.group()
@click.option('--path', default=ROOTDIR)
@click.pass_context
def cli(ctx, path):
    """Command line tool for managing releases."""
    changedir = os.path.join(path, '.changes')
    if not os.path.isdir(changedir):
        sys.stderr.write("'.changes' folder does not exist in path: %s\n" % changedir)
        return
    ctx.obj['CHANGELOG_DIR'] = changedir
 
@cli.command('release')
@click.pass_context
def cli_release(ctx):
    release(ctx.obj['CHANGELOG_DIR'])

@cli.command('changelog')
@click.pass_context
def cli_changelog(ctx):
    changedir = ctx.obj['CHANGELOG_DIR']
    click.echo(generate_changelog(changedir))

@cli.command('add-change')
@click.pass_context
@click.option('--type', type=click.Choice(['major', 'minor', 'patch']), required=True)
@click.option('--description', required=True)
def cli_changelog(ctx, type, description):
    changedir = ctx.obj['CHANGELOG_DIR']
    
    write_new_change(changedir, type, description)

def write_new_change(dirname, type, description):

    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    # Assume that new changes go into the next release.
    dirname = os.path.join(dirname, 'next-release')
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    
    parsed_values = {
        'type': type,
        'description': description,
    }

    # Need to generate a unique filename for this change.
    # We'll try a couple things until we get a unique match.
    change_type = parsed_values['type']

    filename = None
    while (filename is None or os.path.isfile(os.path.join(dirname, filename))):
        filename = '{type_name}-{datetime}.json'.format(
            type_name=parsed_values['type'],
            datetime="{:%Y%m%d%H%M%S}".format(datetime.datetime.utcnow()))

    with open(os.path.join(dirname, filename), 'w') as f:
        f.write(json.dumps(parsed_values, indent=2) + "\n")

def generate_changelog(changedir):
    contents = [
        '',
        '# Changelog',
        'During the Alpha period, minor version releases in the 0.x.y range may introduce breaking changes to the task\'s interface. ',
        '',
    ]
    for release_identifier in sorted_releases(changedir):
        with open(os.path.join(changedir, release_identifier + '.json')) as f:
            data = json.load(f)
        
        contents.append('## ' + release_identifier)
        contents.append('')
        for change in data:
            line = '- %s: %s' % (change['type'], change['description'])
            contents.append(line)
        contents.append('')
        contents.append('')
    return '\n'.join(contents)

def release(changedir):
    changes = []
    next_release_dir = os.path.join(changedir, 'next-release')
    for filename in os.listdir(next_release_dir):
        full_path = os.path.join(next_release_dir, filename)
        with open(full_path) as f:
            data = json.load(f)
            changes.append(data)

    max_type = _get_change_type(changes)
    
    current_version_number = _get_current_version_number()
    next_version_number = increase_version(current_version_number, max_type)
    print("Current release: %s" % current_version_number)
    print("Next release: %s\n" % next_version_number)
    release_json_filename = os.path.join(changedir, '%s.json' % next_version_number)
    with open(release_json_filename, 'w') as f:
        f.write(json.dumps(changes, indent=2, sort_keys=True))
    for filename in os.listdir(next_release_dir):
        full_path = os.path.join(next_release_dir, filename)
        os.remove(full_path)
    os.rmdir(next_release_dir)

    for filename, replacer in get_files_to_change().items():
        print("Bumping version in %s" % filename)
        with open(filename, 'r') as f:
            contents = f.read()
            if callable(replacer):
                new_contents = replacer(contents)
            else:
                new_contents = _regex_based_version_bump(
                    current_version_number,
                    next_version_number,
                    replacer,
                    contents)
            with open(filename, 'w') as f:
                f.write(new_contents)
    
    # generate CHANGELOG.md
    with open("CHANGELOG.md", 'w') as f:
        f.write(generate_changelog(changedir))

def get_files_to_change():
    # A mapping of all files that require version bumps.
    # You can either specify:
    # * Tuple[str, str] - regex to search, replacement string
    # * Callable[[str, str], str] - function to handle custom logic
    files_with_version_numbers = {
        'next.version': ("{previous_version}", "{next_version}"),
        'README.md': ("{previous_version}", "{next_version}"),
    }
    return files_with_version_numbers

def _regex_based_version_bump(previous_version_number, next_version_number, replacer, contents):
    regex = replacer[0].format(previous_version=previous_version_number)
    replacement = replacer[1].format(next_version=next_version_number)
    new_contents = re.sub(regex, replacement, contents)
    return new_contents

def _get_change_type(changes):
    return sorted(list(map(lambda x: x['type'], changes)))[0]

def sorted_releases(changedir):
    files = [f for f in os.listdir(changedir) if os.path.isfile(os.path.join(changedir, f))]
    releases=list(map(lambda x: x[:-len('.json')], files))
    releases=sorted(releases, key=StrictVersion, reverse=True)
    return releases

def _get_current_version_number():
    with open('next.version') as f:
        version = f.readline()
        return version
    raise RuntimeError("Could not find version number from next.version")


def increase_version(current_version, release_type):
    """ 
    Returns a string like '1.0.0'.
    """
    # Convert to a list of ints: [1, 0, 0].
    version_parts = list(int(i) for i in current_version.split('.'))
    if release_type == 'patch':
        version_parts[2] += 1
    elif release_type == 'minor':
        version_parts[1] += 1
        version_parts[2] = 0
    elif release_type == 'major':
        version_parts[0] += 1
        version_parts[1] = 0
        version_parts[2] = 0
    return '.'.join(str(i) for i in version_parts)

def main():
    cli(obj={})

if __name__ == '__main__':
    main()