#!/usr/bin/env bash

RESULT_FILENAME="results.txt"

case "$1" in
	"-o")  # output results
		python -B -m src.main >> "$RESULT_FILENAME"
	;;
	"-ow") # overwrite old if exists
		python -B -m src.main > "$RESULT_FILENAME"
	;;
	*) # simply output to terminal
		python -B -m src.main
	;;
esac
