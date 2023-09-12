import pandas as pd

df = pd.read_csv("ohio_rentals_mined.csv")

# drop index column
df.drop(df.columns[0], axis=1, inplace=True)

# convert $1,000 to 1000
df['Price'] = df['Price'].apply(lambda x: float(x[1:].replace(',', '')))
df['Sq ft'] = df['Sq ft'].apply(lambda x: x if isinstance(x, float) else float(x.replace(',', '')))
print(df.head())

#sift through bad data
df = df[df['Beds'] != "—"]
df = df[df['Baths'] != "—"]
df.to_csv("ohio_rentals_cleaned.csv", index=False)