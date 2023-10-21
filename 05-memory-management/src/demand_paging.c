///
/// demand_paging.c
/// test of demand paging
///
#include <unistd.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <err.h>

#define BUFFER_SIZE (100 * 1024 * 1024)
#define NCYCLE      10
#define PAGE_SIZE   4096

int main(void)
{
    time_t t = time(NULL);

    char *s  = ctime(&t);

    printf("%.*s:before allocation.  please press Enter key\n", (int)(strlen(s) - 1), s);
    getchar();

    char *p = malloc(BUFFER_SIZE);

    if (p == NULL) {
        err(EXIT_FAILURE, "malloc() failed");
    }

    t = time(NULL);
    s = ctime(&t);

    printf("%.*s: allocated %dMB.  please press Enter key\n", (int)(strlen(s) - 1), s, BUFFER_SIZE / (1024 * 1024));
    getchar();

    for (int i = 0; i < BUFFER_SIZE; i += PAGE_SIZE) {
        p[i] = 0;

        int cycle = i / (BUFFER_SIZE / NCYCLE);
        if ((cycle != 0) && (i % (BUFFER_SIZE / NCYCLE) == 0)) {
            t = time(NULL);
            s = ctime(&t);
            printf("%.*s: touched %dMB.  please press Enter key\n", (int)(strlen(s) - 1), s, i / (1024 * 1024));
            sleep(1);
        }
    }

    t = time(NULL);
    s = ctime(&t);

    printf("%.*s: touched %dMB.  please press Enter key\n", (int)(strlen(s) - 1), s, BUFFER_SIZE / (1024 * 1024));
    getchar();

    exit(EXIT_FAILURE);
}
