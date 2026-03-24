#!/usr/bin/env python3
"""Dictionary CLI. Usage: python d.py <command> [args]"""

import argparse
import sys
import os

# Auto-activate venv if present and not already active
_dir = os.path.dirname(os.path.abspath(__file__))
_venv_python = os.path.join(_dir, 'venv', 'bin', 'python3')
if os.path.exists(_venv_python) and sys.prefix == sys.base_prefix:
    os.execv(_venv_python, [_venv_python] + sys.argv)

# Add scripts/ to path so imports work
sys.path.insert(0, os.path.join(_dir, 'scripts'))


def cmd_new(args):
    from new import main as new_main
    sys.argv = ['new', args.headword]
    new_main()


def cmd_validate(args):
    from validate import main as validate_main
    sys.argv = ['validate'] + args.letters
    validate_main()


def cmd_export(args):
    from export import main as export_main
    export_main()


parser = argparse.ArgumentParser(
    prog='d.py', description='Kaitag dictionary tools')
sub = parser.add_subparsers(dest='command', required=True)

p_new = sub.add_parser('new', help='create a new entry file with ID')
p_new.add_argument('headword', help='headword for the new entry')
p_new.set_defaults(fn=cmd_new)

p_val = sub.add_parser(
    'validate', help='validate entries: structure, IDs, tags, schema')
p_val.add_argument('letters', nargs='*',
                   help='letter folders to check (default: all)')
p_val.set_defaults(fn=cmd_validate)

p_exp = sub.add_parser('export', help='build all export formats')
p_exp.set_defaults(fn=cmd_export)

args = parser.parse_args()
args.fn(args)
