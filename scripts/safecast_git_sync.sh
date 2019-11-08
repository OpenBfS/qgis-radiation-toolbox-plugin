#!/bin/bash -e

# Copy Safecast-only related to code to destination dir

DIR=../qgis-safecast-plugin

# docs
cp -r docs         $DIR/
# i18n
cp -r i18n         $DIR/
# icons
cp icons/safecast* $DIR/icons/
cp icons/tool*     $DIR/icons/
# root files
cp __init__.py \
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
cp layer/__init__.py \
   layer/exceptions.py \
   layer/safecast* \
   $DIR/layer
# reader
mkdir -p $DIR/reader
cp reader/__init__.py \
   reader/exceptions.py \
   reader/safecast* \
   reader/logger.py \
   reader/utils.py \
   $DIR/reader
# style
mkdir -p $DIR/style
cp style/__init__.py \
   style/safecast.py \
   $DIR/style
mkdir -p $DIR/style/safecast
cp -r style/safecast/* \
   $DIR/style/safecast
# tools
cp -r tools $DIR/tools

