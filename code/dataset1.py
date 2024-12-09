import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mat
from scipy import stats

USE_TIME = "Daily_Usage_Time (minutes)"
EMOTION = "Dominant_Emotion (Numerical)"
DAILY_POSTS = "Posts_Per_Day"
DAILY_LIKES_REC = "Likes_Received_Per_Day"
DAILY_COMMENTS_REC = "Comments_Received_Per_Day"
DAILY_MESSAGES_SENT = "Messages_Sent_Per_Day"

data = pd.read_csv("../data/dataset_1/final.csv")

data_filtered = []
lookup = ['Happiness', 'Neutral', 'Boredom', 'Anxiety', 'Anger', 'Sadness']
for i in range(6):
    temp = data[data[EMOTION] == i]
    print(f"{lookup[i]}: mean: {temp[USE_TIME].mean()}, std: {temp[USE_TIME].std()}")
    data_filtered.append(temp[USE_TIME])

not_happy = data[data[EMOTION] != 0]
print(f"\npeople that weren't happy: mean: {not_happy[USE_TIME].mean()}, std: {not_happy[USE_TIME].std()}")

happy = data[data[EMOTION] == 0]

x = data[EMOTION]
y = data[USE_TIME]

colormap = mat.colors.ListedColormap(["green", "grey", "blue", "orange", "red", "purple"])


t_value, p_value = stats.ttest_ind(happy[USE_TIME].to_list(), not_happy[USE_TIME].to_list(), nan_policy='raise')
print(f"t: {t_value}, p: {p_value}")
plt.boxplot(data_filtered)
plt.xticks(range(6))
plt.xlabel("Emotional State")
plt.ylabel("Avg Time Spent on Social Media (minutes)")
plt.title("Fig 6: Avg Time Spent on Social Media vs Emotional State (Box)")
plt.savefig("d1_box",transparent=True)
plt.show()

# plt.scatter(x, y, alpha=0.03) #, c=x, cmap=colormap, alpha=0.03)
plt.scatter(x, y, c=x, cmap=colormap, alpha=0.03)
plt.xticks(range(6))
plt.xlabel("Emotional State")
plt.ylabel("Avg Time Spent on Social Media (minutes)")
plt.title("Fig 5: Avg Time Spent on Social Media vs Emotional State (Scatter)")
plt.savefig("d1_scatter",transparent=True)
plt.show()
