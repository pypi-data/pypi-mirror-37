# DataFair plugin for uData

Use DataFair embeds to preview data

## Usage

Install the plugin package in you udata environement:

```bash
pip install udata-data-fair
```

Then activate it in your `udata.cfg`:

```python
PLUGINS = ['udata-data-fair']
```


## Publish

```
python setup.py sdist bdist_wheel
twine upload dist/*
```
