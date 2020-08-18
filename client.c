#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

struct packet_data
{
    char name[100];
    char pass[100];
    int func_id; // We can change this to function name if needed
    // TODO ada time
};
int register(struct packet_data tm);
/* -------------------------------------------------------------------------------------*/
void print_loading() {
    for ( int loop = 0; loop < 4; ++loop) {
        for ( int each = 0; each < 4; ++each) {
            printf ( "\rConnecting to the server%.*s   \b\b\b", each, "...");
            fflush ( stdout);//force printing as no newline in output
            sleep ( 1);
        }
    }
    printf ( "\n");
}

void print_menu()
{
/***
 *       ____     _         _        ____   _  __         ____     _____      _        ____         ____   _       U  ___ u   _   _   ____    
 *    U | __")u  |"|    U  /"\  u U /"___| |"|/ /        / __"| u |_ " _| U  /"\  u U | __")u    U /"___| |"|       \/"_ \/U |"|u| | |  _"\   
 *     \|  _ \/U | | u   \/ _ \/  \| | u   | ' /        <\___ \/    | |    \/ _ \/   \|  _ \/    \| | u U | | u     | | | | \| |\| |/| | | |  
 *      | |_) | \| |/__  / ___ \   | |/__U/| . \\u       u___) |   /| |\   / ___ \    | |_) |     | |/__ \| |/__.-,_| |_| |  | |_| |U| |_| |\ 
 *      |____/   |_____|/_/   \_\   \____| |_|\_\        |____/>> u |_|U  /_/   \_\   |____/       \____| |_____|\_)-\___/  <<\___/  |____/ u 
 *     _|| \\_   //  \\  \\    >>  _// \\,-,>> \\,-.      )(  (__)_// \\_  \\    >>  _|| \\_      _// \\  //  \\      \\   (__) )(    |||_    
 *    (__) (__) (_")("_)(__)  (__)(__)(__)\.)   (_/      (__)    (__) (__)(__)  (__)(__) (__)    (__)(__)(_")("_)    (__)      (__)  (__)_) 
 ***/

    puts("Welcome: ");
    printf("%d: Register\n",1);
    printf("%d: login\n",2);
    printf("%d: create_vm\n",3);
    printf("%d: modify_vm\n",4);
    printf("%d: add_subscription\n",5);
    printf("%d: check_usage\n",6);
    printf("%d: get_vmlife\n",7);
    printf("%d: get_vmstatus\n",8);
}
/* -------------------------------------------------------------------------------------*/
int register(struct packet_data tm){
    printf("%s","Enter Name: ");
    scanf("%s",tm.name);
    printf("%s","Enter pass: ");
    return 1;
}
/* -------------------------------------------------------------------------------------*/
int main()
{
    struct packet_data tm;
    print_menu();
    print_loading();
    register(tm);
}
