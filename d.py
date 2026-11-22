#!/usr/bin/env python3
"""Dictionary CLI. Usage: python d.py <command> [args]"""

import argparse
import os
import sys

# Auto-activate venv if present and not already active
_dir = os.path.dirname(os.path.abspath(__file__))
_venv_python = os.path.join(_dir, 'venv', 'bin', 'python3')
if os.path.exists(_venv_python) and sys.prefix == sys.base_prefix:
    os.execv(_venv_python, [_venv_python] + sys.argv)

# Add scripts/ to path so imports work
sys.path.insert(0, os.path.join(_dir, 'scripts'))

parser = argparse.ArgumentParser(
    prog='d.py', description='Kaitag dictionary tools')
sub = parser.add_subparsers(dest='command', required=True)

p_new = sub.add_parser('new', help='create a new entry file')
p_new.add_argument('headword', help='headword for the new entry')

p_val = sub.add_parser(
    'validate', help='validate entries: structure, tags, refs, schema')
p_val.add_argument('letters', nargs='*',
                   help='letter folders to check (default: all)')

sub.add_parser('export', help='build all export formats')

# 'new' takes a headword that may start with '-' (affix entries) — treat
# everything after 'new' as positional.
if len(sys.argv) > 1 and sys.argv[1] == 'new' and '--' not in sys.argv[2:]:
    sys.argv.insert(2, '--')

args = parser.parse_args()

if args.command == 'new':
    from new import new
    new(args.headword)
elif args.command == 'validate':
    from validate import validate
    sys.exit(validate(args.letters))
elif args.command == 'export':
    from export import main
    main()
