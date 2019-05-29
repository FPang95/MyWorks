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
'''for year in df["REF_DATE"].unique():
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
'''

'''
# look at the top 10 deadliest respiratory diseases for each year
for year in df["REF_DATE"].unique():
    print("\nYear "+ str(year))
    print(df.loc[(df["Sex"]=="Both sexes") & (df["REF_DATE"]==year) & (df["Age group"]=="Total, all ages")].
          groupby(["Cause of death (ICD-10)"]).sum().sort_values("VALUE", ascending=False)["VALUE"][1:11])
#male_age_group_2000 = df.loc[(df["REF_DATE"]==2000)&(df["Sex"]=="Males")]["Age group"].unique()
#top 10 is consistent through the years
'''

# Top 10 deadliest diseases by year are not the same between men and women
'''
# Look if there is a gender bias in top 10 deadliest respiratory diseases (total) for each year
for year in df["REF_DATE"].unique():
    total = df.loc[(df["Sex"]=="Both sexes")&(df["REF_DATE"]==year)&(df["Age group"]=="Total, all ages")].\
        groupby(["Cause of death (ICD-10)"]).sum().sort_values("VALUE", ascending=False)["VALUE"][1:11]

    male = df.loc[(df["Sex"]=="Males")&(df["REF_DATE"]==year)&(df["Age group"]=="Total, all ages")].\
        groupby(["Cause of death (ICD-10)"]).sum().sort_values("VALUE", ascending=False)["VALUE"][1:11]

    female = df.loc[(df["Sex"]=="Females")&(df["REF_DATE"]==year)&(df["Age group"]=="Total, all ages")].\
        groupby(["Cause of death (ICD-10)"]).sum().sort_values("VALUE", ascending=False)["VALUE"][1:11]

    mens = (100*(male/total)).values
    womens = (100*(female/total)).values

    #top 10 killers for males vs females is not the same for every year
    ticks = range(1,len(total)+1)
    p1 = plt.bar(ticks, mens, tick_label=ticks)
    p2 = plt.bar(ticks, womens, bottom=mens)

    #plt.xticks = (ticks, (df["REF_DATE"].unique()))
    plt.legend((p1[0], p2[0]), ("Men", "Women"))
    plt.title("Respiratory deaths in " + str(year))
    plt.yticks(range(0,110, 10))
    plt.ylim(0,130)
    plt.ylabel("Proportional Mortality (%)")
    plt.show()
'''

# look at total deaths per year and separate by gender
total = df.loc[(df["Sex"]=="Both sexes")&(df["Age group"]=="Total, all ages")
               &(df["Cause of death (ICD-10)"]=="Total, all causes of death")][["REF_DATE", "VALUE"]]

male = df.loc[(df["Sex"]=="Males")&(df["Age group"]=="Total, all ages")
              & (df["Cause of death (ICD-10)"]=="Total, all causes of death")][["REF_DATE","VALUE"]]

female = df.loc[(df["Sex"]=="Females")&(df["Age group"]=="Total, all ages")
                & (df["Cause of death (ICD-10)"]=="Total, all causes of death")][["REF_DATE","VALUE"]]

mens = (100*(male["VALUE"].values/total["VALUE"].values))
womens = (100*(female["VALUE"].values/total["VALUE"].values))
ticks = total["REF_DATE"]
p1 = plt.bar(ticks, mens, tick_label=ticks)
p2 = plt.bar(ticks, womens, bottom=mens)

#plt.xticks = (ticks, (df["REF_DATE"].unique()))
plt.legend((p1[0], p2[0]), ("Men", "Women"))
plt.title("Total Deaths by Year")
plt.yticks(range(0, 110, 10))
plt.ylim(0, 130)
plt.ylabel("Proportional Mortality (%)")
plt.show()
#Values appear to be roughly equal for total death so no apparent gender bias


#print(df.loc[(df["REF_DATE"]==2000) & (df["Cause of death (ICD-10)"]=="Total, all causes of death") & (df["Sex"]=="Males")]["VALUE"])


# remove useless columns
#df = df.drop(columns=["UOM_ID", "SCALAR_FACTOR", "SCALAR_ID", "DGUID"])
#df.to_csv("RespiratoryDiseaseDeath.csv", index=False)