#include <emscripten.h>
#include <stdio.h>

int main(){
	printf("game\n");
	emscripten_run_script("alert('hello')");
}
