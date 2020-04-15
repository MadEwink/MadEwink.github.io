# Small SSG

## Introduction

This is a small SSG I develop in python. The goal is to have a simple tool that does what I need it to do for this site.

## How to use it

Place your templates with commands in a folder and the files to include in another folder.
Set the `rootDir`, `templateDir` and `includeDir` variables in parser.py. Please note that `templateDir` and `includeDir` are paths relative to `rootDir`.
Run `python3 parser.py`, and the parser will go through all files in the template directory, interprete commands in it, and write the result in `rootDir`, creating folders if needed.
Please note that putting folders named `templateDir` or `includeDir` inside `templateDir` may result in either interesting or catastrophic results.
The parser will ignore all directory or file which name begins with '.' or '_'.

## Available commands

- [x] include : `{% include filename %}` include a file
- [ ] unknown name : `{% command_name command_args %}` create project list in index from a data file

