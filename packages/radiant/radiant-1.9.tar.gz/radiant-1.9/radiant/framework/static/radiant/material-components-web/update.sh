#!/usr/bin/bash

echo "Removing old files"
rm material-components-web.min.css
rm material-components-web.min.js
echo "Downloading new files"
wget https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css
wget https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js
echo "Done"