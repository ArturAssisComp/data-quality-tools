[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->

<a id="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/ArturAssisComp/data-quality-tools.git">
    <img src="images/logo.png" alt="Logo" width="300" height="300">
  </a>

  <h3 align="center">Data Quality Tool</h3>

  <p align="center">
    A simple and easy to use CLI to measure data quaility of structured data.
    <br />
    <a href="#documentation"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ArturAssisComp/data-quality-tools/issues">Report Bug</a>
    <br/>
    <a href="https://github.com/ArturAssisComp/data-quality-tools/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
<summary>Table of Contents</summary>

- [Description](#description)
- [How to contribute](#how-is-a-contribution-made)
- [Requirements](#requirements)
- [Using Data Quality Tools](#how-to-use-data-quality-tools)
   - [Example](#example-of-usage)
- [Invoke Usage](#invoke-usage)
   - [Clean](#clean)
      - [Opriont](#options)
   - [Test](#test)
      - [Options](#options-1)
      - [Examples](#examples)
   - [Setup Virtual Environment](#setup-virtual-environment)
- [Documentation](#documentation)
    <details>

    - [Overview](#overview)
    - [JSON Structure](#menu-json-structure)

    </details>
</details>




<p align="right">(<a href="#readme-top">back to top</a>)</p>






# Description 

Data Quality Tool is a set CLI tools developed for the evaluation of data quality 
of structured data. The tools emphasize functionality and user experience, 
producing clear data quality insights. Users are advised that the system has been 
structured for ease of installation and straightforward application.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# How is a contribution made?

1. Create a branch from an issue ();

2. Clone the repository: 
```bash
git clone  https://github.com/ArturAssisComp/data-quality-tools.git
```
3. Change to the desired branch: 
```bash
cd data-quality-tools
git checkout <branch-name>
```
4. For each meaningful change, make a commit;

-> Fist, add the files that were changed: 
```bash
git add <filename1> <filename2> ... <filenameN>
```
-> Commit the changes: 
```bash
git commit -m "Implemented function foo()"
```
5. Push the changes: 
```bash
git push origin <name-of-the-branch>
```
6. If more changes are necessary, go to 4. Else,
   go to 7;
7. Create a pull request and assign someone to review the changes
   that were made in the branch;

=> Other useful commands:

Check the history of commits
```bash
git log
```
Check the status of the repository
```bash
git status
```
Get changes from remote repository from branch master
```bash
git pull origin <master-branch-name>
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Requirements




<p align="right">(<a href="#readme-top">back to top</a>)</p>

# How to use data-quality-tools 


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Example of usage


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Invoke Usage

### Clean
Clean up build artifacts and temporary files.
```
invoke clean 
```
#### Options:
- `--venv`: Clean up the virtual environment venv (default: false)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Test
Run tests for the project.
```
invoke test [--target=<test_target>]
```
#### Options:
- `--target`: The specific test or test directory to run. (default: None, runs all tests)

#### Examples:
```
invoke test --target=tests/test_module.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Setup Virtual Environment
Create a virtual environment and install dependencies.
```
invoke setupVenv
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


# Documentation

## Overview




<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Menu JSON Structure


<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- MARKDOWN LINKS & IMAGES -->

[issues-shield]: https://img.shields.io/github/issues/ArturAssisComp/data-quality-tools?logo=github&style=for-the-badge
[issues-url]: https://github.com/ArturAssisComp/data-quality-tools/issues

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/ArturAssisComp/data-quality-tools/blob/master/LICENSE