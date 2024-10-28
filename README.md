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

now that the site is using cloudfront for https, you may need to force an invalidation
in order for content to update after deploying to s3, something along the lines of:
```
aws cloudfront create-invalidation --distribution-id EA8YGAHXI8LCE --paths "/index.html"
```

### To avoid the build / watch / deploy steps above:
```
cp post-commit.py ./.git/hooks/post-commit
chmod +x ./.git/hooks/post-commit
```
Then, the site will build, deploy, and invalidate paths appropriately after each commit.

### to add new events:
Update `data.json`. 

Keep in mind that the links to fb hosted images usually break, and the practice we've adopted has been downloading the photo from the url we listed in `data.json` and keeping the same name, but storing it in static/assets/event_photos. This is weird, but its how things currently work. 
