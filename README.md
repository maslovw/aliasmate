# AliasMate

**AliasMate** is a command-line tool that allows you to execute commands based on configuration files containing aliases. It simplifies complex commands by providing a readable and configurable way to use application aliases and arguments.

## Features

- **Supports JSON and YAML configuration files**.
- **Alias translation**: You can define aliases for commands and their arguments in the config file.
- **Multiple arguments**: Supports multiple arguments after the alias.
- **Combines application name, alias, and extra arguments** into a single command.
- **Error handling**: Exits with the external command's status code.

## Installation

To install and run **AliasMate**, you need to have [Rust](https://www.rust-lang.org/tools/install) installed. Once Rust is installed, you can build and run the application.

1. Clone the repository:
    ```bash
    git clone https://github.com/maslovw/aliasmate.git
    ```

2. Navigate to the project directory:
    ```bash
    cd aliasmate
    ```

3. Build the project:
    ```bash
    cargo build --release
    ```

4. Run the application:
    ```bash
    ./target/release/aliasmate -c config.json -- alias [additional arguments]
    ```

## Usage

### Configuration File

The configuration file can be in either JSON or YAML format. It defines the application to be executed and the aliases for the command arguments.

Here’s an example `config.json` file:

```json
{
    "application": "mount",
    "alias": {
        "myserver": "/media/myserver",
        "readwrite": "-o rw"
    }
}
```

### Example Command

```bash
aliasmate -c config.json -- myserver readwrite -t nfs
```

This command will execute:

```bash
mount /media/myserver -o rw -t nfs
```

- `myserver` is replaced by `/media/myserver` based on the alias defined in the config file.
- `readwrite` is replaced by `-o rw`.
- Any additional arguments (like `-t nfs`) are appended to the command.

### Arguments

- `-c, --config <FILE>`: Specifies the configuration file (JSON or YAML).
- `alias`: An alias defined in the configuration file.
- Additional arguments (after `--`) are passed directly to the command.

### Exit Status

**AliasMate** will return the exit status of the executed command:
- `0`: Success (command executed successfully).
- Non-zero: Error (command failed, with the corresponding exit code).

---

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests to improve the tool.

---

## Author

Developed by [Slava Maslov](https://github.com/maslovw).

---

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
