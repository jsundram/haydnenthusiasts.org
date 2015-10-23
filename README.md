haydnenthusiasts.org
====================

Haydn Enthusiasts website. [Visit it](http://haydnenthusiasts.org/).

to build:
```
python build.py
```

to watch
```
./watch.sh
```

to deploy:
```
cd site-deploy
s3cmd sync . s3://www.haydnenthusiasts.org/ --acl-public
```
