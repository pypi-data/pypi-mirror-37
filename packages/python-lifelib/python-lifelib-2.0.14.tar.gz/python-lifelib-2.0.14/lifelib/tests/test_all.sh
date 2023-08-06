#!/bin/bash

python_versions="$*"

if [ -z "$python_versions" ]; then
python_versions="2 3"
fi

cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

lifelib_basename="$( basename "$( pwd )" )"

if [ "$lifelib_basename" = "lifelib" ]; then
echo "Directory has the correct name."
else
echo "Directory must be called 'lifelib', not '$lifelib_basename'."
exit 1
fi

cd ..

echo "Checking to see whether both versions of Python are installed..."

python_exists="true"

for i in $python_versions; do

python_version="$( "python$i" --version 2>&1 )"
python_status="$?"

if [ "$python_status" = 0 ]; then

printf "Python $i version: \033[1;32m$python_version\033[0m\n"

else

printf "Python $i exited with status code $python_status: \033[1;31m$python_version\033[0m\n"
python_exists="false"

fi

done

if [ "$python_exists" = "false" ]; then
exit 1
fi

set -e

printf "\n\033[1;36m **** UNIT TESTS ****\033[0m\n"
for i in $python_versions; do
"python$i" -m unittest discover lifelib/tests/unit
done

printf "\n\033[1;36m **** INTEGRATION TESTS ****\033[0m\n"
for i in $python_versions; do
"python$i" -m unittest discover lifelib/tests/integration
done

printf "\n\033[1;36m **** INDIRECTION TESTS ****\033[0m\n"
for i in $python_versions; do
"python$i" -m unittest discover lifelib/tests/indirection
done
