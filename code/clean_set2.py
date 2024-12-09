import csv

data_dir = '../data/dataset_2/'

in_name = 'smmh.csv'
out_name = 'test.csv'

# takes a list of strings, converts them to integers and returns their sum
def sum_strs(strings):
    sum = 0
    for s in strings:
        sum += int(s)
    return sum

# used to convert between options described in text to more graphable numbers
time_lookup = ['Less than an Hour', 'Between 1 and 2 hours', 'Between 2 and 3 hours', 'Between 3 and 4 hours', 'Between 4 and 5 hours', 'More than 5 hours']

# used to create a column for each social media to allow sorting by individual social medias
social_lookup = ["Facebook", "Twitter", "Instagram", "YouTube", "Snapchat", "Discord", "Reddit", "Pinterest", "TikTok"]

# new columns to be inserted, and where to insert them
# column numbers are not affected by inserted columns,
# e.g. 7 & 8 are inserted after the original columns 7 & 8
# resulting in: to_write = [... columns[7], new_cols[7], columns[8], new_cols[8], ...]
new_cols = {
    7: "Number of different social media platforms used",
    8: "Average time spent on social media: N hours to N+1 hours",
    11: "'Addiction' score, combined scores of columns 9, 10, and 11",
    14: "'Distractability' score, combined scores of columns 10, 12, and 14",
    17: "'Validation-Seeking' score, combined scores of columns 15, 16, and 17",
    19: "'Depression' score, combined scores of columns 18 and 19"
}

with open(data_dir+in_name, 'r', newline='') as f_read:
    with open(data_dir+out_name, 'w') as f_write:
        reader = csv.reader(f_read)
        writer = csv.writer(f_write)

        # check every row of the data
        row_num = 0
        for row in reader:
            socials = []
            col_num = 0
            to_write = []
            for col in row:
                # row_num 0 is column titles 
                if row_num != 0:
                    # write raw data to new file
                    to_write.append(col)
                    # Number of different social media platforms used
                    if col_num == 7:
                        socials = col.split(', ')
                        to_write.append(len(socials))
                    # Numberical version of average time spend on social media
                    elif col_num == 8:
                        to_write.append(time_lookup.index(col))
                    # Grouping for questions 9, 10, & 11, signs of social media becoming a psychological vice and addiction, range: 3-15
                    elif col_num == 11:
                        to_write.append(sum_strs(to_write[-3:]))
                    # Grouping for questions 10, 12, & 14, about distractability and concentration, range: 3-15
                    elif col_num == 14:
                        to_write.append(sum_strs([to_write[-6], to_write[-3], to_write[-1]]))
                    # Grouping for questions 15, 16, & 17, questions about self-image and seeking validation from others through social media, range: 3-15
                    elif col_num == 17:
                        to_write.append(sum_strs(to_write[-3:]))
                    # Grouping for questions 18 and 19, asking about depression and loss of motivation, range: 2-10
                    elif col_num == 19:
                        to_write.append(sum_strs(to_write[-2:]))
                    # Binary columns for if a participant uses any given social media platform
                    elif col_num == 20:
                        for social_media in social_lookup: # convert True/False to 1/0 so it's more compatible
                            to_write.append(int(social_media in socials))
                else:
                    # write column names to new file
                    to_write.append(col)
                    # use new_cols lookup dictionary to add new columns for combined groupings and other derived statistics
                    if col_num in new_cols.keys():
                        to_write.append(new_cols[col_num])
                    if col_num == 20:
                        to_write.extend(social_lookup)
                col_num += 1
            # write the row to the file
            writer.writerow(to_write)
            row_num += 1
        f_write.close()
    f_read.close()
