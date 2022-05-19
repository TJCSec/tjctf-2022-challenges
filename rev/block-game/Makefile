all: clean build jar

build:
	javac -d build src/*.java

.PHONY:
	clean
	all

jar:
	jar cfm bin/chall.jar MANIFEST.MF -C build/ .

clean:
	rm -rf build/ bin/chall.jar
