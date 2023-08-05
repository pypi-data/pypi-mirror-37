# 🛀 Cleanliness

Cleanliness is a package for doing (very) basic cleaning of text. It can be used for preprocessing input to various
natural language processing tasks.

## Install

Download the source from GitHub, then install using pip (from the repo directory):

```python
pip3 install -e .
```

## Usage

```python
from cleanliness import normalize_whitespace
clean_text = normalize_whitespace("This\ntext\t\contains  odd\n\t whitespace.")
```
