#!/bin/bash
echo $PWD
files=$(ls $TOPDIR/python_exts/setup/* 2>/dev/null | wc -l)
if [ $files != "0" ]; then
	for i in $TOPDIR/python_exts/setup/*; do
		echo $i
		cat $i >>$TOPDIR/python_build/$PYDIR/Modules/Setup.dist
	done
fi
files2=$(ls $TOPDIR/python_exts/c_files/* 2>/dev/null | wc -l)
if [ $files2 != "0" ]; then
	cp -r $TOPDIR/python_exts/c_files/* $TOPDIR/python_build/$PYDIR/Modules/
fi
