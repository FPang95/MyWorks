import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CCDI2018.csv")

#print(df.head())

percent_only = df.loc[df["Unit"] == "%"]

for domains in list(percent_only["Domain"].unique()):
    print(str(list(percent_only["Domain"].unique()).index(domains)+1) + ": " + domains)

print(percent_only.groupby(["Domain"]).mean()["Latest Data [a]"])

ticks = range(1, len(percent_only.groupby(["Domain"]))+1)
height = list(percent_only.groupby(["Domain"]).mean()["Latest Data [a]"])
tick_label = range(1, len(percent_only["Domain"].unique())+1)
plt.bar(ticks, height, tick_label=tick_label, width=0.6)
plt.title("Chronic disease indicators")
plt.ylabel("Percentage")
plt.show()


#new_df = pd.DataFrame(alz["Area"])

#new_df["Incidence"] = ince["Incidence (Rate per 100)"].astype('float')



#new_df = df

#new_df.loc[new_df["Unit"]=='per 1000 total births [c]', ["Unit","Latest Data [a]"]]\
    #=["%", new_df.loc[new_df["Unit"]=='per 1000 total births [c]', for i in ["Latest Data [a]"]: i =i/1000]]




#a.loc["Unit","Latest Data [a]"]=["%", a["Latest Data [a]"]/1000]


#clean up some empty columns
#df = df.drop(columns=["Unnamed: 8", "Unnamed: 9", "Unnamed: 10", "Unnamed: 11"])
#new_df.to_csv("Edit1CCDI2018.csv", index=False)

#make all units to percentages