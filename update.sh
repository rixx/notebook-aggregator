#!/bin/zsh

cd $0:A(:h)
git pull origin master -q
/home/rixx/.local/share/virtualenvs/notebook-aggregator/bin/pip install -Ue .
/home/rixx/.local/share/virtualenvs/notebook-aggregator/bin/notebooks build
