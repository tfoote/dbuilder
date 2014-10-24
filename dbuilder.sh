#!/bin/bash

set -o errexit

PACKAGE=$1

echo dbuilder building package: $PACKAGE
apt-get update


# Not working for ROS packages trying to install fully versioned sourcedeb
# apt-src install $PACKAGE -t
# alternative below
echo apt-get source $PACKAGE
apt-get source $PACKAGE

# It all should be in the docker instance already
# but make sure a dep hasn't changed.
echo apt-get build-dep -y $PACKAGE
apt-get build-dep -y $PACKAGE

# TODO do this better
cd */.

apt-get install -y devscripts
prevversion=`dpkg-parsechangelog | grep Version | awk '{print \$2}'`
newversion=$prevversion-`date +%Y%m%d-%H%M-%z`
debchange -D $(lsb_release -sc) -v $newversion 'Time stamping.'



echo apt-src import $PACKAGE --location .
apt-src import $PACKAGE --location . -t --version $newversion
echo apt-src build $PACKAGE
apt-src build $PACKAGE -t

cp -r .. /output
