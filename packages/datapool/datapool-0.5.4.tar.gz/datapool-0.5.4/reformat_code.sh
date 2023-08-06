#!/bin/bash

# run reformatting code according to pep 8:

if black --version 2>/dev/null >/dev/null ; then
    black datapool tests
    echo
    echo please run \"git diff\" to see the changes
else
    echo
    echo please run \"pip install black\" first
fi


