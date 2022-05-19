CC := gcc
CFLAGS := -Werror -O3
LDFLAGS := -Wl,-x

server: server.c libgo.a verify.s sha512.c sha512.S

.PHONY: clean
clean:
	rm -f server
