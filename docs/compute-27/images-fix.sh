#!/bin/bash

set -x

cd akash

# Iterate over all files in the current directory
for file in *\ *; do
  # Replace spaces with %20
  new_file="${file// /%20}"
  # Rename the file
  mv "$file" "$new_file"
done
