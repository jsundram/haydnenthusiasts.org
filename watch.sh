#!/bin/bash
watchmedo shell-command \
    --patterns="*.py;*.js;*.css;*.json;*.html;*.jpg;*.png;*.gif;*.ico" \
    --recursive \
    --command='python build.py'\
    ./templates ./static ./pages
