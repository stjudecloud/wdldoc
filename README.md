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

### Notice

This repository is still in development!

## 📚 Getting Started

### Installation

Currently, only local setup is supported using Python 3.8 or higher:

```bash
pip install poetry>=1.0.5
poetry install
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

Copyright © 2020 [St. Jude Cloud Team](https://github.com/stjudecloud).<br />
This project is [MIT][license-md] licensed.

[contributing-md]: https://github.com/stjudecloud/wdldoc/blob/master/CONTRIBUTING.md
[license-md]: https://github.com/stjudecloud/wdldoc/blob/master/LICENSE.md
