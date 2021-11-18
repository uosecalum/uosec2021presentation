/*
	duck-battle.c
	CTF_FLAG{52d7fcdc6c0ba02631ebfa84871d858be7a90770}
	Solution: use undocumented command to win
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

void reward(char* string){
	int i = strlen(string);
	for (int x = 0; x < i; x++){
		string[x] = string[x] ^ 1;
	}
}

void intro(){
	char* title = "________                 __     __________         __    __  .__          \n\\______ \\  __ __   ____ |  | __ \\______   \\_____ _/  |__/  |_|  |   ____  \n |    |  \\|  |  \\_/ ___\\|  |/ /  |    |  _/\\__  \\\\   __\\   __\\  | _/ __ \\ \n |    `   \\  |  /\\  \\___|    <   |    |   \\ / __ \\|  |  |  | |  |_\\  ___/ \n/_______  /____/  \\___  >__|_ \\  |______  /(____  /__|  |__| |____/\\___  >\n        \\/            \\/     \\/         \\/      \\/                     \\/ \n";
	system("clear");
	puts("Welcome to...");
	puts(title);
}

void gameOver(){
	char* ghost = "     .-.\n   .'   `.\n   :g g   :\n   : o    `.\n  :         ``.\n :             `.\n:  :         .   `.\n:   :          ` . `.\n `.. :            `. ``;\n    `:;             `:'\n       :              `.\n        `.              `.     .\n          `'`'`'`---..,___`;.-'";
	system("clear");
	puts(ghost);
	puts("You died.");
	exit(0);
}

int main(){
	int in;
	char player[32];
	char choice[8];
	char secret[] = "43e6gbeb7b1c`13720dcg`95960e949cd6`81661";
	char* duck = "           ,-.\n       ,--' ~.).\n     ,'         `.\n    ; (((__   __)))\n    ;  ( (#) ( (#)\n    |   \\_/___\\_/|\n   ,\"  ,-'    `__\".\n  (   ( ._   ____`.)--._        _\n   `._ `-.`-' \\(`-'  _  `-. _,-' `-/`.\n    ,')   `.`._))  ,' `.   `.  ,','  ;\n  .'  .     `--'  /     ).   `.      ;\n ;     `-        /     '  )         ;\n \\                       ')       ,'\n  \\                     ,'       ;\n   \\               `~~~'       ,'\n    `.                      _,'\nhjw   `.                ,--'\n        `-._________,--'\n";

//Begin Game
	intro();

//Ask for name
	puts("What do you want to be called?");
	scanf(" %31s", player);
	fflush(stdin);
	printf("Hello, %s. It is time for the DUCK BATTLE.\n\n Are you ready? (y/n):", player);
	scanf(" %c",choice);
	fflush(stdin);
	if(!strncmp("y", choice, 1))
		puts("yes");
	else if (!strncmp("n", choice, 1)){
		puts("Oh, okay then.");
		exit(1);
	}
	else {
		puts("Huh? We're playing anyways!");
		sleep(2);
	}

//A duck approaches
//Fight loop (reward in fight loop to discourage folks from trying to just find the win func)
	int battle = 1;
	int attempts = 0;
	int winner = 0;
	//Battle Intro
	system("clear");
	puts(duck);
	puts("A duck approaches! Time for battle!");
	puts("What will you do?\n1: Attack\n2: Items\n3: Panic");
	getchar();
	scanf(" %d", &in);
	fflush(stdin);
	
	//main battle loop
	while(battle){
		if(attempts > 3){
			system("clear");
			puts(duck);
			puts("uh oh! You took too long!");
			sleep(2);
			puts("The duck quacks really loud and it makes you want to shout uncontrollably.");
			sleep(2);
			gameOver();
		}
		switch (in){
			case 1:
				system("clear");
				puts(duck);
				puts("You attack!");
				sleep(2);
				puts("The duck dodges and then uses its web foot attack!");
				sleep(2);
				puts("Oh no! It hurts a lot more than you would expect!");
				sleep(2);
				gameOver();
				break;
			case 2:
				system("clear");
				puts(duck);
				puts("You reach into your pocket... and pull out a really old reciept for coffee from the Duck Store. It's from 2014.");
				sleep(2);
				puts("The duck laughs and then summons a meteor!");
				sleep(2);
				puts("It's uh, really big. This isn't going to end we-");
				sleep(2);
				gameOver();
				break;
			case 3:
				attempts++;
				system("clear");
				puts(duck);
				puts("You panic!");
				sleep(2);
				puts("You feel a little better, but the duck is still here.");
				sleep(2);
				puts("What will you do?\n1: Attack\n2: Items\n3: Panic");
				scanf(" %d", &in);
				fflush(stdin);
				break;
			case 8128626:
				battle = 0;
				system("clear");
				puts(duck);
				puts("You sweep the duck's leg!");
				sleep(2);
				puts("The duck loses balance and falls down a very large cliff!");
				sleep(2);
				winner = 1;
				reward(secret);
				break;
			default:
				puts("what?");
				attempts++;
				sleep(2);
				system("clear");
				puts(duck);
				puts("That duck looks mean!");
				puts("What will you do?\n1: Attack\n2: Items\n3: Panic");
				scanf(" %d", &in);
				fflush(stdin);
		}

		if(winner){
			system("clear");
			puts("You win! You won the DUCK BATTLE!");
			printf("CTF_FLAG{%s}\n", secret);
		}
	}
	return 0;
}
