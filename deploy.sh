#!/bin/bash

cd site-deploy
s3cmd sync . s3://www.haydnenthusiasts.org/ --acl-public
