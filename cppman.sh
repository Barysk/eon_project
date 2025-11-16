#!/usr/bin/env bash

project_name="EON"

run() {
	cmake . && make && ./bin/"$project_name"
}

build() {
	cmake . && make
}

clean(){
	echo "Cleaning project..."

	rm -rf CMakeFiles
	rm -f CMakeCache.txt
	rm -f cmake_install.cmake
	rm -f Makefile

	rm -rf bin
	rm -f *.o
	rm -f *.obj

	rm -f *.log
	rm -f *~
	rm -f *.swp

	echo "Clean complete."
}

case "$1" in
	run) run
	;;
	build) build
	;;
	clean) clean
	;;
	*) echo "Incorrect usage: Provide run|build|clean as an argument."
	;;
esac

