# Subset

This CLI extension adds the command `subset` that generates a config file for a subset (i.e. a detached part) of the Foliant project. The command uses:

* the part of config that is common (i.e. single) for the whole Foliant project;
* the part of config that is individual for each subset. The Foliant project may include multiple subsets that are defined by partial config files.

The command `subset` takes a path to the subset directory as a mandatory command line parameter.

The command `subset` reads the partial config of the subset, then optionally rewrites the paths of Markdown files that specified there in the `chapters` section, and then joins the result with the common part of the whole Foliant project config. Finally, the full config file will be written. The prepared full config file allows to build a certain subset of the Foliant project with the `make` command.

## Installation

To install the extension, use the command:

```bash
$ pip install foliantcontrib.subset
```

## Usage

To get the list of all necessary parameters and available options, run `foliant subset --help`:

```bash
$ foliant subset --help
usage: foliant subset [-h] [-p PROJECT_DIR] [-s SRC_DIR] [-n] [-c CONFIG] [-d]
                      SUBPATH

Generate subset config file using partial data from SUBPATH.

positional arguments:
  SUBPATH

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT_DIR, --project-dir PROJECT_DIR
                        Path to the Foliant project root directory, default './'
  -s SRC_DIR, --src-dir SRC_DIR
                        Path to the Foliant project source directory, default './src/'
  -n, --no-rewrite      Do not rewrite the paths of Markdown files in the partial config
  -c CONFIG, --config CONFIG
                        Name of config file of the Foliant project, default 'foliant.yml'
  -d, --debug           Log all events during build. If not set, only warnings and errors are logged
```

In most cases it’s enough to use the default values of optional parameters. You need to specify only the `SUBPATH`—the directory that should be located inside the Foliant project source directory.

Initially the Foliant project may have no config file, because the Subset CLI extension can generate it. However, the names of partial config files are based on the whole Foliant project config file name. Suppose you use the default Foliant project config file name `foliant.yml`. Then:

* `foliant.yml.common` is the name of the file that contains the common part of config;
* `foliant.yml.partial` is the name of multiple files that contain the individual parts of the config of each subset.

The file `foliant.yml.common` should be located in the Foliant project root directory.

The files `foliant.yml.partial` must be located in the directories of the subsets.

Your Foliant project tree may look so:

```bash
$ tree
.
├── foliant.yml.common
└── src
    ├── group_1
    │   ├── product_1
    │   │   └── feature_1
    │   │       ├── foliant.yml.partial
    │   │       └── index.md
    │   └── product_2
    │       ├── foliant.yml.partial
    │       └── main.md
    └── group_2
        ├── foliant.yml.partial
        └── intro.md
```

The command `foliant subset group_1/product_1/feautre_1` will join the files `./src/group_1/product_1/feautre_1/foliant.yml.partial` and `./foliant.yml.common`, and write the result into the file `./foliant.yml`.

Let’s look at some examples.

The content of the file `./src/group_1/product_1/feautre_1/foliant.yml.partial`:

```yaml
title: &title Group 1, Product 1, Feature 1

subtitle: &subtitle Technical Specification

version: &version 1.0

chapters:
    - index.md
```

The content of the file `./foliant.yml.common`:

```yaml
backend_config:
    pandoc:
        template: !path /somewhere/template.tex
        reference_docx: !path /somewhere/reference.docx
        vars:
            title: *title
            version: *version
            subtitle: *subtitle
        params:
            pdf_engine: xelatex
```

The content of newly generated file `./foliant.yml`:

```yaml
title: &title Group 1, Product 1, Feature 1

subtitle: &subtitle Technical Specification

version: &version 1.0

chapters:
    - group_1/product_1/feautre_1/index.md

backend_config:
    pandoc:
        template: !path /somewhere/template.tex
        reference_docx: !path /somewhere/reference.docx
        vars:
            title: *title
            version: *version
            subtitle: *subtitle
        params:
            pdf_engine: xelatex
```

If the option `--no-rewrite` is not set, the paths of Markdown files that are specified in the `chapters` section of the file `./src/group_1/product_1/feautre_1/foliant.yml.partial`, will be rewritten as if these paths were relative to the directory `./src/group_1/product_1/feautre_1/`.

Otherwise, the Subset CLI extension will not rewrite the paths of Markdown files as if they were relative to `./src/` directory.

Note that the Subset CLI Extension does not parse YAML files; it only process them as plain text files. Thus:

* `foliant.yml.common` and `foliant.yml.partial` separately may be not valid, e.g. you may use in `foliant.yml.common` the variables that are defined in `foliant.yml.partial`;
* the settings from `foliant.yml.partial` do not override the settings from `foliant.yml.common`, e.g. you can’t use custom value of the setting `backend_config.pandoc.template` at the subset level.
