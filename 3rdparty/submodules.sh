#!/bin/sh

DIR=$PWD

# git submodule add git@edison.fel.zcu.cz:agros/RDOLab/3rdparty/nlopt2.git 3rdparty/nlopt2
# git submodule add git@edison.fel.zcu.cz:agros/RDOLab/3rdparty/bayesopt.git 3rdparty/bayesopt
# git submodule add git@edison.fel.zcu.cz:agros/agros2d.git 3rdparty/agros

# update
git submodule update --init --recursive

# nlopt2
cd $DIR/nlopt2
mkdir -p build
cd build
cmake ..
make -j2
cp $DIR/nlopt2/build/src/swig/_nlopt.so $DIR/../artap/lib/_nlopt.so
cp $DIR/nlopt2/build/src/swig/__nlopt.so $DIR/../artap/lib/_nlopt.so
strip $DIR/../artap/lib/_nlopt.so

# BayesOpt
cd $DIR/bayesopt
mkdir -p build
cd build
cmake ..
make -j2
cp $DIR/bayesopt/build/lib/bayesopt.so $DIR/../artap/lib/
strip $DIR/../artap/lib/bayesopt.so

# Agros Suite
cd $DIR/agros
git submodule update --init 
cd dealii 
mkdir -p build 
cd build 
cmake -DCMAKE_BUILD_TYPE="Release" -DDEAL_II_WITH_CXX14="OFF" -DDEAL_II_WITH_CXX17="OFF" ..
make -j2 
cd ../../
# - export CC=/usr/bin/clang
# - export CXX=/usr/bin/clang++     
cmake . 
make -j2
# generator
./agros_generator
cd plugins
cmake .
make -j2
# strip
cd ..
strip libs/*.so
strip agros
strip agros_solver
strip pythonlab
# link ~/.local
ln -sfn $DIR/agros ~/.local/lib/python3.7/site-packages/agrossuite
#ln -sfn $DIR/agros ~/.local/lib/python3.6/site-packages/agrossuite
#ln -sfn $DIR/agros /home/tamas/anaconda3/envs/artapenc/lib/python3.6/site-packages/agrossuite
# go back
cd $DIR
