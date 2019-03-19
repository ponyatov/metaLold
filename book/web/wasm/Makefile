all: none.wasm

%.wasm: %.c
	emcc -s WASM=1 -s SIDE_MODULE=1 -o $@ $< 
