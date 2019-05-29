import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CD_Household.csv")

print(df.columns)
print(df["Diseases"].unique())

# remove useless columns
#df = df.drop(columns=["UOM_ID", "SCALAR_FACTOR", "SCALAR_ID", "VECTOR", "COORDINATE", "STATUS", "SYMBOL", "TERMINATED", "DECIMALS"])
#df.to_csv("CD_Household.csv", index=False)