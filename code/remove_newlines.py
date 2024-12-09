import sys

if not (len(sys.argv) in [3,4]):
    print("Incorrect number of arguments entered, enter 2/3 arguments: the source file, then the destination file to be created/overwritten, then optionally a directory to make both paths relative to, e.g. ../data/dataset_1/")
    sys.exit()

temp = []

in_file = sys.argv[1]
out_file = sys.argv[2]
pwd = ""
if len(sys.argv) == 4:
    pwd = sys.argv[3]

# read data of input file
try:
    with open(pwd+in_file, 'r') as f_read:
        i = 0
        for row in f_read:
            temp.append(row)
        f_read.close()
except:
    print(f"filepath 1: '{in_file}' could not be found")

try:
    with open(pwd+out_file, 'w') as f_write:
        i = 0
        for row in temp:
            if i % 2 == 0: # ignore every other line because they're empty
                f_write.write(row)
            i += 1
        f_write.close()
except:
    print(f"filepath 2: '{out_file}' could not be found")
