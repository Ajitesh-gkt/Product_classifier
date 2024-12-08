import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder


# print(f"Unique categories: {df['category_id'].unique()}")
df = pd.read_csv('cleaned_sampled_df.csv')

le = LabelEncoder()
df['category_id'] = le.fit_transform(df['category_id'])

category_mapper = dict(zip(df['category_id'], df['category_name']))

with open("Category_mapper.json", "w") as f:
    json.dump(category_mapper, f)

print("Category_mapper.json created successfully")