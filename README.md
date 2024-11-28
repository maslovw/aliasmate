# AliasMate

**AliasMate** is a command-line tool that allows you to execute commands based on configuration files containing
aliases. It simplifies complex commands by providing a readable and configurable way to use application aliases and
arguments.

## Features

- **Supports JSON and YAML configuration files**.
- **Alias translation**: You can define aliases for commands and their arguments in the config file.
- **Multiple arguments**: Supports multiple arguments after the alias.
- **Combines application name, alias, and extra arguments** into a single command.
- **Error handling**: Exits with the external command's status code.

## Installation

`pip install aliasmate`

or

```bash
git clone https://github.com/maslovw/aliasmate.git
cd aliasmate
pip install .
```

## Usage

### Configuration File

The configuration file can be in either JSON or YAML format. It defines the application to be executed and the aliases for the command arguments.

Here’s an example `config.json` file:

```json
{
  "application": "mount",
  "alias": {
    "read only": "-o ro",
    "read write": "-o rw",
    "no execute": "-o noexec",
    "user mount": "-o user",
    "bind": "--bind",
    "verbose": "-v",
    "all": "-a",
    "remount": "-o remount",
    "loop": "-o loop"
  }
  "aliasmate": {
    "verbose": true
  }
}
```
Read more here [Configuration File Format](doc/ConfigurationFileFormat.md)

### Example Command

```bash
$ alias mountmate="aliasmate -c mount_aliases.json --"
$ sudo mountmate read only /dev/sdb1 /mnt/usb
```
This command will execute:

```bash
mount -o ro /dev/sdb1 /mnt/usb
```
It is possible to pass arguments to aliasmate with second `--` group of arguments:

```bash
$ sudo mountmate read only /dev/sdb1 /mnt/usb -- --verbose
Command for execution:
mount -o ro /dev/sdb1 /mnt/usb
```
### Another example

```json
{
  "application": "tar",
  "alias": {
    "create": "-c",
    "extract": "-x",
    "gzip": "-z",
    "bzip2": "-j",
    "file": "-f",
    "verbose": "-v",
    "list": "-t",
    "xz": "-J"
  }
}
```

```bash
$ alias tarmate="aliasmate -c tar_aliases.json --"

$ tarmate create gzip file archive.tar.gz directory/
$ tarmate extract bzip2 verbose file archive.tar.bz2
$ tarmate list xz file 'archive.tar.xz'
```

### Arguments

- `-c, --config <FILE>`: Specifies the configuration file (JSON or YAML).
- `-s`, `--show-alias`: print currently used configuration and resulting command, without execution
- `-v`, `--verbose`: print resulting command and execute it
- Additional arguments (after `--`) are passed directly to the application.
- 2nd Additional arguments (after 2nd `--`) are passed directly to the aliasmate(append to first arguments).

### Example Usage:

It is intended to use `alias` (or `.bat` for windows) for this tool

```bash
# create shell alias in .bashrc for example
alias mount="aliasmate -c ~/.config/aliasmate/mount.json --"

# call aliasmate with mount.json
mount myserver readwrite -t nfs
# this command will be translated into
# mount /media/myserver -o rw -t nfs
```

## Shell completion

### ZSH completion

add completion/aliasmate_completion.zsh to your .completion.zsh

---

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests to improve the tool.

---

## Author

Developed by [Slava Maslov](https://github.com/maslovw).

---


