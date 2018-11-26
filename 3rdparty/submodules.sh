#!/bin/sh

DIR=$PWD

# git submodule add git@edison.fel.zcu.cz:agros/RDOLab/3rdparty/nlopt2.git 3rdparty/nlopt2
# git submodule add git@edison.fel.zcu.cz:agros/RDOLab/3rdparty/platypus.git 3rdparty/platypus
# git submodule add git@edison.fel.zcu.cz:agros/RDOLab/3rdparty/bayesopt.git 3rdparty/bayesopt

# update
git submodule update --init --recursive

# nlopt2
cd $DIR/nlopt2
mkdir -p build
cd build
cmake ..
make -j4
cp $DIR/nlopt2/build/src/swig/_nlopt.so $DIR/../artap/lib/
strip $DIR/../artap/lib/_nlopt.so

# BayesOpt
cd $DIR/bayesopt
mkdir -p build
cd build
cmake ..
make -j4
cp $DIR/bayesopt/build/lib/bayesopt.so $DIR/../artap/lib/
strip $DIR/../artap/lib/bayesopt.so


# go back
cd $DIR