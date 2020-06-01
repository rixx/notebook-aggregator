Notebook Aggregator
-------------------

This is the data source powering [notebooks.rixx.de](https://notebooks.rixx.de), an aggregator website for "notebook
blogs". Notebook blogs are small personal blogs, usually intended for daily or frequent writing practice.

Add your blog
-------------

There are a bunch of ways to add your blog to the website:

- Ping [@rixxtr](https://twitter.com/rixxtr) on Twitter with your blog info
- If you have a GitHub account, [open an issue](https://github.com/rixx/notebook-aggregator/issues/new/choose)
- If you have a GitHub account and know JSON, [open a
  PR](https://github.com/rixx/notebook-aggregator/blob/master/_data/blogs.json). Not all keys are required, automated
  testing will let you know if something is amiss.

Development
-----------

If you want to run this locally or contribute, start a Python virtualenv, run ``pip install -e .``, and you're in
business. `notebooks build` will then render the page into the `_html` directory.

The general layout is in the `templates` directory, build scripts are in `scripts`.
