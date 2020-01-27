import re
import string
import sys
import os
import fnmatch


def main():


    # delete duplicate
    #to_be_sorted = input("Which file to use? ('.txt')")
    to_be_sorted = sys.argv[1]
    os.system("sort -u %s -o %s" %(to_be_sorted,to_be_sorted))
        
    # Read from row-unique
    #in_file = to_be_sorted
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    #out_file = input("Which file to output ('.idx')")
    f = open(in_file, "r")
    w = open("ready.txt", "w")
    rows = f.readlines()
    # put the cleaned data into ready.txt
    # remove trailing newline/whitespace
    for row in rows:
        # Replace backslash with "&92;"
        new = re.sub(r"\\", "&92;", row)
        # print out key and value in diff line
        found = re.search("^(.+?):(.+?)$", new)
        if found:
            front = found.group(1)
            #print(front)
            w.write(str.strip(front)+"\n")
            rear = found.group(2)
            #print(rear)
            w.write(str.strip(rear)+"\n")
    f.close()
    w.close()
    #bdbtype = input("What type of Berkeley DB to use?")

    # read from the text file
    os.system("db_load -T -c duplicates=1 -f %s -t %s %s" %("ready.txt", sys.argv[3], out_file))
    #name = str(out_file).rstrip(".idx")
    os.system("db_dump -p -f dump_new.txt %s" %(out_file))


if __name__ == "__main__":
	main()