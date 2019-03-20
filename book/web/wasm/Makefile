all: none.wasm hello.wasm

OPT  = -s NO_EXIT_RUNTIME=1 -s NO_FILESYSTEM=1 
OPT += -fno-exceptions -fno-rtti --llvm-lto 1
%.wasm: %.c
	emcc -s WASM=1 -s SIDE_MODULE=1 $(OPT) -o $@ $<
