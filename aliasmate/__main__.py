import argparse
import json
import sys
import subprocess
from pprint import pprint

VERSION='0.1.0'

try:
    import yaml
except ImportError:
    yaml = None

def split_arguments(argv):
    # Split sys.argv manually to handle '--'
    positions = [i for i, arg in enumerate(argv) if arg == '--']

    if len(positions) == 1:
        idx = positions[0]
        own_args = argv[1:idx]
        sub_args = argv[idx+1:]
    elif len(positions) >= 2:
        idx1 = positions[0]
        idx2 = positions[1]
        own_args = argv[1:idx1] + argv[idx2+1:]
        sub_args = argv[idx1+1:idx2]
    else:
        own_args = argv[1:]
        sub_args = []
    return own_args, sub_args

def main():
    own_args, sub_args = split_arguments(sys.argv)
    # Parse own_args
    parser = argparse.ArgumentParser(description='''Aliasmate: Command-line alias substitution tool
All arguments before `--` will be accepted by aliasmate
All arguments after `--` will pass substitution according to config and given to the application
It is possible to use second `--` group of arguments to pass back to aliasmate''',
                                     usage='use "%(prog)s --help',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', help='Config file (JSON or YAML)', required=True)
    parser.add_argument('-s', '--show-alias', help='print current config and the result command without execution', required=False, action='store_true')
    parser.add_argument('-v', '--verbose', help='print result command before executing', required=False, action='store_true')
    parser.add_argument("--version", action="version", version="0.1.0")
    args = parser.parse_args(own_args)

    config_file = args.config

    try:
        with open(config_file, 'r') as f:
            if config_file.endswith('.json'):
                config = json.load(f)
            elif config_file.endswith(('.yaml', '.yml')):
                if yaml is None:
                    print("YAML support is not available. Please install PyYAML.")
                    sys.exit(1)
                config = yaml.safe_load(f)
            else:
                print("Unsupported config file format. Must be .json or .yaml")
                sys.exit(1)
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

    if args.show_alias:
        pprint(config)
        print()

    application_str = config.get('application', '')
    if not application_str:
        print("No 'application' key found in config file.")
        sys.exit(1)
    alias_dict = config.get('alias', {})

    def substitute_tokens(tokens, alias_dict):
        position = 0
        output_tokens = []
        if not alias_dict:
            return tokens
        max_key_length = max(len(key.split()) for key in alias_dict.keys())
        while position < len(tokens):
            match_found = False
            for length in range(max_key_length, 0, -1):
                if position + length > len(tokens):
                    continue
                seq = tokens[position:position+length]
                seq_str = ' '.join(seq)
                if seq_str in alias_dict:
                    substitution = alias_dict[seq_str].split()
                    output_tokens.extend(substitution)
                    position += length
                    match_found = True
                    break
            if not match_found:
                output_tokens.append(tokens[position])
                position += 1
        return output_tokens

    tokens = sub_args
    output_tokens = substitute_tokens(tokens, alias_dict)
    application_tokens = application_str.split()
    final_tokens = application_tokens + output_tokens
    command_str = ' '.join(final_tokens)

    is_verbose = (args.show_alias | args.verbose)

    if is_verbose:
        print("Command for execution:")
        print(command_str)
    if args.show_alias:
        sys.exit(0)

    try:
        output = subprocess.run(command_str, shell=True, check=True)
        #os.execvp(final_tokens[0], final_tokens)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except Exception as e:
        sys.exit(1)

if __name__ == '__main__':
    main()
