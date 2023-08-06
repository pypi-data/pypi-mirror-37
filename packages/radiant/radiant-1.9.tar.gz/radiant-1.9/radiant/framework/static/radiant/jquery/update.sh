#!/usr/bin/bash

echo "Removing old files"
rm jquery.min.js
rm  jquery.cookie.js
echo "Downloading new files"
wget https://code.jquery.com/jquery-3.3.1.min.js -O jquery.min.js
wget https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js -O jquery.cookie.js
echo "Done"
