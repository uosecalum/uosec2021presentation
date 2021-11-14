#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char * argv[]) {
	printf("Enter the secure passphrase: \n");
	char * buf = NULL;
	size_t bufsize = 0;
	ssize_t guess_size = 0;
	guess_size = getline(&buf, &bufsize, stdin);
	if (guess_size > 33) {
		puts("Whoa, we said secure passphrase, not super secure, who uses a password over 32 chars I mean really now.\n");
		return -1;
	}
	if (buf[guess_size-1] == '\n') {
		buf[guess_size-1] = '\0';
	}
	int guess = strcmp(buf, "f8a9da56bc463ca06ebcde0cde409196");
	if (guess == 0) {
		printf("flag{uosec_rip_kb}.\n");
		return 0;
	}
	else if (guess < 0 && guess > -10) {
		printf("Now what was that dang passcode, this has got to be Mike Belotti's fault %d.\n", guess);
	}
	else if (guess > 0 && guess > 10) {
		printf("Did it rhyme with Deschutes? I don't know, but I did spend entirely too long of my life in there %d.\n", guess);
	}
	else if (guess < 50 && guess > 10) {
		printf("This reminds me of that time I left my wallet on the 4th floor of the Willamette building %d.\n", guess);
	}
	else if (guess > -50 && guess < -10) {
		printf("Does everyone still wonder how it gets so hot in Deady hall basement %d.\n", guess);
	}
	else {
		printf("Maybe these numbers mean something? hmmm %d.\n", guess);
	}
	return 0;
}
