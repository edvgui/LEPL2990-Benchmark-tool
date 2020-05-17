#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>

int lineCounter = 0;
int fileCounter = 0;

void countLines(FILE *file) {

    char* line = NULL;
	size_t len = 0;

	while(getline(&line, &len, file) != -1) {
		lineCounter++;
	}
}

void countFiles(DIR *directory, char* path) {
    struct dirent *dir;
	
	while ((dir = readdir(directory)) != NULL) {
	    if (dir->d_type & DT_REG) {
	        char buf[512];
	        snprintf(buf, 510, "%s/%s", path, dir->d_name);
	        
	        FILE *file = fopen(buf, "r");
	        if (file == NULL) {
	            printf("Error with file %s\n", buf);
	        } else {
	            countLines(file);
	            fileCounter++;
	            
	            fclose(file);
	        }
	    }
	}
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("A argument required, got %d\n", argc - 1);
    }
    char* path = argv[1];

	DIR* d = opendir(path);
	if (d == NULL) {
	    printf("Couldn't open directory %s\n", path);
	    exit(1);
	}
	
	countFiles(d, path);
	
	printf("Done\n%d lines in %d files in directory %s\n", lineCounter, fileCounter, path);

	return 0; 
}
