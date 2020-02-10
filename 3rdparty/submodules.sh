#!/bin/sh

DIR=$PWD

# git submodule add git@edison.fel.zcu.cz:agros/RDOLab/3rdparty/bayesopt.git 3rdparty/bayesopt

# update
git submodule update --init --recursive

# BayesOpt
cd $DIR/bayesopt
mkdir -p build
cd build
cmake ..
make -j5
cp $DIR/bayesopt/build/lib/bayesopt.so $DIR/../artap/lib/
strip $DIR/../artap/lib/bayesopt.so
