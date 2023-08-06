# $title Preprocessor for Foliant

Description of the preprocessor.

## Installation

```shell
$ pip install foliantcontrib.$slug
```


## Config

To enable the preprocessor, add `$slug` to `preprocessors` section in the project config:

```yaml
preprocessors:
  - $slug
```

The preprocessor has a number of options:

```yaml
preprocessors:
  - $slug:
      option: value
```

`option`
:   Option description.


## Usage

Explain how your preprocessor should be used in Foliant projects. Provide Markdown samples. If the preprocessor registers tags, provide examples of their usage.

!!! important

    In order to omit processing of the tags in this file, use `<<tag></tag>` syntax:

    ```markdown
    <<$slug option="value">body</$slug>
    ```
