mkdir -p test_modules
cd test_modules

git_clone () {
  echo git clone $1
  git clone $1
}

git_clone https://github.com/tinygrad/tinygrad
