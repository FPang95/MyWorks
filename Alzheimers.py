import pandas as pd
import matplotlib.pyplot as plt

alz = pd.read_csv("CCDSS.csv")

#print(alz)

ince = alz.loc[~alz["Incidence (Rate per 100)"].str.contains("-")]
prev = alz.loc[~alz["Prevalence (%)"].str.contains("-")]
mort = alz.loc[~alz["Mortality (Rate Ratio)"].str.contains("-")]

new_df = pd.DataFrame(alz["Area"])

new_df["Incidence"] = ince["Incidence (Rate per 100)"].astype('float')
new_df["Prevalence"] = prev["Prevalence (%)"].astype('float')
new_df["Mortality"] = mort["Mortality (Rate Ratio)"].astype('float')

print(new_df.groupby(["Area"]).mean())
#list(new_df.groupby(["Area"]).mean()["Incidence"])
#print(new_df["Area"].sort_values().unique())

for i in new_df.columns[1:]:
    ticks = range(1, len(new_df.groupby(["Area"]))+1)
    height = list(new_df.groupby(["Area"]).mean()[i])
    tick_label = new_df["Area"].sort_values().unique()
    plt.bar(ticks, height, tick_label=tick_label, width=0.6)
    plt.title("Alzheimer's " + i + " by Province")
    plt.ylabel("Population Percentage")
    plt.show()

'''
alz_ince = {}
alz_prev = {}
alz_mort = {}

#print(alz.columns)

areas = list(set(alz["Area"]))
for i in areas:
    alz_ince.setdefault(i, [])
    alz_prev.setdefault(i, [])
    alz_mort.setdefault(i, [])

for entries in alz.values:
    for keys in alz_ince.keys():
        if entries[0] == keys:
            if entries[6] == "-":
                pass
            else:
                alz_ince[keys].append(float(entries[6]))
            if entries[9] == "-":
                pass
            else:
                alz_prev[keys].append(float(entries[9]))
            if entries[12] == "-":
                pass
            else:
                alz_mort[keys].append(float(entries[12]))

for keys in alz_ince.keys():
    alz_ince[keys] = s.mean(alz_ince[keys])
    alz_prev[keys] = s.mean(alz_prev[keys])
    alz_mort[keys] = s.mean(alz_mort[keys])

#print(alz_ince)
#print(alz_prev)
#print(alz_mort)

shorthand = []
for short in alz_ince.keys():
    shorthand.append(short[:5])

ticks = range(1, len(alz_ince.keys())+1)
height = list(alz_ince.values())
tick_label = shorthand
plt.bar(ticks, height, tick_label=tick_label, width=0.6)
plt.title("Alzheimer's Incidence by Province")
plt.ylabel("Population Percentage")
plt.show()


ticks = range(1, len(alz_prev.keys())+1)
height = list(alz_prev.values())
tick_label = shorthand
plt.bar(ticks, height, tick_label=tick_label, width=0.6)
plt.title("Alzheimer's Prevalence by Province")
plt.ylabel("Population Percentage")
plt.show()

ticks = range(1, len(alz_mort.keys())+1)
height = list(alz_mort.values())
tick_label = shorthand
plt.bar(ticks, height, tick_label=tick_label, width=0.6)
plt.title("Alzheimer's Mortality by Province")
plt.ylabel("Population Percentage")
plt.show()
'''