build:
	python3 gen.py
	emcc main.cpp -s USE_SDL=2 -o ../server/index.js

clean:
	rm -f ../server/index.js ../server/index.wasm
