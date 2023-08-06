# pysass

A simple wrapper on
[libsass-python pysassc](https://sass.github.io/libsass-python/pysassc.html)
to add watch capability using watchdog.

## Features

- add `-w` and `--watch` flags to `pysassc` command.
- watch included directories and source directory recursively.
- only watch `*.scss` files.
- throttling.

## Install

```
$ pip install pysass
```

## Usage

Use `pysass` command instead of `pysassc` in order to be able to use `-w` or
`--watch` flag additionaly to those provided by
[libsass-python pysassc](https://sass.github.io/libsass-python/pysassc.html)
to be able to watch included directories and source directory recursively.

eg.

```
$ pysass -t compressed -I node_modules/skeleton-scss/scss/ \
	-m ./project/src/main.scss ./project/dist/style.css --watch
```
