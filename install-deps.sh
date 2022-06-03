#!/bin/sh

while read r; do
	pip install $r
done < requirements
