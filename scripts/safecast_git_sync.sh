#!/bin/bash -e

# Copy Safecast-only related to code to destination dir

DIR=../qgis-safecast-plugin

# docs
cp -rv docs         $DIR/
# i18n
cp -rv i18n         $DIR/
# icons
cp -v icons/safecast* $DIR/icons/
cp -v icons/tool*     $DIR/icons/
# root files
cp -v __init__.py \
   LICENSE \
   Makefile \
   pb_tool.cfg \
   plugin_type.py \
   radiation_toolbox_dockwidget_base.ui \
   radiation_toolbox*.py \
   resources* \
   $DIR/
# layer
mkdir -p $DIR/layer
cp -v layer/__init__.py \
   layer/exceptions.py \
   layer/safecast* \
   $DIR/layer
# reader
mkdir -p $DIR/reader
cp -v reader/__init__.py \
   reader/exceptions.py \
   reader/safecast* \
   reader/logger.py \
   reader/utils.py \
   $DIR/reader
# style
mkdir -p $DIR/style
cp -v style/__init__.py \
   style/safecast.py \
   $DIR/style
mkdir -p $DIR/style/safecast
cp -rv style/safecast/* \
   $DIR/style/safecast
# tools
cp -rv tools $DIR/tools

exit 0
