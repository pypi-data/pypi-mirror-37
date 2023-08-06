#! /bin/sh
#
# setup.sh
# Copyright (C) 2018 Uwe Schmitt <uwe.schmitt@id.ethz.ch>
#
# Distributed under terms of the MIT license.
#

set -e

export ETC=$(pwd)
rm -rf datapool || true
rm -rf lz || true
rm -rf dlz || true


mkdir lz

pool init-config --use-sqlitedb lz

pool init-db

pool run-simple-server &

sleep 2

pool create-example dlz
pool update-operational dlz

sudo -E pool delete-entity --force --force --what site test_site
pool update-operational dlz
