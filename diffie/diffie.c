/*
	CTF_FLAG{745808261b1fad2dc90e6bdb936867c72c622d5b}
	Key in hex is '20B40'
	Solution: do math to break diffie hellman

	prime 		208003
	root modulo	207999
	secret a 	13370
	secret b 	86753
	share A 	61337	(207999^13370 mod 208003)
	share B 	64488	(207999^86753 mod 208003)
	secret s 	133952	(64488^13370 mod 208003)
	secret s 	133952	(61337^86753 mod 208003)
	hex(s)	 	0x20B40

 */

#include <stdio.h>
#include <string.h>
#include <time.h>

int main(int argc, char **argv){
	char key[64];
	char data[64];
	
	if (argc != 2){
		puts("usage: ./diffie datafile");
		return 1;
	}

	puts("Please enter key (in hexadecimal)");
	scanf(" %63s",key);
	fflush(stdin);

	FILE *datafile = fopen(argv[1], "rb");
	fread (data, 64, 64, datafile);

	//get datafile size
	fseek(datafile, 0L, SEEK_END);
	int fsize = ftell(datafile);
	rewind(datafile);

	int j = strlen(key); //Determine key block size
	int y = 0;

	FILE *f2 = fopen("diffie.out", "w");
	for(int x = 0; x <= fsize; x++){
		data[x] = data[x] ^ key[y%j];
		y++;
		fprintf(f2, "%c", data[x]);
	}
	puts("Protected secret written to diffie.out");



}
