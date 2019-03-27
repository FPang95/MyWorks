import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Heart_Disease.csv")

print(df.columns)

cases = df.loc[df["indicatorName"]=="number of cases",df.columns[2:]]
deaths = df.loc[df["indicatorName"]=="number of deaths",df.columns[2:]]

#print(cases[["year", "Total"]])
#print(deaths[["year", "Total"]])

for i in cases.columns[2:-1]:
    j = deaths[i].values/cases[i].values
    ticks = range(1, len(cases["year"]) + 1)
    height = j
    tick_label = cases["year"].values
    plt.bar(ticks, height, tick_label=tick_label, width=0.6)
    plt.title(i + " deaths/cases")
    plt.ylabel("Mortality Rate")
    plt.xlabel("Year")
    plt.show()

#survival = cases["ipb-ischemic heart disease"].values-deaths["ipb-ischemic heart disease"].values
#print(survival)

#df["Total"] = df.iloc[:, 4:,].sum(axis=1)
#print(cases)


ticks = range(1, len(cases["year"]) + 1)
height = cases["Total"].values
tick_label = cases["year"].values
plt.bar(ticks, height, tick_label=tick_label, width=0.6)
plt.title("Heart disease cases by year")
plt.ylabel("Number of cases")
plt.xlabel("Year")
plt.show()

ticks = range(1, len(deaths["year"]) + 1)
height = deaths["Total"].values
tick_label = deaths["year"].values
plt.bar(ticks, height, tick_label=tick_label, width=0.6)
plt.title("Heart disease deaths by year")
plt.ylabel("Number of deaths")
plt.xlabel("Year")
plt.show()

ticks = range(1, len(deaths["year"]) + 1)
height = deaths["Total"].values/cases["Total"].values
tick_label = deaths["year"].values
plt.bar(ticks, height, tick_label=tick_label, width=0.6)
plt.title("Death Rate")
plt.ylabel("Deaths/Cases")
plt.xlabel("Year")
plt.show()


#df = df.drop(columns="Unnamed: 0")
#df.to_csv("Heart_Disease.csv", index=False)