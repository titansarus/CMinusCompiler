#!/bin/sh

mkdir zipper
cp src/compiler.py zipper
cp -r src/Compiler zipper/Compiler
rm -rf zipper/Compiler/Misc
rm -rf 'zipper/Compiler/generator codes'
find zipper -name "__pycache__" -type d -exec rm -r "{}" \;

rm ./compiler.zip

cd zipper
zip -r ../compiler.zip ./compiler.py ./Compiler
cd ..

rm -rf zipper
