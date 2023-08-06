#!/usr/bin/bash

echo "Removing old files"
rm hammer.min.js
echo "Downloading new files"
wget https://hammerjs.github.io/dist/hammer.min.js
echo "Done"



