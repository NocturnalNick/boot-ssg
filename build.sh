#!/bin/bash
# Build script for production deployment
# This builds the site with the correct basepath for GitHub Pages

# Get the repository name from git
REPO_NAME=$(basename -s .git $(git config --get remote.origin.url))

# Run the site generator with the repository name as basepath
python3 src/main.py "/$REPO_NAME/"

echo "Site built with basepath: /$REPO_NAME/"
echo "Output directory: docs/"
