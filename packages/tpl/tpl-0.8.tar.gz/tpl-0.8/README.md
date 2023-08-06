# `tpl`: Render templates with data from various sources

<p><!-- badges --><a href="https://travis-ci.com/M3t0r/tpl"><img src="https://api.travis-ci.com/M3t0r/tpl.svg?branch=master" alt="travis-ci build badge"></a></p>

You want to fill data into a template file?
```shell
tpl --yaml data.yaml template.file > rendered.file
```

You have everything already set up in your environment and now you just want to
POST it somewhere?
```shell
tpl structure.json | curl -X POST -H "Content-Type: application/json" -d@- httpbin.org/anything
```

You want to fill in a template in your CD pipeline and have access to docker?
```shell
echo "My go-to editor is {{VISUAL}} on {{OS}}" \
  | docker run --rm -i -e "VISUAL" -e "OS=$(uname)" m3t0r/tpl -
```

## Installation
`make install` or `pip install tpl`

## Input sources
`tpl` supports multiple sources:
 * YAML files (`--yaml <file>`)
 * JSON files (`--json <file>`)
 * environment variables (`--environment`)

You can specify multiple sources at once, but if a key is present in more than
one then it's value will be taken from the latter source. This can be useful if
you have default values that you want to always be present:
```shell
tpl \
  --yaml defaults.yaml \
  --json <(curl -H "Content-Type: application/json" now.httpbin.org) \
  template.jinja2 > results.html
```

# Usage
```
Usage:
  tpl [options] <template_file>
  tpl --help
  tpl --version


tpl uses the Jinja2 templating engine to render it's output. You can find the
documentation for template designers at:
    http://jinja.pocoo.org/docs/latest/templates/

If you provide multiple data sources they will be merged together. If a key is
present in more than one source the value of the source that was specified
last will be used. Nested objects will be merged with the same algorithm.

Options:
  -e, --environment    Use all environment variables as data
  --json=<file>        Load JSON data from a file or STDIN
  --yaml=<file>        Load YAML data from a file or STDIN
```
