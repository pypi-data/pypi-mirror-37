# Webviz petroleum technology plugins

[`webviz-petech`](https://github.com/Statoil/webviz) contains `webviz`plugins
relevant for petroleum technology. Specific plugins might at some later
point in time be transferred to the main
[webviz repository](https://github.com/Statoil/webviz).

From a user point of view, plugins are imported similarly regardless of it
being one from the main repository or "pure plugin repositories" like this one.
After installation, e.g. the history match visualization from this repository
can be imported as
```python
from webviz.page_elements import HistoryMatch
```
To compare, the `Map` visualization from the main repository is imported as
```python
from webviz.page_elements import Map
```
