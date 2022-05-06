# Summary

Some improvements for [`less`](https://man7.org/linux/man-pages/man1/less.1.html) usability
1. Syntax highlighting via [`source-highlight`](https://www.gnu.org/software/src-highlite/) or [`pygments`](https://pygments.org/)
1. Open compressed files via [`lesspipe`](https://github.com/wofr06/lesspipe)

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

```shell
export LESSOPEN="||lesspipe.sh %s"
```

## Copy `lessfilter` to home folder

```shell
curl -s -o ~/.lessfilter https://raw.githubusercontent.com/sliors/utils/master/less/lessfilter && chmod +x ~/.lessfilter
```

By default, `source-highlight` is used as the coloring tool.

To configure the coloring tool, set env var `LESS_COLOR_CMD` to either `source-highlight` or `pygmentize`. For example:

```shell
export LESS_COLOR_CMD=pygmentize
```
