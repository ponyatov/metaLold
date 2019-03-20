all: none.wasm hello.html

%.wasm: %.c
	emcc -s WASM=1 -s SIDE_MODULE=1 -o $@ $< 
%.html: %.c
	emcc -s WASM=1 -o $@ $< 
	