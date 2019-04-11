#!/bin/bash

# Custom plugin builder

TYPE='safecast'

DIR=/tmp/$TYPE
rm -rf $DIR ; mkdir $DIR

safecast_packager() {
    cp -r . $DIR
    (cd $DIR/docs;make html)
    rm -rf $DIR/.git $DIR/.gitignore
    rm -rf $DIR/__pycache__ $DIR/layer/__pycache__ $DIR/reader/__pycache__ $DIR/style/__pycache__
    rm $DIR/icons/radiation*
    rm $DIR/layer/ers* $DIR/layer/pei*
    mv $DIR/metadata_safecast.txt $DIR/metadata.txt
    rm $DIR/plugin_upload.py
    rm $DIR/reader/pei* $DIR/reader/ers*
    rm -r $DIR/style/ers* $DIR/style/pei*
    rm -r $DIR/test $DIR/scripts

    sed -i 's/PLUGIN_TYPE = PluginType.Dev/PLUGIN_TYPE = PluginType.Safecast/g' $DIR/plugin_type.py
}

zip_packager() {
    cd /tmp
    zip $TYPE.zip $TYPE -r
}

if [ "$TYPE" == 'safecast' ]; then
    safecast_packager
fi
zip_packager

exit 0
