# Argparse Cheat Sheet
=====================


<details>
<summary> Table of contents </summary>

- [Description](#description)
- [1. Import the module](#1-import-the-module)
- [2. Create a parser](#2-create-a-parser)
- [3. Add arguments](#3-add-arguments)
    - [Positional arguments](#positional-arguments)
    - [Optional arguments (flags)](#optional-arguments-flags)
    - [Optional arguments with values](#optional-arguments-with-values)
    - [Optional arguments with default values](#optional-arguments-with-default-values)
    - [Choice-based arguments](#choice-based-arguments)
    - [Version argument](#version-argument)
- [4. Parse arguments](#4-parse-arguments)
- [5. Access parsed arguments](#5-access-parsed-arguments)
- [6. Use arguments in your program](#6-use-arguments-in-your-program)
- [7. Display help message](#7-display-help-message)
- [For more](#for-more)

</details>




# Description

Argparse is a Python standard library module for creating command-line interfaces. It makes it easy to handle command-line arguments, providing a consistent and user-friendly experience.

This cheat sheet covers the basic usage of the argparse module, including creating a parser, defining arguments, and parsing input.


[(back-to-top)](#argparse-cheat-sheet)

# 1. Import the module
---------------------
```python
import argparse
```

[(back-to-top)](#argparse-cheat-sheet)

# 2. Create a parser
-------------------
```python
parser = argparse.ArgumentParser(description="A brief description of your program.")
```

[(back-to-top)](#argparse-cheat-sheet)

# 3. Add arguments
-----------------
## Positional arguments
```python
parser.add_argument("input_file", help="Path to the input file.")
```

[(back-to-top)](#argparse-cheat-sheet)

## Optional arguments (flags)
```python
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
```

[(back-to-top)](#argparse-cheat-sheet)

## Optional arguments with values
```python
parser.add_argument("-o", "--output", type=str, help="Path to the output file.")
```

[(back-to-top)](#argparse-cheat-sheet)

## Optional arguments with default values
```python
parser.add_argument("-n", "--num-iterations", type=int, default=10, help="Number of iterations.")
```

[(back-to-top)](#argparse-cheat-sheet)

## Choice-based arguments
```python
parser.add_argument("--mode", choices=["A", "B", "C"], help="Choose the mode (A, B, or C).")
```

[(back-to-top)](#argparse-cheat-sheet)

## Version argument
```python
parser.add_argument("--version", action="version", version="Your Program 1.0")
```

[(back-to-top)](#argparse-cheat-sheet)

# 4. Parse arguments
-------------------
```python
args = parser.parse_args()
```

[(back-to-top)](#argparse-cheat-sheet)

# 5. Access parsed arguments
---------------------------
```python
input_file = args.input_file
verbose = args.verbose
output_file = args.output
num_iterations = args.num_iterations
mode = args.mode
```

[(back-to-top)](#argparse-cheat-sheet)

# 6. Use arguments in your program
--------------------------------
```python
if verbose:
    print("Verbose mode enabled")

for i in range(num_iterations):
    # Your code here
```

[(back-to-top)](#argparse-cheat-sheet)

# 7. Display help message
------------------------
The help message is automatically generated based on the arguments defined. Users can display it by running your script with the `-h` or `--help` flag.

```
$ python your_script.py -h
```

[(back-to-top)](#argparse-cheat-sheet)

# For more
This cheat sheet provides a basic overview of argparse usage. For more information and advanced usage, refer to the official argparse documentation: https://docs.python.org/3/library/argparse.html

[(back-to-top)](#argparse-cheat-sheet)