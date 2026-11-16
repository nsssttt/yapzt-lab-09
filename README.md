# Lab 09 - White-Box Testing

Use Python 3.12 in a virtual environment.

```sh
python -m pip install -r requirements.txt
python -m coverage run -m pytest -q
python -m coverage report -m --fail-under=100
python -m coverage html
python cfg.py
```

Open `htmlcov/index.html` for the coverage report. `cfg.py` generates DOT graphs and a control-flow analysis. Render a graph with Graphviz, for example `dot -Tpng cfg.dot -o cfg.png`.
