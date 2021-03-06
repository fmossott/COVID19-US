#!/bin/bash -e

function fail {
  echo $1
  exit 1
}

function banner {
  echo
  echo --------------------------------------------------------
  echo $1
  echo --------------------------------------------------------
  echo
}

pull=true

if [ "$1" = "--nopull" ]; then
  pull=false
fi

cd `dirname $0`
cwd=$PWD 

#Pull source
banner "Pulling source repo"
cd "$cwd/../COVID-19"
git pull

cd "$cwd"

#Pull this repo
if [ "$pull" = true ]; then
  banner "Pulling this repos"
  git checkout master
  git pull
fi

# Process data
banner "Process data"
./combine.sh

# Check changes, commit and push
banner "Checking for changes"
if [[ `git status --porcelain` ]]; then
  echo Changes to commit
  mergetime=`date -u "+%Y-%m-%dT%H:%M:%S"` 
  banner "Committing to 'Merge $mergetime'"
  git commit -a -m "Merge $mergetime"

  git push
  if [ -f refresh.sh ]; then
    ./refresh.sh
  fi
else
  echo No changes to commit
fi
