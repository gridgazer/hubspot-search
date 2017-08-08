#!/bin/bash
deps=(pastel algoliasearch)
for dep in ${deps[@]}; do
 	version=$(pip show $dep | perl -n -e'/Version: ([\d\.]+)/ && print $1')
 	if [ $version ]; then
 		echo $dep is installed with version $version
 	else
 		echo $dep is not installed
 		pip install $dep
 	fi
done
