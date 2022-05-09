import requests
import pandas as pd

from tqdm import tqdm
from pathlib import Path


API_KEY = "zWAtdFQxeCdADBYwbIvHiVRrUwo8rOTOc4PBzJzF"
DATA_DIR = Path("data/USA")


# categories IDs
categories_url = f"https://api.eia.gov/category/?api_key={API_KEY}&category_id=3390101"
child_categories = requests.get(url=categories_url).json()["category"]["childcategories"]

# 13 USA disjoint sectors
sectors_categories_df = pd.DataFrame.from_dict(child_categories)
sectors = sectors_categories_df[1:14]


# Loading data

for i, (category_id, sector_name) in tqdm(sectors.iterrows(), desc="Loading data", total=sectors.shape[0]):
    
    sector_name = sector_name.split("(")[0].strip().replace(" ", "-")
    
    sector_url = f"https://api.eia.gov/category/?api_key={API_KEY}&category_id={category_id}"
    sector_series = pd.DataFrame.from_dict(requests.get(sector_url).json()["category"]["childseries"])
    sector_sources = sector_series.loc[sector_series.f=="H"]
    
    dfs = []
    for i, row in sector_sources.iterrows():
        series_id = row.series_id
        col_name = series_id.split(".")[3]
        url = f"https://api.eia.gov/series/?api_key={API_KEY}&series_id={series_id}"
        response = requests.get(url).json()
        data = pd.DataFrame.from_records(response["series"][0]["data"], columns=["date", col_name])
        data.date = pd.to_datetime(data.date)
        dfs.append(data)
        
    df = pd.concat(dfs, axis=1, join='inner')
    df.index = df.pop("date").iloc[:,0]
    df.sort_index(inplace=True)
    
    df.to_csv(DATA_DIR / f"{sector_name}.csv", index_label="datetime")
