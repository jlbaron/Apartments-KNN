import requests
import pandas as pd

df = pd.read_csv("ohio_rentals_cleaned.csv")

# will read address and parse into proper format
# will request for geocode from google maps
# will take lat/long and add as a column to df

# save final df for KNN
# df.to_csv("ohio_rentals.csv", index=False)