# Aliasmate Configuration Documentation

**Aliasmate** is a command-line tool that uses JSON or YAML configuration files to perform alias substitutions and
execute commands. This documentation provides an in-depth explanation of how to create and use configuration files
with Aliasmate to simplify and customize command-line operations.

## Table of Contents

- [Configuration File Structure](#configuration-file-structure)
  - [Top-Level Keys](#top-level-keys)
  - [Example Configuration Files](#example-configuration-files)
- [Configuration Options](#configuration-options)
  - [`application`](#application)
  - [`alias`](#alias)
- [Creating Aliases](#creating-aliases)
  - [Single-Word Aliases](#single-word-aliases)
  - [Multi-Word Aliases](#multi-word-aliases)
  - [Nested Aliases](#nested-aliases)
- [Using the Configuration File](#using-the-configuration-file)
  - [Command-Line Invocation](#command-line-invocation)
  - [Alias Integration](#alias-integration)
- [Examples](#examples)
  - [Grep Configuration Example](#grep-configuration-example)
  - [Curl Configuration Example](#curl-configuration-example)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Configuration File Structure

Aliasmate configuration files are written in either JSON or YAML format. They define how input arguments
are transformed into commands by specifying aliases and other options.

All arguments that are not recognized from configuration file will be given to the application as is

### Top-Level Keys

The configuration file consists of top-level keys:

- `application`: *(Required)* The base command or application to be executed.
- `alias`: *(Optional)* A dictionary mapping phrases to their substitutions.

### Example Configuration Files

#### JSON Example

```json
{
  "application": "grep",
  "alias": {
    "ignore case": "-i",
    "recursive": "-r",
    "line number": "-n"
  }
}
```

#### YAML Example

```yaml
---
application: grep
alias:
  ignore case: -i
  recursive: -r
  line number: -n
```

#### YAML for cantools UDS

```yaml
---
application: 'cantools'

alias:
  # UDS Operations
  read dtc: 'decode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x19'
  clear dtc: 'encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x14'
  read data: 'decode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x22 --data-identifier'
  write data: 'encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x2E --data-identifier'

  # General CAN Operations
  send message: 'send --frame-id'
  receive messages: 'monitor'

  # Specific Data Identifiers (DIDs)
  engine rpm: '0x0C'
  vehicle speed: '0x0D'
  coolant temp: '0x05'

  # Diagnostic Session Control
  default session: 'encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x10 --session 0x01'
  programming session: 'encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x10 --session 0x02'

  # Security Access
  request seed: 'encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x27 --sub-function 0x01'
  send key: 'encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x27 --sub-function 0x02 --key'

  # Additional Options
  interface can0: '--channel can0'
  interface can1: '--channel can1'
  timeout 1000ms: '--timeout 1000'
  verbose: '--verbose'

  # Advanced Usage
  full diagnostic: 'encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x10 --session 0x02 && encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x27 --sub-function 0x01 && encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x27 --sub-function 0x02 --key'

aliasmate:
  verbose: True # always print command for execution
  concatenate_symbols: "++" # use ++ to concatenate multiple arguments
```

```bash
$ alias uds="aliasmate -c cantools_aliases.yaml --"
$ uds interface can0 read dtc
Command for execution:
cantools --channel can0 decode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x19

$ uds interface can0 programming session
Command for execution:
cantools --channel can0 encode --database uds.dbc --frame-id 0x7DF --udsoncan-service 0x10 --session 0x02
```
---

## Configuration Options

### `application`

- **Type:** String
- **Description:** The base command or application to execute. This can include command-line options and arguments.
- **Example:** `"grep"` or `"java -jar myapp.jar"`

### `alias`

- **Type:** Dictionary (Mapping)
- **Description:** A set of key-value pairs where each key is a phrase to be matched in the input arguments, and the value is the substitution.
- **Supports:** Single-word and multi-word keys.

**Example:**

```json
"alias": {
  "ignore case": "-i",
  "read version": "read f1ab",
  "app2": "doip 10"
}
```

---

## Creating Aliases

Aliases allow you to simplify and shorten complex command-line arguments by mapping them to intuitive phrases.

### Single-Word Aliases

**Definition:**

```json
"alias": {
  "verbose": "-v",
  "help": "--help"
}
```

**Usage:**

- Input: `verbose`
- Substitution: `-v`

### Multi-Word Aliases

Aliasmate supports aliases that consist of multiple words.

**Definition:**

```json
"alias": {
  "ignore case": "-i",
  "read version": "read f1ab"
}
```

**Usage:**

- Input: `ignore case`
- Substitution: `-i`

### Nested Aliases

Aliases can be nested or combined to build complex commands.

**Definition:**

```json
"alias": {
  "app2": "doip 10",
  "read version": "read f1ab"
}
```

**Usage:**

- Input: `app2 read version`
- Substitution: `doip 10 read f1ab`

---

## Using the Configuration File

### Command-Line Invocation

To use Aliasmate with a configuration file, pass the `-c` or `--config` option followed by the path to your configuration file.

**Syntax:**

```bash
aliasmate -c config.json -- [arguments to process]
```

**Example:**

```bash
aliasmate -c grep_aliases.json -- ignore case 'pattern' file.txt
```

### Alias Integration

For convenience, you can create a shell alias to simplify the invocation.

**Example:**

```bash
alias grepmate="aliasmate -c grep_aliases.json --"
```

Now, you can use `grepmate` as a shortcut:

```bash
grepmate ignore case 'pattern' file.txt
```

---

## Examples

### Grep Configuration Example

**Configuration File: `grep_aliases.json`**

```json
{
  "application": "grep",
  "alias": {
    "ignore case": "-i",
    "recursive": "-r",
    "line number": "-n",
    "word": "-w",
    "count": "-c"
  }
}
```

**Usage:**

```bash
alias grepmate="aliasmate -c grep_aliases.json --"

grepmate ignore case word 'error' /var/log/syslog
```

**Resulting Command:**

```bash
grep -i -w 'error' /var/log/syslog
```

### Curl Configuration Example

**Configuration File: `curl_aliases.json`**

```json
{
  "application": "curl",
  "alias": {
    "get": "-X GET",
    "post": "-X POST",
    "header": "-H",
    "data": "-d",
    "silent": "-s",
    "output": "-o"
  }
}
```

**Usage:**

```bash
alias curlmate="aliasmate -c curl_aliases.json --"

curlmate post header 'Content-Type: application/json' data '{"name":"John"}' 'https://api.example.com/users'
```

**Resulting Command:**

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"name":"John"}' 'https://api.example.com/users'
```

---

## Best Practices

- **Use Descriptive Aliases:** Choose aliases that are intuitive and self-explanatory.
- **Avoid Conflicts:** Ensure that your aliases do not conflict with actual command arguments.
- **Test Configurations:** Validate your configuration files with sample commands to ensure correct substitutions.

---

## Troubleshooting

- **Alias Not Substituted:**
  - **Cause:** The input phrase does not match any key in the `alias` dictionary.
  - **Solution:** Verify that the input matches exactly, including spaces and case (if case-sensitive).

- **Command Execution Fails:**
  - **Cause:** The constructed command is incorrect or the application encounters an error.
  - **Solution:** Use the `--verbose` or `--show-alias` option to inspect the command being executed.

- **YAML Support Error:**
  - **Cause:** PyYAML is not installed.
  - **Solution:** Install PyYAML using `pip install PyYAML` or include it as an extra dependency when installing Aliasmate: `pip install aliasmate[yaml]`.

- **Invalid Configuration File:**
  - **Cause:** Syntax errors or incorrect structure in the configuration file.
  - **Solution:** Validate the JSON or YAML syntax using online validators or linters.

---

**Aliasmate** empowers you to streamline complex command-line operations by using customizable aliases defined in configuration files. By understanding and utilizing the options available, you can tailor the tool to fit your workflow and enhance productivity.

For further assistance or to report issues, please refer to the project's repository or contact the maintainer.

Happy automating!
