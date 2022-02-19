from setuptools import setup

setup(
    name="notebook-aggregator",
    author="Tobias Kunze",
    author_email="r@rixx.de",
    url="https://github.com/rixx/notebook-aggregator",
    packages=["scripts"],
    entry_points="""
        [console_scripts]
        notebooks=scripts.cli:cli
    """,
    install_requires=[
        "click",
        "feedparser",
        "jinja2==3.0.*",
        "markdown==3.1.*",
        "python-dateutil",
        "requests",
    ],
)
