haydnenthusiasts.org
====================

Haydn Enthusiasts website. [Visit it](http://haydnenthusiasts.org/).

to build:
```
cd build
python build.py
```

to deploy:
```
cd site
s3cmd sync . s3://www.haydnenthusiasts.org/ --acl-public
```
