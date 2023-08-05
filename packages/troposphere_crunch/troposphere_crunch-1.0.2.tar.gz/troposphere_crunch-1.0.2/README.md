# troposphere-crunch
A tool to compile and (optionally) deploy Troposphere templates with AWS CLI and a very opinionated structure.

## Installation

Install through pip/pipenv/poetry/whatever as usual. It's [on
PyPi](https://pypi.org/project/troposphere_crunch/).

## Usage

You'll need a `stacks.toml` file that defines the following:

- `module`, an importable Python module path (relative to current working
  directory or otherwise within your `PYTHONPATH`) which contains a variable
  `template`, which is a Troposphere `Template` instance.

- `capabilities` (optional): a list of `awscli` capabilities, ex.
  `['CAPABILITY_IAM', 'CAPABILITY_NAMED_IAM']`

- `region` (optional, default=`us-west-2`): `awscli`-compatible region string

- `output_dir` (optional, default=`cloudformation`): output directory for the
  compiled JSON templates

You'll use this file as `CONFIG`. From here, refer to the `--help` output:

```
usage: troposphere-crunch [-h] -c CONFIG [-C] [-d] [-o OUTPUT_DIR]

A tool to compile and (optionally) deploy Troposphere templates with AWS CLI
and a very opinionated structure

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to TOML config file
  -C, --clean           remove output_dir before building templates
  -d, --deploy          after building, actually deploy stacks with awscli
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        default output directory (overridable per stack in
                        config)
```

## License

MIT License

Copyright (c) 2018 Josh Klar <josh@klar.sh>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
