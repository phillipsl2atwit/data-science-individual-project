import csv

data_dir = '../data/dataset_1/'

in_name = 'train_clean.csv'
out_name = 'wip.csv'
lookup = ['Happiness', 'Neutral', 'Boredom', 'Anxiety', 'Anger', 'Sadness']

with open(data_dir+in_name, 'r', newline='') as f_read:
    with open(data_dir+out_name, 'w') as f_write:
        reader = csv.reader(f_read)
        writer = csv.writer(f_write)

        largest = 0
        smallest = 1000
        # check every row of the data
        row_num = 0
        for row in reader:
            col_num = 0
            to_write = []
            for col in row:
                if row_num != 0:
                    if col_num == 4:
                        num = int(col)
                        largest = max(num, largest)
                        smallest = min(num, smallest)
                    if col_num == 9:
                        to_write.append(col)
                        to_write.append(lookup.index(col))
                    else:
                        to_write.append(col)
                else:
                    to_write.append(col)
                    if col_num == 9:
                        to_write.append("Dominant_Emotion (Numerical)")
                col_num += 1
            writer.writerow(to_write)
            row_num += 1
        print(f"least amount of time spent: {smallest}")
        print(f"greatest amount of time spent: {largest}")
        f_write.close()
    f_read.close()
