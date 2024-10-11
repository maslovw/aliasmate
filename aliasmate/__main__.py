import argparse
import json
import sys
import subprocess
import shlex

VERSION='0.1.3'

try:
    import yaml
except ImportError:
    yaml = None

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def read_and_print_file(file_path):
    print(f"Config File: {file_path}")
    try:
        with open(file_path, 'r') as file:
            for line in file:
                print(line, end='')
    except FileNotFoundError:
        eprint(f"Error: The file '{file_path}' does not exist.")
    except IOError:
        eprint(f"Error: An I/O error occurred while reading '{file_path}'.")

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

special_chars = {'|', '<', '>', '&', ';'}

def contains_special_char(s):
    return not set(s).isdisjoint(special_chars)

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
    parser.add_argument('-s', '--show-alias', '--show-config', help='print current config and the result command without execution', required=False, action='store_true')
    parser.add_argument('-v', '--verbose', help='print result command before executing', required=False, action='store_true')
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(own_args)

    config_file = args.config


    try:
        with open(config_file, 'r') as f:
            if config_file.endswith('.json'):
                config = json.load(f)
            elif config_file.endswith(('.yaml', '.yml')):
                if yaml is None:
                    eprint("YAML support is not available. Please install PyYAML.")
                    sys.exit(1)
                config = yaml.safe_load(f)
            else:
                eprint("Unsupported config file format. Must be .json or .yaml")
                sys.exit(1)
    except Exception as e:
        eprint(f"Error reading config file: {e}")
        sys.exit(1)

    config_dict = config.get('aliasmate', {})

    is_verbose = (args.show_alias | args.verbose | config_dict.get('verbose', False))

    if args.show_alias:
        read_and_print_file(config_file)
        print()

    application_str = config.get('application', '')
    if not application_str:
        eprint("No 'application' key found in config file.")
        sys.exit(1)
    alias_dict = config.get('alias', {})

    def substitute_tokens(tokens, alias_dict):
        position = 0
        output_tokens = []
        special_chars_found_wrong_placed = (False, None)
        if not alias_dict:
            return tokens, special_chars_found_wrong_placed
        max_key_length = max(len(key.split()) for key in alias_dict.keys())
        while position < len(tokens):
            match_found = False
            for length in range(max_key_length, 0, -1):
                if position + length > len(tokens):
                    continue
                seq = tokens[position:position+length]
                seq_str = ' '.join(seq)
                if seq_str in alias_dict:
                    subs_val = alias_dict[seq_str]
                    substitution = subs_val.split()
                    output_tokens.extend(substitution)
                    position += length
                    # check if substition contains flow control characters and it's not the last argument
                    if position < len(tokens):
                        if contains_special_char(subs_val):
                            special_chars_found_wrong_placed=(True, subs_val)
                    match_found = True
                    break
            if not match_found:
                output_tokens.append(tokens[position])
                position += 1
        return output_tokens, special_chars_found_wrong_placed

    tokens = sub_args
    output_tokens, wrong_placed_special_character = substitute_tokens(tokens, alias_dict)
        #raise RuntimeError(f"Found special flow handling in the middle of command: {subs_val}")
    application_tokens = application_str.split()
    final_tokens = application_tokens + output_tokens
    command_str = ' '.join(final_tokens)

    if wrong_placed_special_character[0]:
        eprint(f"ERROR: Found special flow handling in the middle of command: {wrong_placed_special_character[1]}")
        eprint(f"ERROR: result command: {command_str}")
        sys.exit(1)

    # Check for special characters not at the end
    #check_special_characters(command_str)


    if is_verbose:
        eprint("Command for execution:")
        eprint(command_str)
    if args.show_alias:
        sys.exit(0)

    try:
        subprocess.run(command_str, shell=True, check=True)
        # execvp will change current alliasmate process with executed command
        # resulting in the same PID on unix systems
        # but piping used in the config file won't be possible
        #os.execvp(final_tokens[0], final_tokens)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except Exception as e:
        sys.exit(1)

if __name__ == '__main__':
    main()
