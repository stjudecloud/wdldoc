<p align="center">
  <h1 align="center">
  wdldoc
  </h1>

  <p align="center">
    Convert WDL documentation to Markdown for rendering.
    <br />
    <a href="https://github.com/stjudecloud/wdldoc/issues">Request Feature</a>
    ·
    <a href="https://github.com/stjudecloud/wdldoc/issues">Report Bug</a>
    ·
    ⭐ Consider starring the repo! ⭐
    <br />
  </p>
</p>

## 📚 Getting Started

For an example of what the results can look like, check out the [GitHub Pages](https://stjudecloud.github.io/workflows/) for the [St Jude Cloud Workflows](https://github.com/stjudecloud/workflows) repo! The documentation is automatically built for each release using `wdldoc`.

### Installation

wdldoc is only available for Python 3.8 or higher.

Suggested install method:

```bash
conda create -n wdldoc python=3.8
conda activate wdldoc
pip install wdldoc
```

## Usage

wdldoc is designed to be simple, and require as little work as possible. Once installed, simply call `wdldoc .` at the root of your WDL project, and Markdown files will be generated in the `./documentation` directory for each WDL file found. There are `tasks/` and `workflows/` subdirectories, with documentation for WDL workflow files in `workflows/`, and documentation for WDL task files in `tasks/`.

Any valid WDL file will have the inputs, outputs, and meta information individually documented for all its tasks and workflows. There's no need to conform to any standards we dictate; if it runs, we'll document it.

Any strings found in meta fields will be treated as Markdown, so feel free to add custom bolding, italicizing, code snippets, etc.

If there's any information you want to include for a file that doesn't fit into a meta field of one of it's tasks or workflows, you can include a header section of your WDL file, and we'll convert it to Markdown and prepend it to the documentation. This is a good place to document the uses for the file and any licensing information. Simply start a line with `##` followed by a space, and the rest of the line will be parsed as Markdown. There's no limit to the number of header lines. It's good practice to break up the header into sections using Markdown titles.

```text
usage: wdldoc [-h] [-o OUTPUT_DIRECTORY] [-d DESCRIPTION] [-c CHOICES] [-v] [--debug] sources [sources ...]

Generate clean WDL documentation from source.

positional arguments:
  sources               Top level directories to search for WDL files, or the WDL files themselves.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Directory to store markdown files. Default is `./documentation`
  -d DESCRIPTION, --description DESCRIPTION
                        If parameter meta fields use a JSON object, the key for the field containing the input description. Default is 'help'. Ignored if only strings are used.
  -c CHOICES, --choices CHOICES
                        If parameter meta fields use a JSON object, the key for the field containing the input choices. Default is 'choices'. Ignored if only strings are used.
  -v, --verbose         Sets the log level to INFO.
  --debug               Sets the log level to DEBUG.
```

Either directories or individual files can be supplied. When directories are supplied,
wdldoc will recursively search the input directories searching for all `.wdl` files, and generate documentation for them.

WDL `parameter_meta` info can be anything that conforms to the WDL spec, but we recommend one of two formats. The first is simply `input_name: "descriptive string"`. The other is a JSON object containing a description key with a string value and optionally a choices key with a list of options. The value of the "description" and "choices" keys can be specified with the `--description` and `--choices` arguments. Below is an example of both formats in one parameter meta block.

```text
parameter_meta {
    in_bams: {
        help: "Provide bams to run for comparison"
    }
    tissue_type: {
        help: "Provide the tissue type to compare against",
        choices: ['blood', 'brain', 'solid']
    }
    output_filename: "Name for the output HTML t-SNE plot"
}
```

## 🖥️ Development

If you are interested in contributing to the code, please first review
our [CONTRIBUTING.md][contributing-md] document. To bootstrap a
development environment, please use the following commands.

```bash
# Clone the repository
git clone git@github.com:stjudecloud/wdldoc.git
cd wdldoc

# Install the project using poetry
poetry install

# Ensure pre-commit is installed to automatically format
# code using `black`.
brew install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

## 📝 License

Copyright © 2020 [St. Jude Cloud Team](https://github.com/stjudecloud).

This project is [MIT][license-md] licensed.

[contributing-md]: https://github.com/stjudecloud/wdldoc/blob/master/CONTRIBUTING.md
[license-md]: https://github.com/stjudecloud/wdldoc/blob/master/LICENSE.md
