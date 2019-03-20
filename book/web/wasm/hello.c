#include <stdio.h>

int main(int argc, char *argv[]) {
	printf("Hello World\n\n");
	for (int i=0; i<argc; i++)
		printf("argv[%i] = %s\n",i,argv[i]);
}
