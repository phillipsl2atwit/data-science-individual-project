import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mat

# terminal color codes for printing color coded statistic output
class CL:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# column macros to make typing these very specific strings easier
NUM_SOCIALS = "Number of different social media platforms used"
USE_TIME = "Average time spent on social media: N hours to N+1 hours"
ADDICTION = "'Addiction' score, combined scores of columns 9, 10, and 11"
DISTRACTIBILITY = "'Distractability' score, combined scores of columns 10, 12, and 14"
VALIDATION = "'Validation-Seeking' score, combined scores of columns 15, 16, and 17"
DEPRESSION = "'Depression' score, combined scores of columns 18 and 19"
SOCIALS = "7. What social media platforms do you commonly use?"

# threshold above which r^2 is colored green in stats printout
R_THRESHOLD = 0.05
# y variables to search for correlations in
Y_VARS = ["1. What is your age?", "Number of different social media platforms used", "9. How often do you find yourself using Social media without a specific purpose?", "10. How often do you get distracted by Social media when you are busy doing something?", "11. Do you feel restless if you haven't used Social media in a while?", "'Addiction' score, combined scores of columns 9, 10, and 11", "12. On a scale of 1 to 5, how easily distracted are you?", "13. On a scale of 1 to 5, how much are you bothered by worries?", "14. Do you find it difficult to concentrate on things?", "'Distractability' score, combined scores of columns 10, 12, and 14", "15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?", "16. Following the previous question, how do you feel about these comparisons, generally speaking?", "17. How often do you look to seek validation from features of social media?", "'Validation-Seeking' score, combined scores of columns 15, 16, and 17", "18. How often do you feel depressed or down?", "19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?", "'Depression' score, combined scores of columns 18 and 19", "20. On a scale of 1 to 5, how often do you face issues regarding sleep?"]

data = pd.read_csv("../data/dataset_2/final.csv")

# formats one of the social media statistics for printing, comparing it to the population as a whole, and showing the percentage increase/decrease
def format_num(a, b):
    retval = ""
    # color based on if the difference exceeds R_THRESHOLD, and if it is greater than or less than the whole population
    if (abs((a-b)/b) < R_THRESHOLD or abs(a) < R_THRESHOLD) and a != b:
        retval += CL.YELLOW
    elif a > b:
        retval += CL.GREEN
    elif a < b:
        retval += CL.RED
    elif a > R_THRESHOLD:
        retval += CL.GREEN

    # print main number with precision
    retval += f"{a:.4f}"
    # first segment does the + if it's positive, then it gets the % difference between a dnd b, and displays it with a percent sign at the end
    retval += f" {'+' if a >= b else ''}{((a-b)/b)*100:.2f}%"

    retval += CL.ENDC
    return retval

# adds spaces up to a fixed length to be printed with the strings in strs for
def spaces(strs, length):
    sum = 0
    for s in strs:
        sum += len(s)
    return " "*(length-sum)
# prints stats for a specific social media's distribution compared to the whole population, r^2, mean and std deviation 
def print_raw_stats(social, y_var, r_squared, mean, std, all_r_squared, all_mean, all_std):
    print(f"{social}, {y_var}: {spaces([social, y_var], 130)} {format_num(r_squared, all_r_squared)}, {format_num(mean, all_mean)}, {format_num(std, all_std)}")

# calculates correlation, mean and std deviation across all feasible axis pairings with USE_TIME
meta_stats = [] # stores a row of stats for each y_var of each social media, including ALL, the whole population
social_lookup = ["ALL", "Facebook", "Twitter", "Instagram", "YouTube", "Snapchat", "Discord", "Reddit", "Pinterest", "TikTok"]
for social in social_lookup:
    i = 0
    # print social media name as a title for each block, color it so that it stands out, print the amount of people in it and the percentage of total users that use that social media
    print(f"\t{CL.GREEN}{social}[{len(data[data[social] == 1]) if social != 'ALL' else len(data)}] {(len(data[data[social] == 1])/len(data))*100 if social != 'ALL' else 100:.2f}% :{CL.ENDC}")
    for y_var in Y_VARS:
        # get filtered set of data, or complete set if ALL
        data_temp = data
        if social == "ALL":
            data_temp = data
        else:
            data_temp = data[data[social] == 1]

        x_temp = data_temp[USE_TIME]
        y_temp = data_temp[y_var]

        # calculate linear regression, half of these variables won't be used
        temp_line, temp_residuals, rank, singular_vals, rcond = np.polyfit(x_temp, y_temp, 1, full=True)

        # calculate missing useful variables
        temp_mean = float(np.mean(y_temp))
        temp_std = float(np.std(y_temp))
        temp_sum_squares = np.sum((y_temp-temp_mean)**2)

        # calculate r^2 from the residuals
        r_squared = float(1 - (temp_residuals/temp_sum_squares))

        # store stats
        stats_row = [social, y_var, r_squared, temp_mean, temp_std]
        meta_stats.append(stats_row)

        # get the stats for the whole population for usage in printing
        all_r_squared = meta_stats[i][-3]
        all_mean = meta_stats[i][-2]
        all_std = meta_stats[i][-1]

        # print this row of stats
        print_raw_stats(social, y_var, r_squared, temp_mean, temp_std, all_r_squared, all_mean, all_std)
        i += 1

# create meta_stats csv file
with open("meta_stats.csv", "w") as f_write:
    writer = csv.writer(f_write)

    col_names = ["social_media_platform", "y_variable", "r_squared", "mean", "std"]
    writer.writerow(col_names)

    for l in meta_stats:
        writer.writerow(l)
    f_write.close()

x = data[USE_TIME]
y = data[DEPRESSION]

# calculate graph linear regression
line, residuals, rank, singular_vals, rcond = np.polyfit(x, y, 1, full=True)

# calculate r^2 from regression stats
y_mean = np.mean(y)
sum_squares = np.sum((y-y_mean)**2)
r_squared = 1 - residuals/sum_squares

max_x = x.to_numpy().max()

# prepare regression for drawing
m = line[0]
b = line[1]
lin_x = np.linspace(0,max_x,100)
lin_y = np.linspace(0+b,max_x*m + b,100)

# print regression statistics of graph
print(f"\nm: {m}, b: {b}, res: {residuals}, r_squared: {r_squared}")

# this order: addiction, distractability, depression

# make the graph
plt.scatter(x, y, alpha=25/len(x), color="purple")#, c=x, cmap=colormap, alpha=0.03)
plt.plot(lin_x, lin_y, color='red')
plt.xlabel("Rough Amount of Time Spent on Social Media (Hours)")
plt.ylabel("Distractibility Score")
plt.title("Fig 6: Correlation Between Time on Social Media and Distractibility Score")
plt.savefig("temp2",transparent=True)
plt.show()
