[*view Italian version*](README_it.md)

# *html*2*py*

html2py is a tool for converting an html file in python language and viceversa.

## Features

- create a pythonic html page.

- wrap python code in a function and add imports.

- A command line interface for generating script.

- Also an API for extend functionalities, see module documenation for more details.

## Dependencies

- lxml

- yattag (for running generated scripts)

#### For testing:

- hypothesis

- pytest (or something that fetch test cases in modules)

- xmldiff

## Usage

#### Command line tool

```
usage: html2py.py [-h] -o OUTPUT [-e | -f | -c] [-s] file

Convert html file to yattag based python script.

parameters:
  file                  Html file to convert (required).
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file. By default in output there is python
                        header with imports and a function with code (required).
  -e, --no-head         Do not insert header and imports.
  -f, --no-function     Do not insert code into function
  -c, --only-code       Write only code into output. Do not insert header or
                        functions.
```

#### APIs

(see module documentation for more informations)

Html2py backend lib is composed with 4 module:

- parser

  Parse an input file and transform it into something pythonic.
  Currently it supported html and xml.
- output

  It provides 2 feature:
  - some extensible objects to represent python instructions
  - An extensible interface to write your code
- yattag

  Using parsed data and output module for writing your code.
- converter

  Essentially a connector between cli tool and the other 3 modules.

## TODO

#### Proposing for future:

Now this tool works enough, but it not working in all cases; we need lots of document for testing purposes and for finding unhandled errors.

Html2py can potentially pythonize also xml documents and xml based documents, but also other types of file, such as json or yaml.

In addition add supports to other xml tree library and not just lxml (currently supported).

#### Improve test suite:

At the moment there is a very poor test suite (only a case) and this tool, though there is very small in lines of code,  need lots of cases, samples and, why not, a random html generator.

#### Add wiki or website for documentation

Describe APIs and tools with a structured doc page instead of this readme.


