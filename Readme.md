# Bubble          ⚪ 

![GitHub Actions (Tests)](https://github.com/hamishgibbs/bubble/workflows/Tests/badge.svg)

Automate your makefile automation.

A Python CLI for scaffolding research projects.

### Features:

* Scaffold Python and R files to support command line arguments and interactive coding
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
 bubble make
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

Made with :heart:
