#!/bin/bash

# Custom plugin builder

TYPE='safecast'

DIR=/tmp/$TYPE
rm -rf $DIR ; mkdir $DIR

safecast_packager() {
    cp -r . $DIR
    rm $DIR/icons/radiation*
    rm $DIR/layer/ers* $DIR/layer/pei*
    mv $DIR/metadata_safecast.txt $DIR/metadata.txt
    rm $DIR/plugin_packager.sh
    rm $DIR/reader/pei* $DIR/reader/ers*
}

if [ "$TYPE" == 'safecast' ]; then
    safecast_packager
fi

exit 0
