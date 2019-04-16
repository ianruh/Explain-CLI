#! /bin/bash

echo "" > examples.txt
explain -v "echo Ian | sed 's/an/in/'" >> examples.txt
explain -v curl -I -s myapplication:5000 >> examples.txt
explain -v "cat test.json | jq" >> examples.txt
