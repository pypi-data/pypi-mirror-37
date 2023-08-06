# Subset

This CLI extension adds the command `subset` that generates a config file for a subset (i.e. a detached part) of the Foliant project. The command uses:

* the common (i.e. default, single) config file for the whole Foliant project;
* the part of config that is individual for each subset. The Foliant project may include multiple subsets that are defined by their own partial config files.

The command `subset` takes a path to the subset directory as a mandatory command line parameter.

The command `subset`:

* reads the partial config of the subset;
* optionally rewrites the paths of Markdown files that specified there in the `chapters` section;
* merges the result with the default config of the whole Foliant project config;
* finally, writes a new config file that allows to build a certain subset of the Foliant project with the `make` command.

## Installation

To install the extension, use the command:

```bash
$ pip install foliantcontrib.subset
```

## Usage

To get the list of all necessary parameters and available options, run `foliant subset --help`:

```bash
$ foliant subset --help
usage: foliant subset [-h] [-p PROJECT_DIR_PATH] [-c CONFIG] [-n] [-d] SUBPATH

Generate the config file to build the project subset from SUBPATH.

positional arguments:
  SUBPATH               Path to the subset of the Foliant project

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT_DIR, --project-dir PROJECT_DIR
                        Path to the Foliant project
  -c CONFIG, --config CONFIG
                        Name of config file of the Foliant project, default 'foliant.yml'
  -n, --no-rewrite      Do not rewrite the paths of Markdown files in the subset partial config
  -d, --debug           Log all events during build. If not set, only warnings and errors are logged
```

In most cases it’s enough to use the default values of optional parameters. You need to specify only the `SUBPATH`—the directory that should be located inside the Foliant project source directory.

Suppose you use the default settings. Then you have to prepare:

* the common (default) config file `foliant.yml` in the Foliant project root directory;
* partial config files for each subset. They also must be named `foliant.yml`, and they must be located in the directories of the subsets.

Your Foliant project tree may look so:

```bash
$ tree
.
├── foliant.yml
└── src
    ├── group_1
    │   ├── product_1
    │   │   └── feature_1
    │   │       ├── foliant.yml
    │   │       └── index.md
    │   └── product_2
    │       ├── foliant.yml
    │       └── main.md
    └── group_2
        ├── foliant.yml
        └── intro.md
```

The command `foliant subset group_1/product_1/feautre_1` will merge the files `./src/group_1/product_1/feautre_1/foliant.yml` and `./foliant.yml`, and write the result into the file `./foliant.yml.subset`.

After that you may use the command like the following to build your Foliant project:

```bash
$ foliant make pdf --config foliant.yml.subset
```

Let’s look at some examples.

The content of the common (default) file `./foliant.yml`:

```yaml
title: &title Default Title

subtitle: &subtitle Default Subtitle

version: &version 0.0

backend_config:
    pandoc:
        template: !path /somewhere/template.tex
        reference_docx: !path /somewhere/reference.docx
        vars:
            title: *title
            version: *version
            subtitle: *subtitle
            year: 2018
        params:
            pdf_engine: xelatex
```

The content of the partial config file `./src/group_1/product_1/feautre_1/foliant.yml`:

```yaml
title: &title Group 1, Product 1, Feature 1

subtitle: &subtitle Technical Specification

version: &version 1.0

chapters:
    - index.md

backend_config:
    pandoc:
        vars:
            year: 2019
```


The content of newly generated file `./foliant.yml.subset`:

```yaml
title: &title Group 1, Product 1, Feature 1
subtitle: &subtitle Technical Specification
version: &version 1.0
backend_config:
    pandoc:
        template: !path /somewhere/template.tex
        reference_docx: !path /somewhere/reference.docx
        vars:
            title: *title
            version: *version
            subtitle: *subtitle
            year: 2019
        params:
            pdf_engine: xelatex
chapters:
- b2b/order_1/feature_1/index.md
```

If the option `--no-rewrite` is not set, the paths of Markdown files that are specified in the `chapters` section of the file `./src/group_1/product_1/feautre_1/foliant.yml`, will be rewritten as if these paths were relative to the directory `./src/group_1/product_1/feautre_1/`.

Otherwise, the Subset CLI extension will not rewrite the paths of Markdown files as if they were relative to `./src/` directory.

Note that the Subset CLI Extension merges the data of the config files recursively, so any subkeys of default config may be overridden by the settings of partial config.
