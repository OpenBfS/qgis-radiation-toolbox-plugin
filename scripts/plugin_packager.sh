#!/bin/bash -e

# Custom plugin builder

TYPE='safecast'

DIR=/tmp/qgis-${TYPE}-plugin
rm -rf $DIR ; mkdir $DIR

safecast_packager() {
    cp -r . $DIR
    (cd $DIR/help;make html)
    mkdir $DIR/docs
    cp -r $DIR/help/build/html/* $DIR/docs
    rm -rf $DIR/help
    rm -rf $DIR/.git $DIR/.gitignore
    rm -rf $DIR/__pycache__ $DIR/layer/__pycache__ $DIR/reader/__pycache__ $DIR/style/__pycache__
    rm $DIR/icons/radiation*
    rm $DIR/layer/ers* $DIR/layer/pei*
    mv $DIR/metadata_safecast.txt $DIR/metadata.txt
    rm $DIR/reader/pei* $DIR/reader/ers*
    rm -r $DIR/style/ers* $DIR/style/pei*
    rm -r $DIR/scripts

    sed -i 's/PLUGIN_TYPE = PluginType.Dev/PLUGIN_TYPE = PluginType.Safecast/g' $DIR/plugin_type.py
    sed -i 's/safecast_icon_devel/safecast_icon_stable/g' $DIR/radiation_toolbox.py
}

pythonqwt_packager() {
    TMPDIR=/tmp/pythonqwt
    pip3 install PythonQwt -t $TMPDIR
    cp -r $TMPDIR/qwt $DIR/
    rm -rf $TMPDIR
}

zip_packager() {
    cd /tmp
    zip_file=qgis-${TYPE}-plugin.zip
    rm -f $zip_file
    zip $zip_file qgis-${TYPE}-plugin -r
}

if [ "$TYPE" == 'safecast' ]; then
    safecast_packager
    pythonqwt_packager
fi
zip_packager

exit 0
