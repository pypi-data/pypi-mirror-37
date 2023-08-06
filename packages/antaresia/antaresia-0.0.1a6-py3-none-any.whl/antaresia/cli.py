from typing import Dict, List, Optional
import json
import sys
import argparse

from .exceptions import AntaresiaException
from .loaders import load


def key_val_to_dict(pairs: Optional[List[str]]) -> Dict:
    """
    Converts KEY=VALUE pairs into a {KEY: VALUE, ...} dict
    """
    # TODO error handling
    if not pairs:
        return {}
    variable_dict = {}
    for pair in pairs:
        key, value = pair.split("=", 1)
        variable_dict[key] = value
    return variable_dict


def main():

    parser = argparse.ArgumentParser(description="Configuration for Humans.")
    parser.add_argument(
        "--variable",
        "-v",
        dest="variables",
        action="append",
        help="Variables to pass to the configuration file",
    )
    parser.add_argument(
        "--allow-import",
        "-i",
        dest="allowed_imports",
        action="append",
        help="Imports allowed in the configuration file",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        dest="timeout",
        type=float,
        help="How many seconds to wait for the server to send data before giving up",
    )
    parser.add_argument("filename", metavar="FILENAME", help="Configuration File")
    args = parser.parse_args()
    
    output_is_piped = not sys.stdout.isatty()
    try:
        generated = load(
            args.filename,
            variables=key_val_to_dict(args.variables),
            allowed_imports=args.allowed_imports,
            timeout=args.timeout,
        )
        if output_is_piped:
            print(json.dumps(generated))
        else:
            print(json.dumps(generated, indent=2))
    except AntaresiaException as exception:
        sys.exit(exception)
