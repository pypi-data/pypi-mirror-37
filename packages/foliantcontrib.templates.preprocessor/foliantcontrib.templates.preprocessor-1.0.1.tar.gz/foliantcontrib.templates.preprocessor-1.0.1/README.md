# Preprocessor Template for `foliant init` Command

Template for a Foliant preprocessor. Instead of looking for an existing preprocessor, cloning it, and modifying its source, install this package and generate a preprocessor directory. As simple as:

```shell
$ foliant init -t preprocessor
```
## Installation

```shell
$ pip install foliantcontrib.templates.preprocessor
```

## Usage

```shell
$ foliant init -t preprocessor
Enter the project name: Awesome Preprocessor
✔ Generating project
─────────────────────
Project "Awesome Preprocessor" created in awesome-preprocessor
```

Or:

```shell
$ foliant init -t preprocessor -n "Awesome Preprocessor"
✔ Generating project
─────────────────────
Project "Awesome Preprocessor" created in awesome-preprocessor
```

Result:

```shell
$ tree awesome-preprocessor
.
├── changelog.md
├── foliant
│   └── preprocessors
│       └── awesome-preprocessor.py
├── LICENSE
├── README.md
└── setup.py

2 directories, 5 files
```
