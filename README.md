haydnenthusiasts.org
====================

Haydn Enthusiasts website. [Visit it](http://haydnenthusiasts.org/).

### to build:
```
python3 build.py
```

### to watch
```
./watch.sh
```

### to deploy:
```
./deploy.sh
```

### to add new events:
Update `data.json`. 

Keep in mind that the links to fb hosted images usually break, and the practice we've adopted has been downloading the photo from the url we listed in `data.json` and keeping the same name, but storing it in static/assets/event_photos. This is weird, but its how things currently work. 
