#!/bin/bash

# Custom plugin builder

TYPE='safecast'

DIR=/tmp/$TYPE
rm -rf $DIR ; mkdir $DIR

safecast_packager() {
    cp -r . $DIR
    rm -rf $DIR/__pycache__ $DIR/layer/__pycache__ $DIR/reader/__pycache__ $DIR/style/__pycache__
    rm $DIR/icons/radiation*
    rm $DIR/layer/ers* $DIR/layer/pei*
    mv $DIR/metadata_safecast.txt $DIR/metadata.txt
    rm $DIR/plugin_packager.sh
    rm $DIR/reader/pei* $DIR/reader/ers*
    rm -r $DIR/ers* $DIR/pei*
    rm -r $DIR/tests $DIR/scripts
}

if [ "$TYPE" == 'safecast' ]; then
    safecast_packager
fi

exit 0
