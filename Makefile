all: site

site:
	python build/build.py

deploy:
	s3cmd sync site s3://www.haydnenthusiasts.org/ --acl-public --dry-run

debug:
	ls build
