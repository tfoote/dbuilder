#!/bin/bash

PACKAGE=$1

echo dbuilder building package: $PACKAGE
apt-get update
apt-src install $PACKAGE
apt-src build $PACKAGE
