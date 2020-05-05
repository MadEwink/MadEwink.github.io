# Small SSG

## Introduction

This is a small SSG I develop in python. The goal is to have a simple tool that does what I need it to do for this site.

## How to use it

Place your templates with commands in a folder and the files to include in another folder.
Set the `rootDir`, `templateDir` and `includeDir` variables in parser.py. Please note that `templateDir` and `includeDir` are paths relative to `rootDir`.
Run `python3 parser.py`, and the parser will go through all files in the template directory, interprete commands in it, and write the result in `rootDir`, creating folders if needed.
Please note that putting folders named `templateDir` or `includeDir` inside `templateDir` may result in either interesting or catastrophic results.
The parser will ignore all directory or file which name begins with '.' or '_'.
For now, it is quite annoying that a default value is always required for `{{ arg=def_val }}` but changing this might require deep changes, that I don't want to spend time on. I might work on this if I find it too annoying.

## Available commands

- [x] include : `{% include file_name=filename arg=val arg2="value with spaces" %}` include a file, replacing all `{{ arg=def_val }}` by `val`
- [x] make posts : `{% make-posts %}` create project list in index from files in `includeDir`/projects_data on template `includeDir`/project_post.html
- [x] load arguments : `{% load-arguments file_name=filename %}` load arguments from a file, allowing use of `{{ arg=def_val }}` in the template file

