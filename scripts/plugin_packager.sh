#!/bin/bash -e

# Custom plugin builder

DIR=`pwd`/..

pythonqwt_packager() {
    TMPDIR=/tmp/pythonqwt
    python3 -m venv /tmp/pythonqwt
    source /tmp/pythonqwt/bin/activate
    python3 -m pip install PythonQwt
    cp -r $TMPDIR//lib/python3.9/site-packages/qwt/ $DIR/
    rm -rf $TMPDIR
}

packager() {
    find $DIR | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
    pb_tool zip
}

pythonqwt_packager
packager

exit 0
