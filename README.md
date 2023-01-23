# Basic Repo Template

This is a basic template repository for a python project. 

Change the `package_name` in: `pyproject.toml` to the name of your package (doing a global search and repolace for the default string `basic_repo_template`.


You'll also want to change the `name`, `email` etc in `pyproject.toml` and `{repository_name}.__init__.py` to your own details.

## Publishing to PyPi (to make it pip installable)

NOTE - These instructions haven't been tested yet, this is placeholder text (written 2023-01-19)

You'll need to create a PyPi account and then create an API token for the Github Action configured in the file: `.github/workflows/publish_to_pypi_when_new_tag_is_pushed_to_main.yml` 

These instructions may help you set that up! https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/