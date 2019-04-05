import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("RespiratoryDiseaseDeath.csv")

print(df.columns)


# Sum of deaths by respiratory diseases separated by age group every year
#for col in list(df["Age group"].unique()[1:]):
#    print(str(list(df["Age group"].unique()).index(col)) + ": " + col)
'''
for year in df["REF_DATE"].unique():
    age_groups = df.loc[(df["Sex"]=="Both sexes") & (df["REF_DATE"]==year)].groupby(["Age group"], sort=False).sum()["VALUE"]
    ticks = range(1, len(age_groups[1:]) + 1)
    height = age_groups[1:]
    tick_label = ["<1","1-4","5-9","10-14","15-19","20-24","25-29","30-34","35-39","40-44","45-49","50-54","55-59",
                  "60-64","65-69","70-74","75-79","80-84","85-89","90+","Unstated"]
    #tick_label = range(1, len(age_groups[1:]) + 1)
    plt.bar(ticks, height, tick_label=tick_label, width=0.6)
    plt.title("Respiratory deaths in " + str(year))
    plt.ylabel("Number of deaths")
    plt.xlabel("Age Groups")
    plt.ylim([0, 90000])
    plt.show()
'''

# look at older years, seems that more of older generation are dying from respiratory diseases.
# life expectancy is increasing meaning more people living to older generation, which could explain rise in
# death for 84-89 and 90+ age groups comparing 2000 to 2016
for year in df["REF_DATE"].unique():
    age_groups = df.loc[(df["Sex"]=="Both sexes") & (df["REF_DATE"]==year)].groupby(["Age group"], sort=False).sum()["VALUE"]
    ticks = range(1, len(age_groups[14:-1]) + 1)
    height = age_groups[14:-1]
    tick_label = ["60-64","65-69","70-74","75-79","80-84","85-89","90+"]
    #tick_label = range(1, len(age_groups[1:]) + 1)
    plt.bar(ticks, height, tick_label=tick_label, width=0.6)
    plt.title("Respiratory deaths in " + str(year))
    plt.ylabel("Number of deaths")
    plt.xlabel("Age Groups")
    plt.ylim([0, 90000])
    plt.show()

#male_age_group_2000 = df.loc[(df["REF_DATE"]==2000)&(df["Sex"]=="Males")]["Age group"].unique()




#print(df.loc[(df["REF_DATE"]==2000) & (df["Cause of death (ICD-10)"]=="Total, all causes of death") & (df["Sex"]=="Males")]["VALUE"])




# remove useless columns
#df = df.drop(columns=["STATUS", "SYMBOL", "TERMINATED", "DECIMALS"])
#df.to_csv("RespiratoryDiseaseDeath.csv", index=False)