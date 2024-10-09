#!/usr/bin/env python3

import argparse
import json
import sys
import os

try:
    import yaml
except ImportError:
    yaml = None

def main():
    # Split sys.argv manually to handle '--'
    if '--' in sys.argv:
        idx = sys.argv.index('--')
        own_args = sys.argv[1:idx]
        sub_args = sys.argv[idx+1:]
    else:
        own_args = sys.argv[1:]
        sub_args = []

    # Parse own_args
    parser = argparse.ArgumentParser(description="Aliasmate: Command-line alias substitution tool")
    parser.add_argument('-c', '--config', help='Config file (JSON or YAML)', required=True)
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
    print(command_str)
    os.execvp(final_tokens[0], final_tokens)

if __name__ == '__main__':
    main()
