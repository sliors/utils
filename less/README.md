# Summary

Some improvements for `less` usability
1. Syntax highlighting via source-highlight or pygments
1. Open compressed files via lesspipe

# Installation

## Install required programs

### Mac

```shell
brew install lesspipe source-highlight pygments
```

### CentOS

```shell
sudo yum install -y source-highlight python-pygments
```

## Configure `LESSOPEN` env var

Add the following line to your environment variables, e.g., in `~/.bashrc`, `~/.zshrc`.

```
export LESSOPEN="|lesspipe.sh %s"
```

## Copy lessfilter to home folder

```shell
curl -s -o ~/.lessfilter https://raw.githubusercontent.com/sliors/utils/master/less/lessfilter
```

By default, `source-highlight` is used.

To configure the coloring tool, set env var `LESS_COLOR_CMD` to either `source-highlight` or `pygmentize`.
