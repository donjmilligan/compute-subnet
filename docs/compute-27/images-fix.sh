#!/bin/bash

set -x

cd akash

# DISABLED [

fix1 () {
# Iterate over all files in the current directory
for file in *\ *; do
  # Replace spaces with %20
  new_file="${file// /%20}"
  # Rename the file
  mv "$file" "$new_file"
done
}

# DISABLED ]
# EXPORT screens.md [

echo '# screens' > screens.md

for file in *\ *; do
  new_file="${file// /%20}"
  # Rename the file
  echo "## file" >> screens.md
  echo "$new_file" >> screens.md
done

# EXPORT screens.md ]
