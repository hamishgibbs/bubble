# Bubble

![GitHub Actions (Tests)](https://github.com/hamishgibbs/bubble/workflows/Tests/badge.svg)

Automate your automation.

A Python CLI for scaffolding research projects.

### Features:

* Scaffold Python and R files for easy input/output and interactive coding
* Parse a bubble template file to generate Makefile targets

### Quickstart:

Create a new bubble project, writing a `bubble.json` configuration file.

``` {shell}
bubble init
```

Create a Makefile using a bubble template.

``` {shell}
bubble create -f Makefile
```

Create a `src` directory. Bubble assumes target files will be located in `./src` (see `bubble.json`).

``` {shell}
mkdir src
```

Create an example Python file using a bubble template.

``` {shell}
bubble create -f src/example.py
```

Extract the dependencies from this file and update the Makefile at the project root.

 ``` {shell}
 bubble makefile
 ```

`Successfully updated 1 Makefile targets. 🎂`

Success! You should see a summary of the targets that have been updated.

**Note:** Whether a Bubble template is parsed into a Makefile target is controlled by a commented string `# *** bubble make ***` at the top of each bubble template. If you don't want a file to be included in the Makefile, delete this string.

# Reference

The entry point for the bubble cli is `bubble`. For more information, use `bubble --help`

#### init

`bubble init`: Initiates a bubble project by writing a `bubble.json` configuration file.

Options:

*-root* *(--root)*: Specify the project root. Default: `os.getcwd()`.

#### create

`bubble create`: creates files from bubble templates.

Options:

*-f* *(--file)*: Path of a file to create. Accepts `Makefile`, `*.py`, and `*.R` files.
*-t* *(--tag)*: Omit the bubble file tag. Files are tagged by default.

#### make

`bubble make`: Parses bubble template files and updates Makefile targets.

Options:

*-root* *(--root)*: Specify the project root. Default: `os.getcwd()`.

# Contributions

Contributions are welcome. If you encounter problems while using this library, please [open an issue.](https://github.com/hamishgibbs/bubble/issues/new)

# How it works

This is a simple library with a limited scope. It is intended to take dependencies specified in code files and move them to a makefile to make it simple to automate the creation of research (or other) outputs.

`bubble` decides whether Makefile targets should be created from code files based on two criteria:

* Files should have a recognised file extension (the current defaults are `*.py` and `*.R`).
* Files should be specified as Makefile targets. Bubble recognises the commented string `# *** bubble make ***` in source files.

`bubble` parses dependencies specified between the `# *** bubble input start ***` and `# *** bubble input end ***` strings. Dependencies are identified within double quotes `""`. The last dependency in the list is assumed to be the output file.

Accepting command line arguments in Python files while allowing interactive coding requires the strings ``"__main__"`` and `"null"`. These strings will be ignored by `bubble`.

Made with :heart:
