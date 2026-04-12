---
date: 2025-12-20
description: An end-to-end analysis of rental trends and pricing factors in Nairobi.
readingTime: 34 min read
status: published
tags:
- Python
- Nairobi
- DataScience
- RealEstate
title: Nairobi Airbnb Market Analysis
---

# IMPORTING ALL DEPENDENCIES I NEED FOR THIS PROJECT


```python
import numpy as np
import pandas as pd
import missingno as msno 
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import statsmodels.graphics.correlation as sgc
from statsmodels.graphics.gofplots import qqplot
import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import OLSInfluence
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
```

# CONNECTION TO MY DATABASE ON POSTGRES

This is the connection link to my database on postgreSQL, the actual connection function is on the file **db_connect.py**


```python
# Import necessary packages
import pandas as pd
import sys
sys.path.append('..')  # Go up one level to the root folder
from db_connect import connect_to_db

# Step 1: Connect to the database
conn = connect_to_db()

# Step 2: Create a cursor and run a query
cursor = conn.cursor()
query = "SELECT * FROM airbnbs_nairobi.listing_data_yearly;"
cursor.execute(query)

# Step 3: Fetch results and convert to a DataFrame
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

# Step 4: Display the data
print("Connection successful! Previewing data:")
display(df.head())
```

    Database connection successful!
    Connection successful! Previewing data:



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>listing_id</th>
      <th>listing_name</th>
      <th>listing_type</th>
      <th>room_type</th>
      <th>cover_photo_url</th>
      <th>photos_count</th>
      <th>minimum_nights</th>
      <th>cancellation_policy</th>
      <th>professional_management</th>
      <th>registration</th>
      <th>...</th>
      <th>rating_communication</th>
      <th>rating_location</th>
      <th>rating_value</th>
      <th>revenue_per_year</th>
      <th>avg_rate_per_year</th>
      <th>annual_occupancy(%)</th>
      <th>revenue_per_night_yearly</th>
      <th>reserved_days_in_year</th>
      <th>blocked_days_in_year</th>
      <th>available_days_in_year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>75683</td>
      <td>Kiloranhouse Apt Prime Bedroom</td>
      <td>Private room in home</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/5499026/ef...</td>
      <td>13</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>5.0</td>
      <td>4.8</td>
      <td>4.7</td>
      <td>141049.0</td>
      <td>6474.0</td>
      <td>6.6</td>
      <td>386.4</td>
      <td>24</td>
      <td>0</td>
      <td>341</td>
    </tr>
    <tr>
      <th>1</th>
      <td>471581</td>
      <td>Located In a Serene Environment</td>
      <td>Entire cottage</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/6434524/bc...</td>
      <td>37</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.8</td>
      <td>4.8</td>
      <td>804490.0</td>
      <td>5791.6</td>
      <td>54.8</td>
      <td>3058.9</td>
      <td>144</td>
      <td>102</td>
      <td>221</td>
    </tr>
    <tr>
      <th>2</th>
      <td>906958</td>
      <td>Makena's Place Karen - Flamingo Room</td>
      <td>Private room in cottage</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/68ecc57f-d...</td>
      <td>29</td>
      <td>1</td>
      <td>Firm</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.9</td>
      <td>4.9</td>
      <td>594869.0</td>
      <td>6772.2</td>
      <td>24.4</td>
      <td>1629.8</td>
      <td>89</td>
      <td>0</td>
      <td>276</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1023556</td>
      <td>Guesthouse Near Nairobi National Park &amp; Airport</td>
      <td>Entire guesthouse</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/ddd8badc-1...</td>
      <td>20</td>
      <td>1</td>
      <td>Flexible</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.7</td>
      <td>4.8</td>
      <td>29004.0</td>
      <td>3631.3</td>
      <td>3.0</td>
      <td>79.5</td>
      <td>11</td>
      <td>0</td>
      <td>354</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1237886</td>
      <td>Hob House</td>
      <td>Room in bed and breakfast</td>
      <td>hotel_room</td>
      <td>https://a0.muscache.com/im/pictures/cbdab7e1-f...</td>
      <td>8</td>
      <td>1</td>
      <td>Flexible</td>
      <td>True</td>
      <td>False</td>
      <td>...</td>
      <td>4.6</td>
      <td>4.7</td>
      <td>4.8</td>
      <td>168583.0</td>
      <td>15401.5</td>
      <td>3.0</td>
      <td>461.9</td>
      <td>11</td>
      <td>0</td>
      <td>354</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 42 columns</p>
</div>



```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>listing_id</th>
      <th>listing_name</th>
      <th>listing_type</th>
      <th>room_type</th>
      <th>cover_photo_url</th>
      <th>photos_count</th>
      <th>minimum_nights</th>
      <th>cancellation_policy</th>
      <th>professional_management</th>
      <th>registration</th>
      <th>...</th>
      <th>rating_communication</th>
      <th>rating_location</th>
      <th>rating_value</th>
      <th>revenue_per_year</th>
      <th>avg_rate_per_year</th>
      <th>annual_occupancy(%)</th>
      <th>revenue_per_night_yearly</th>
      <th>reserved_days_in_year</th>
      <th>blocked_days_in_year</th>
      <th>available_days_in_year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>75683</td>
      <td>Kiloranhouse Apt Prime Bedroom</td>
      <td>Private room in home</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/5499026/ef...</td>
      <td>13</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>5.0</td>
      <td>4.8</td>
      <td>4.7</td>
      <td>141049.0</td>
      <td>6474.0</td>
      <td>6.6</td>
      <td>386.4</td>
      <td>24</td>
      <td>0</td>
      <td>341</td>
    </tr>
    <tr>
      <th>1</th>
      <td>471581</td>
      <td>Located In a Serene Environment</td>
      <td>Entire cottage</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/6434524/bc...</td>
      <td>37</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.8</td>
      <td>4.8</td>
      <td>804490.0</td>
      <td>5791.6</td>
      <td>54.8</td>
      <td>3058.9</td>
      <td>144</td>
      <td>102</td>
      <td>221</td>
    </tr>
    <tr>
      <th>2</th>
      <td>906958</td>
      <td>Makena's Place Karen - Flamingo Room</td>
      <td>Private room in cottage</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/68ecc57f-d...</td>
      <td>29</td>
      <td>1</td>
      <td>Firm</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.9</td>
      <td>4.9</td>
      <td>594869.0</td>
      <td>6772.2</td>
      <td>24.4</td>
      <td>1629.8</td>
      <td>89</td>
      <td>0</td>
      <td>276</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1023556</td>
      <td>Guesthouse Near Nairobi National Park &amp; Airport</td>
      <td>Entire guesthouse</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/ddd8badc-1...</td>
      <td>20</td>
      <td>1</td>
      <td>Flexible</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.7</td>
      <td>4.8</td>
      <td>29004.0</td>
      <td>3631.3</td>
      <td>3.0</td>
      <td>79.5</td>
      <td>11</td>
      <td>0</td>
      <td>354</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1237886</td>
      <td>Hob House</td>
      <td>Room in bed and breakfast</td>
      <td>hotel_room</td>
      <td>https://a0.muscache.com/im/pictures/cbdab7e1-f...</td>
      <td>8</td>
      <td>1</td>
      <td>Flexible</td>
      <td>True</td>
      <td>False</td>
      <td>...</td>
      <td>4.6</td>
      <td>4.7</td>
      <td>4.8</td>
      <td>168583.0</td>
      <td>15401.5</td>
      <td>3.0</td>
      <td>461.9</td>
      <td>11</td>
      <td>0</td>
      <td>354</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>295</th>
      <td>42123446</td>
      <td>Mvuli Luxury Suites</td>
      <td>Entire rental unit</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/238557fd-c...</td>
      <td>24</td>
      <td>1</td>
      <td>Firm</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.5</td>
      <td>4.3</td>
      <td>4.4</td>
      <td>59105.0</td>
      <td>3710.9</td>
      <td>4.4</td>
      <td>161.9</td>
      <td>16</td>
      <td>0</td>
      <td>349</td>
    </tr>
    <tr>
      <th>296</th>
      <td>42139551</td>
      <td>Modern 1BR | King Bed | Fast Wi-Fi | Near CBD</td>
      <td>Entire condo</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/a10f889a-4...</td>
      <td>27</td>
      <td>1</td>
      <td>Flexible</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.9</td>
      <td>4.8</td>
      <td>228931.0</td>
      <td>6572.8</td>
      <td>9.0</td>
      <td>663.6</td>
      <td>31</td>
      <td>20</td>
      <td>334</td>
    </tr>
    <tr>
      <th>297</th>
      <td>42187559</td>
      <td>Cosy &amp; Airy Studio with Balcony WI-FI and Netflix</td>
      <td>Tiny home</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/miso/Hosti...</td>
      <td>43</td>
      <td>1</td>
      <td>Moderate</td>
      <td>True</td>
      <td>False</td>
      <td>...</td>
      <td>5.0</td>
      <td>4.7</td>
      <td>5.0</td>
      <td>25317.0</td>
      <td>2041.4</td>
      <td>3.3</td>
      <td>69.4</td>
      <td>12</td>
      <td>0</td>
      <td>353</td>
    </tr>
    <tr>
      <th>298</th>
      <td>42207619</td>
      <td>Kazuri Ivy Serene &amp; Spacious Nairobi Apartment</td>
      <td>Entire rental unit</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/hosting/Ho...</td>
      <td>19</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.9</td>
      <td>4.4</td>
      <td>4.8</td>
      <td>422289.0</td>
      <td>4969.1</td>
      <td>25.6</td>
      <td>1272.0</td>
      <td>85</td>
      <td>33</td>
      <td>280</td>
    </tr>
    <tr>
      <th>299</th>
      <td>42223689</td>
      <td>Airy &amp; Light-Filled: Indoor-Outdoor Home-Stay</td>
      <td>Private room in rental unit</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/fd146f8e-5...</td>
      <td>17</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>4.8</td>
      <td>4.9</td>
      <td>4.9</td>
      <td>190766.0</td>
      <td>2930.6</td>
      <td>22.4</td>
      <td>657.8</td>
      <td>65</td>
      <td>75</td>
      <td>300</td>
    </tr>
  </tbody>
</table>
<p>300 rows × 42 columns</p>
</div>



# Data Exploration an attempt at understanding my data


```python
df.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 300 entries, 0 to 299
    Data columns (total 42 columns):
     #   Column                    Non-Null Count  Dtype  
    ---  ------                    --------------  -----  
     0   listing_id                300 non-null    int64  
     1   listing_name              300 non-null    object 
     2   listing_type              300 non-null    object 
     3   room_type                 300 non-null    object 
     4   cover_photo_url           300 non-null    object 
     5   photos_count              300 non-null    int64  
     6   minimum_nights            300 non-null    int64  
     7   cancellation_policy       300 non-null    object 
     8   professional_management   300 non-null    bool   
     9   registration              300 non-null    bool   
     10  instant_book              300 non-null    bool   
     11  amenities                 300 non-null    object 
     12  host_id                   300 non-null    int64  
     13  host_name                 300 non-null    object 
     14  cohost_ids                300 non-null    object 
     15  cohost_names              300 non-null    object 
     16  owned_by                  300 non-null    object 
     17  owners                    300 non-null    int64  
     18  superhost                 300 non-null    bool   
     19  latitude                  300 non-null    float64
     20  longitude                 300 non-null    float64
     21  guests_allowed            300 non-null    int64  
     22  bedrooms                  300 non-null    int64  
     23  beds                      300 non-null    int64  
     24  baths                     300 non-null    float64
     25  cleaning_fee              300 non-null    float64
     26  extra_guest_fee           300 non-null    float64
     27  num_reviews               300 non-null    int64  
     28  rating_overall            300 non-null    float64
     29  rating_accuracy           300 non-null    float64
     30  rating_checkin            300 non-null    float64
     31  rating_cleanliness        300 non-null    float64
     32  rating_communication      300 non-null    float64
     33  rating_location           300 non-null    float64
     34  rating_value              300 non-null    float64
     35  revenue_per_year          300 non-null    float64
     36  avg_rate_per_year         300 non-null    float64
     37  annual_occupancy(%)       300 non-null    float64
     38  revenue_per_night_yearly  300 non-null    float64
     39  reserved_days_in_year     300 non-null    int64  
     40  blocked_days_in_year      300 non-null    int64  
     41  available_days_in_year    300 non-null    int64  
    dtypes: bool(4), float64(16), int64(12), object(10)
    memory usage: 90.4+ KB



```python
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>listing_id</th>
      <th>photos_count</th>
      <th>minimum_nights</th>
      <th>host_id</th>
      <th>owners</th>
      <th>latitude</th>
      <th>longitude</th>
      <th>guests_allowed</th>
      <th>bedrooms</th>
      <th>beds</th>
      <th>...</th>
      <th>rating_communication</th>
      <th>rating_location</th>
      <th>rating_value</th>
      <th>revenue_per_year</th>
      <th>avg_rate_per_year</th>
      <th>annual_occupancy(%)</th>
      <th>revenue_per_night_yearly</th>
      <th>reserved_days_in_year</th>
      <th>blocked_days_in_year</th>
      <th>available_days_in_year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>3.000000e+02</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>3.000000e+02</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>...</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>3.000000e+02</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>300.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2.818099e+07</td>
      <td>30.100000</td>
      <td>2.176667</td>
      <td>1.294209e+08</td>
      <td>1.580000</td>
      <td>-1.282688</td>
      <td>36.793314</td>
      <td>5.360000</td>
      <td>1.736667</td>
      <td>2.176667</td>
      <td>...</td>
      <td>4.869000</td>
      <td>4.825333</td>
      <td>4.775000</td>
      <td>5.557893e+05</td>
      <td>7504.654667</td>
      <td>23.385333</td>
      <td>1733.102333</td>
      <td>73.513333</td>
      <td>39.670000</td>
      <td>291.486667</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.191095e+07</td>
      <td>16.297916</td>
      <td>3.445533</td>
      <td>1.062699e+08</td>
      <td>0.890455</td>
      <td>0.035017</td>
      <td>0.039478</td>
      <td>4.856854</td>
      <td>1.571269</td>
      <td>2.031225</td>
      <td>...</td>
      <td>0.157549</td>
      <td>0.174527</td>
      <td>0.194769</td>
      <td>8.759067e+05</td>
      <td>6837.522117</td>
      <td>20.727560</td>
      <td>2581.110728</td>
      <td>66.100738</td>
      <td>52.670057</td>
      <td>66.100738</td>
    </tr>
    <tr>
      <th>min</th>
      <td>7.568300e+04</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>2.699700e+04</td>
      <td>1.000000</td>
      <td>-1.379600</td>
      <td>36.669400</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>...</td>
      <td>3.700000</td>
      <td>3.600000</td>
      <td>3.000000</td>
      <td>1.826400e+04</td>
      <td>1366.000000</td>
      <td>2.700000</td>
      <td>50.000000</td>
      <td>10.000000</td>
      <td>0.000000</td>
      <td>34.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>2.000117e+07</td>
      <td>19.000000</td>
      <td>1.000000</td>
      <td>3.594571e+07</td>
      <td>1.000000</td>
      <td>-1.297350</td>
      <td>36.779075</td>
      <td>2.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>...</td>
      <td>4.800000</td>
      <td>4.800000</td>
      <td>4.700000</td>
      <td>1.338565e+05</td>
      <td>4382.800000</td>
      <td>6.675000</td>
      <td>399.450000</td>
      <td>22.000000</td>
      <td>0.000000</td>
      <td>261.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>3.198200e+07</td>
      <td>28.000000</td>
      <td>1.000000</td>
      <td>1.008633e+08</td>
      <td>1.000000</td>
      <td>-1.284950</td>
      <td>36.791200</td>
      <td>4.000000</td>
      <td>1.000000</td>
      <td>2.000000</td>
      <td>...</td>
      <td>4.900000</td>
      <td>4.900000</td>
      <td>4.800000</td>
      <td>3.001395e+05</td>
      <td>6198.150000</td>
      <td>15.700000</td>
      <td>950.500000</td>
      <td>50.000000</td>
      <td>20.000000</td>
      <td>315.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>3.868569e+07</td>
      <td>37.000000</td>
      <td>2.000000</td>
      <td>2.237596e+08</td>
      <td>2.000000</td>
      <td>-1.264500</td>
      <td>36.806925</td>
      <td>6.000000</td>
      <td>2.000000</td>
      <td>3.000000</td>
      <td>...</td>
      <td>5.000000</td>
      <td>4.900000</td>
      <td>4.900000</td>
      <td>6.591980e+05</td>
      <td>8770.775000</td>
      <td>35.100000</td>
      <td>2171.350000</td>
      <td>104.000000</td>
      <td>61.250000</td>
      <td>343.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>4.222369e+07</td>
      <td>122.000000</td>
      <td>30.000000</td>
      <td>4.292661e+08</td>
      <td>6.000000</td>
      <td>-1.187200</td>
      <td>36.909600</td>
      <td>16.000000</td>
      <td>15.000000</td>
      <td>19.000000</td>
      <td>...</td>
      <td>5.000000</td>
      <td>5.000000</td>
      <td>5.000000</td>
      <td>1.070000e+07</td>
      <td>88421.700000</td>
      <td>90.700000</td>
      <td>32344.600000</td>
      <td>331.000000</td>
      <td>258.000000</td>
      <td>355.000000</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 28 columns</p>
</div>



# Data Cleaning


```python
import re

def to_snake_case(name):
    # Convert to lowercase
    name = name.lower()
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Remove special characters like parentheses
    name = re.sub(r'[(%\)]+', '', name)
    # Replace multiple underscores with single underscore
    name = re.sub(r'_+', '_', name)
    return name

# Apply to all columns
df.columns = [to_snake_case(col) for col in df.columns]

print(df.columns)
```

    Index(['listing_id', 'listing_name', 'listing_type', 'room_type',
           'cover_photo_url', 'photos_count', 'minimum_nights',
           'cancellation_policy', 'professional_management', 'registration',
           'instant_book', 'amenities', 'host_id', 'host_name', 'cohost_ids',
           'cohost_names', 'owned_by', 'owners', 'superhost', 'latitude',
           'longitude', 'guests_allowed', 'bedrooms', 'beds', 'baths',
           'cleaning_fee_', 'extra_guest_fee', 'num_reviews', 'rating_overall',
           'rating_accuracy', 'rating_checkin', 'rating_cleanliness',
           'rating_communication', 'rating_location', 'rating_value',
           'revenue_per_year', 'avg_rate_per_year', 'annual_occupancy',
           'revenue_per_night_yearly', 'reserved_days_in_year',
           'blocked_days_in_year', 'available_days_in_year'],
          dtype='object')



```python
msno.matrix(df)
```



    <Axes: >

    
![png](/images/blog/airbnb_analysis_nairobi_11_1.png)
    representation of all columns to show no missing value


# Pricing & Revenue Analysis

## What's the correlation between listing type and average nightly rate?
For this analysis, room type is used as the primary classification variable, as it provides a more general and consistent categorization of listings. In contrast, listing type contains a large number of highly specific categories, which can introduce unnecessary complexity and reduce comparability across observations.


```python
listing_type = df['listing_type'].unique()
len(listing_type)
```




    29




```python
room_type = df['room_type'].unique()
len(room_type)
room_type
```




    array(['private_room', 'entire_home', 'hotel_room'], dtype=object)



While **listing types** consist of **29 unique categories** across the dataset, **room types** are limited to **three broad and representative categories** that better capture the nature of the accommodation. These include **Private Room**, **Entire Home/Apartment**, and **Hotel Room**, the latter of which appears only once in the dataset.

#### Distribution of Room Type across the entire dataset


```python
room_type_count = df['room_type'].value_counts()
plt.figure(figsize=(10,8))
plt.pie(room_type_count, labels=room_type_count.index, colors=("#0FB9B9", "#E29015", "#F3013E"), autopct='%1.1f%%', startangle=90, textprops={'fontsize':11})
plt.title("Room Type Distribution Across the Dataset", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()
```


    
![png](/images/blog/airbnb_analysis_nairobi_18_0.png)
    A pie chart visualizing the distribution of room types



```python
listing_type_vs_avg_rate_per_night = df.groupby('room_type')['avg_rate_per_year'].mean().sort_values(ascending=False).round(2)
plt.figure(figsize=(10, 6))
listing_type_vs_avg_rate_per_night.plot(kind='bar', color=["#1AF64D", "#10EFCD", "#F60F0FF3"])
plt.title('Listing Type correlation to Average Rate Per Night', fontsize=14, fontweight='bold')
plt.ylabel('Average rate per Night', fontsize=14)
plt.xlabel('Type of Listing', fontsize=14)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# display the findings
listing_type_vs_avg_rate_per_night
```


    
![png](/images/blog/airbnb_analysis_nairobi_19_0.png)
    a bar chart visualizing listing type and their average rate per night





    room_type
    hotel_room      15401.50
    entire_home      7488.58
    private_room     7424.20
    Name: avg_rate_per_year, dtype: float64



Based on the analysis, **hotel rooms** command the highest average nightly rate at **KSh 15,401**. In contrast, **entire homes** and **private rooms** are priced at relatively similar levels, with average nightly rates of **KSh 7,488** and **KSh 7,424**, respectively.

## Which room types generate the most revenue despite having lower average rates?


```python
avg_rate_vs_revenue_per_room_type = df.groupby('room_type')['revenue_per_year'].mean().sort_values(ascending=False).round(2)
avg_rate_vs_revenue_per_room_type
```




    room_type
    entire_home     619762.21
    private_room    229331.23
    hotel_room      168583.00
    Name: revenue_per_year, dtype: float64




```python
avg_rate_vs_revenue_per_room_type = (
    df.groupby('room_type')
      .agg(
          avg_rate_per_night=('avg_rate_per_year', 'mean'),
          revenue_per_year=('revenue_per_year', 'mean')
      )
).sort_values(by='revenue_per_year', ascending=False).round(2)

avg_rate_vs_revenue_per_room_type
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_rate_per_night</th>
      <th>revenue_per_year</th>
    </tr>
    <tr>
      <th>room_type</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>entire_home</th>
      <td>7488.58</td>
      <td>619762.21</td>
    </tr>
    <tr>
      <th>private_room</th>
      <td>7424.20</td>
      <td>229331.23</td>
    </tr>
    <tr>
      <th>hotel_room</th>
      <td>15401.50</td>
      <td>168583.00</td>
    </tr>
  </tbody>
</table>
</div>



The listing type generating the most revenue is **Entire Home, Ksh 619762** despite being the second highest rate per night, followed by **Private Room** generating **Ksh 229331** per year and lastly **Hotel Rooms** generating **Ksh 168583** despite being the highest rate per night

# Host Strategy & Management

## Are professionally managed listings priced higher than individually managed ones?

A listing is considered **professionally managed** when it is:

*   Operated by a **property management company** or hospitality firm
    
*   Managed by hosts who handle **multiple properties** as a business rather than a single personal residence
    

This typically includes:

*   Standardized check-in/check-out procedures
    
*   Dedicated cleaning and maintenance teams
    
*   Consistent pricing and availability management
    
*   Formal guest communication and support systems
    

How this differs from individual hosts

*   **Individually managed listings** are usually run by:
    
    *   A single host
        
    *   Often the property owner
        
    *   With more personalized and less standardized operations
        
*   **Professionally managed listings** tend to:
    
    *   Have **stricter policies** (e.g., cancellation, minimum nights)
        
    *   Operate more like hotels or serviced apartments
        
    *   Prioritize occupancy optimization and operational efficiency


```python
# Map boolean values to labels
management_labels = df['professional_management'].map({
    True: 'Professionally Managed',
    False: 'Individually Managed'
})

professional_management_pie = management_labels.value_counts()

colors = ("#5da718", "#79059c")

plt.figure(figsize=(10, 8))
plt.pie(
    professional_management_pie,
    labels=professional_management_pie.index,
    autopct='%1.1f%%',
    colors=colors,
    startangle=90,
    textprops={'fontsize': 11}
)
plt.title("Professionally Managed vs Individually Managed Listings")
plt.tight_layout()
plt.show()

# Display counts
print(professional_management_pie)

```


    
![png](/images/blog/airbnb_analysis_nairobi_28_0.png)
    A pie chart visualising distribution of how listings are managed


    professional_management
    Individually Managed      201
    Professionally Managed     99
    Name: count, dtype: int64


so 99 Listings making up 33% of all the listings are professionally managed while 201 Listings making uo 67% of all the listings are Individually managed


```python
management_labels = df['professional_management'].map({
    True: 'Professionally Managed',
    False: 'Individually Managed'
})

pricing_vs_avg_rate_per_year = df.groupby(management_labels)['avg_rate_per_year'].mean().round(2)
pricing_vs_avg_rate_per_year
```




    professional_management
    Individually Managed      7218.56
    Professionally Managed    8085.51
    Name: avg_rate_per_year, dtype: float64




```python
plt.figure(figsize=(10,6))
pricing_vs_avg_rate_per_year.plot(kind='bar', color=["#05258D","#067538"])
plt.title('Professional Management Correlation To Average Price', fontsize=12, fontweight='bold')
plt.xlabel('Professional Management', fontsize=12)
plt.xticks(rotation=0)
plt.ylabel('Average Rate Per Year', fontsize=12)
plt.tight_layout()
plt.show()

```


    
![png](/images/blog/airbnb_analysis_nairobi_31_0.png)
    A bar chart showing how differently managed listings rate


based on our chart above, the professionally managed listings tend to be priced higher compared to individually run listings, With professionally managed listings charging an average a rate of **8086 per Night** and Individually Managed Listings charging an average rate of **7219 per Night**

## Do professionally managed listings have better reviews/ratings?


```python
professionally_managed_vs_reviews = df.groupby(management_labels)['rating_overall'].mean().sort_values(ascending=True).round(2)
professionally_managed_vs_reviews
```




    professional_management
    Professionally Managed    4.77
    Individually Managed      4.79
    Name: rating_overall, dtype: float64



**Individually Managed** Listings are slightly better rated at **4.79** compared to **Professionally Managed** listings at **4.77**

## Is there a relationship between professional management and cancellation strictness?

To assess whether host management strategy influences booking flexibility, we examined the distribution of cancellation policies across professionally and individually managed listings.


```python
professional_management_vs_cancellation_strictness = df.groupby('cancellation_policy')['professional_management'].value_counts
professional_management_vs_cancellation_strictness
```




    <bound method SeriesGroupBy.value_counts of <pandas.core.groupby.generic.SeriesGroupBy object at 0x79cb866339e0>>




```python
pm_vs_policy = (
    pd.crosstab(
        df['cancellation_policy'],
        df['professional_management'].map({
            True: 'Professionally Managed',
            False: 'Individually Managed'
        })
    )
)

```


```python
pm_vs_policy.plot(
    kind='bar',
    stacked=True,
    figsize=(10, 6)
)

plt.title('Professional Management vs Cancellation Policy')
plt.xlabel('Cancellation Policy')
plt.ylabel('Number of Listings')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

```


    
![png](/images/blog/airbnb_analysis_nairobi_40_0.png)
    A stacked bar chart showing which cancellation policy listings fall under and their management category


### Key Insights: Professional Management vs Cancellation Policy

1.  **Flexible policies are dominated by individually managed listings**The majority of listings with _Flexible_ cancellation policies are individually managed, suggesting that solo hosts prioritize flexibility to attract bookings and remain competitive.
    
2.  **Professionally managed listings are more concentrated in stricter policies**Under _Strict_ and _Moderate_ cancellation policies, professionally managed listings make up a noticeably larger share. This indicates that professional operators are more comfortable enforcing stricter terms, likely due to better demand forecasting, operational buffers, and portfolio diversification.
    
3.  **Moderate policies represent a middle ground for both host types**Both individual and professional hosts are strongly represented under _Moderate_ policies, reinforcing the idea that this policy balances guest appeal with revenue protection.
    
4.  **Firm and Limited policies are relatively rare**Very few listings adopt _Firm_ or _Limited_ cancellation policies, suggesting low market preference—possibly due to reduced guest willingness to book under highly restrictive conditions.
    

### Strategic Interpretation

Overall, **professional management is associated with stricter cancellation strategies**, while **individual hosts rely more on flexibility to drive demand**. This highlights differing risk tolerance and pricing strategies between professional operators and independent hosts in Nairobi’s Airbnb market.

If you want, I can now help you **connect this insight directly to pricing or occupancy outcomes** for a stronger narrative in your report.

## What price range attracts the most bookings (occupancy)?



```python
# Create price bins
df['price_range'] = pd.cut(df['avg_rate_per_year'], 
                            bins=[0, 5000, 10000, 15000, 20000],
                            labels=['Budget (0-5k)', 'Mid-range (5-10k)', 'Premium (10-15k)', 'Luxury (15k+)'])

# Group by price range
best_price_metric = df.groupby('price_range')['annual_occupancy'].agg(['mean', 'count']).sort_values('mean', ascending=False)

plt.figure(figsize=(10, 6))
best_price_metric['mean'].plot(kind='bar', color='steelblue')
plt.title('Average Occupancy by Price Range', fontsize=16, fontweight='bold')
plt.xlabel('Price Range', fontsize=14)
plt.ylabel('Average Occupancy (%)', fontsize=14)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

print(best_price_metric)
```

    /tmp/ipykernel_54075/1302887327.py:7: FutureWarning: The default of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
      best_price_metric = df.groupby('price_range')['annual_occupancy'].agg(['mean', 'count']).sort_values('mean', ascending=False)



    
![png](/images/blog/airbnb_analysis_nairobi_43_1.png)
    Different price bins and the occupancy rate they attract


                            mean  count
    price_range                        
    Mid-range (5-10k)  24.607586    145
    Luxury (15k+)      23.842857     14
    Budget (0-5k)      22.109615    104
    Premium (10-15k)   22.013333     30


### Insights: Average Occupancy by Price Range


1.  **Mid-range listings (KSh 5k–10k) attract the most customers**With the highest average occupancy, mid-range listings appear to offer the best balance between price and perceived value. This price segment is likely the most attractive to the majority of guests in Nairobi.
    
2.  **Luxury listings (KSh 15k+) maintain strong demand**Despite higher prices, luxury listings show relatively high occupancy, suggesting a consistent market for premium accommodation—possibly driven by business travelers, expatriates, or high-end tourists.
    
3.  **Budget listings (Below KSh 5k) do not achieve the highest occupancy**While budget listings are cheaper, their lower occupancy compared to mid-range listings suggests that **price alone is not the primary driver of demand**. Factors such as location, amenities, and perceived quality likely play a significant role.
    
4.  **Premium listings (KSh 10k–15k) show moderate occupancy**Premium listings fall between mid-range and budget listings in terms of occupancy, indicating that demand tapers slightly as prices rise beyond the mid-range threshold.
    

### Key Takeaway


> **Mid-range Airbnb listings (KSh 5k–10k) attract the highest customer demand, highlighting a value-for-money sweet spot in Nairobi’s short-term rental market.**

## How does cancellation policy affect pricing strategy?

In this segment, we check the various types of cancellation policies present within our dataset


```python
plt.figure(figsize=(10, 8))
cancellation_policy_count = df['cancellation_policy'].value_counts()
colors = ['#FF6B6B', "#6F0DD0", '#45B7D1', "#EDC914", "#4EED14"]
plt.pie(cancellation_policy_count, labels=cancellation_policy_count.index, autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 11})
plt.title("Cancellation Policy Distribution", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Display the counts
print(cancellation_policy_count)
```


    
![png](/images/blog/airbnb_analysis_nairobi_47_0.png)
    A distribution of different cancellation policies throughout our listings


    cancellation_policy
    Flexible    131
    Moderate    110
    Firm         34
    Strict       24
    Limited       1
    Name: count, dtype: int64


### Cancellation Policy Distribution

The dataset is dominated by **Flexible** and **Moderate** cancellation policies, with **43.7%** and **36.7%** listings respectively. This suggests that most hosts prefer policies that allow guests greater freedom to cancel reservations with minimal penalties.

**Firm** and **Strict** policies are less common, appearing in **11.3%** and **8.0%** listings respectively, indicating a smaller segment of hosts who prioritize booking certainty over flexibility.

Only **one** listing follows a **Limited** cancellation policy, making it negligible in the overall distribution.

### Key Insight

Overall, the distribution reflects a **guest-friendly marketplace**, where flexible cancellation options are more prevalent than restrictive policies, likely aimed at attracting short-term and undecided travelers.


```python
valid_policies = ['Flexible', 'Moderate', 'Firm', 'Strict']
cancellation_policy_vs_pricing = df[df['cancellation_policy'].isin(valid_policies)].groupby('cancellation_policy')['avg_rate_per_year'].mean().sort_values(ascending=False).round(2)
cancellation_policy_vs_pricing
```




    cancellation_policy
    Moderate    8850.24
    Strict      7568.66
    Firm        6986.59
    Flexible    6418.48
    Name: avg_rate_per_year, dtype: float64



so i got rid of **Limited** since it's only one entry, i don't think it a good representation of the insights i'd like to derive from the dataset


```python
plt.figure(figsize=(10,6))
cancellation_policy_vs_pricing.plot(kind='bar')
plt.title('Cancellation Policy and it\'s effect on Pricing of the Listing',fontsize=14,fontweight='bold' )
plt.ylabel('Average Rate per Night', fontsize=12)
plt.xlabel('Cancellation Policy', fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

```


    
![png](/images/blog/airbnb_analysis_nairobi_51_0.png)
    Different cancellation policies and the price rate they attract


### Effect of Cancellation Policy on Listing Pricing

The chart shows a **clear relationship between cancellation strictness and average nightly price**.

*   **Moderate cancellation policies** have the **highest average nightly rates**, suggesting that hosts with mid-level flexibility are able to charge a premium—possibly balancing guest trust with revenue protection.
    
*   **Strict policies** follow closely, indicating that listings enforcing tighter cancellation rules still command relatively high prices, likely due to stronger demand, desirable locations, or higher-quality listings.
    
*   **Firm policies** sit in the middle range, reflecting a moderate pricing strategy.
    
*   **Flexible cancellation policies** are associated with the **lowest average nightly rates**, suggesting that hosts may lower prices to compensate for the higher risk of last-minute cancellations.
    

###  Interpretation

Overall, **less flexible cancellation policies tend to correlate with higher pricing**, implying that hosts who restrict cancellations may do so confidently when their listings have strong market appeal. Conversely, greater flexibility appears to be used as a competitive pricing lever to attract more bookings.

#  Occupancy & Booking Patterns

## What's the average occupancy rate across the dataset?
The average occupancy rate across all active Airbnb listings in Nairobi provides a baseline measure of market demand. This metric helps contextualize how different pricing strategies, room types, and cancellation policies perform relative to the overall market.


```python
average_occupancy_rate = df['annual_occupancy'].mean().round(2)
average_occupancy_rate
```




    np.float64(23.39)



Average occupancy rate across the dataset is **23.39%**

## Do flexible cancellation policies lead to higher occupancy?


```python
valid_policies = ['Flexible', 'Moderate', 'Firm', 'Strict']
cancellation_policy_vs_occupancy = df[df['cancellation_policy'].isin(valid_policies)].groupby('cancellation_policy')['annual_occupancy'].mean().sort_values(ascending=False).round(2)
cancellation_policy_vs_occupancy
```




    cancellation_policy
    Strict      26.35
    Moderate    23.61
    Firm        23.29
    Flexible    22.42
    Name: annual_occupancy, dtype: float64



From our Findings,Listings with  **Strict** cancellation policy holds the largest percentage of annual occupancy rate at **26.35%**, Listings with **Moderate** cancellation policy come in second with **23.61%**, Firm Cancellation policy listings hold a **23.29%** annual occupancy rate and listings with **Flexible** cancellation Policy hold the least annual occupancy percentage at **22.42%**. So to answer the question, **No** 
#### Flexible Cancellation policies do not attract higher annual occupancy

## How does minimum night requirement affect booking frequency?


```python
minimum_nights_vs_booking_frequency = df.groupby('minimum_nights')['annual_occupancy'].mean().sort_values(ascending=False)
minimum_nights_vs_booking_frequency
```




    minimum_nights
    30    81.600000
    28    43.850000
    7     30.800000
    3     29.932258
    2     26.201031
    1     19.886275
    4     13.850000
    14     4.200000
    5      3.600000
    Name: annual_occupancy, dtype: float64




```python
plt.figure(figsize=(10,6))
minimum_nights_vs_booking_frequency.plot(kind='barh')
plt.title('Minimum Nights vs Booking Frequency', fontsize=14, fontweight='bold')
plt.ylabel('Minimum Nights', fontsize=12)
plt.xlabel('Annual Occupancy Percentage', fontsize=12)
plt.tight_layout()
plt.show()
```


    
![png](/images/blog/airbnb_analysis_nairobi_62_0.png)
    A horizontal bar showing minimum nights requirement and the occupancy rate they attract


**1\. Long-Term Stays Dominate Annual Occupancy**

*   **30-Day Stays are King:** The most significant finding is that bookings with a minimum stay of **30 nights** account for the highest annual occupancy percentage by a wide margin, reaching approximately **82%**.
    
*   **Strong Performance of 28-Day Stays:** The second-highest occupancy is for **28-night** minimum stays, at around **44%**.
    
*   **Conclusion:** This suggests a very strong market for monthly or near-monthly rentals, which could be driven by corporate housing, digital nomads, or temporary relocations. These long stays are the primary drivers of occupancy in this dataset.
    

**2\. Weekly and Long-Weekend Stays are Important Secondary Drivers**

*   **The "Sweet Spot" for Shorter Stays:** Minimum stays of **7 nights** and **3 nights** have very similar and significant occupancy percentages, both hovering around the **30-31%** mark.
    
*   **Conclusion:** There is substantial demand for weekly vacations and extended weekend trips. For hosts not targeting the monthly market, these two durations appear to be the most effective for maintaining occupancy.
    

**3\. Very Short Stays Contribute Less to Overall Occupancy**

*   **1-2 Night Stays:** While extremely common in the short-term rental market, minimum stays of **2 nights** (~26%) and **1 night** (~20%) contribute less to the total annual occupancy than the 3, 7, 28, and 30-night options.
    
*   **Implication:** This could indicate that while these bookings may be frequent, the higher turnover results in more unbooked "gap days," leading to a lower overall occupancy percentage over the course of a year compared to longer, more continuous stays.
    

**4\. Specific Durations are Less Effective**

*   **Low Occupancy for 4, 5, and 14 Nights:** Minimum stays of **4 nights** (~14%), **14 nights** (~4%), and **5 nights** (~3%) show the lowest annual occupancy percentages.
    
*   **Conclusion:** These specific booking windows seem to be less popular with guests or less successfully utilized by hosts compared to the standard 1-night, weekend (2-3 nights), weekly (7 nights), or monthly models.
    

**Strategic Implication for Hosts:** To maximize annual occupancy, the data suggests targeting the **30+ day market** is the most effective strategy. If that is not feasible, focusing on **7-night (weekly)** or **3-night (long weekend)** minimums would be better than setting minimums of 1, 2, 4, 5, or 14 nights.

**Key Insight** The data suggests that decreasing booking frequency (by raising minimum nights to 28+) actually increases your overall business performance (occupancy).

## Which listing types have the highest occupancy rates?


```python
listing_types_vs_occupancy_rate = df.groupby('room_type')['annual_occupancy'].mean().sort_values(ascending=False).round(2)
listing_types_vs_occupancy_rate
```




    room_type
    entire_home     25.05
    private_room    15.08
    hotel_room       3.00
    Name: annual_occupancy, dtype: float64



**Entire Homes** are the most common listing type to be booked at a rate of **25.05%**, followed by **Private Room** at a rate of **15.08%** and lastly**Hotel Rooms** making up **3.0%** of the total occupancy rate

## How many listings per host on average?


```python
no_of_hosts = df['host_id'].unique()
len(no_of_hosts)
```




    205



Our dataset has 205 unique hosts all who own either one or a bunch of listings within Nairobi


```python
no_of_listing_per_host = (
    df.groupby('host_id')
      .agg(
          host_name=('host_name', 'first'),
          number_of_listings=('listing_id', 'count')
      ).sort_values(by='number_of_listings',ascending=False)
)

no_of_listing_per_host
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>host_name</th>
      <th>number_of_listings</th>
    </tr>
    <tr>
      <th>host_id</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>35945714</th>
      <td>Samra Apartments</td>
      <td>19</td>
    </tr>
    <tr>
      <th>308523342</th>
      <td>Damaris</td>
      <td>8</td>
    </tr>
    <tr>
      <th>8042369</th>
      <td>Sherry</td>
      <td>7</td>
    </tr>
    <tr>
      <th>145631743</th>
      <td>Diana</td>
      <td>6</td>
    </tr>
    <tr>
      <th>43851715</th>
      <td>Duncan</td>
      <td>5</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>322215915</th>
      <td>David</td>
      <td>1</td>
    </tr>
    <tr>
      <th>326653326</th>
      <td>Alain</td>
      <td>1</td>
    </tr>
    <tr>
      <th>327031637</th>
      <td>Lillian</td>
      <td>1</td>
    </tr>
    <tr>
      <th>363302880</th>
      <td>Nyangaga</td>
      <td>1</td>
    </tr>
    <tr>
      <th>429266147</th>
      <td>Anata</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>205 rows × 2 columns</p>
</div>




```python
top_host = no_of_listing_per_host.iloc[0]
print(f"Top host: {top_host['host_name']} with {top_host['number_of_listings']} listings")
```

    Top host: Samra Apartments with 19 listings



```python
print(f"Total hosts: {len(no_of_listing_per_host)}")
print(f"Average listings per host: {no_of_listing_per_host['number_of_listings'].mean():.2f}")
print(f"Max listings by one host: {no_of_listing_per_host['number_of_listings'].max()}")
print(f"Min listings by one host: {no_of_listing_per_host['number_of_listings'].min()}")
```

    Total hosts: 205
    Average listings per host: 1.46
    Max listings by one host: 19
    Min listings by one host: 1


The dataset contains **205 unique hosts**, with an **average of 1.46 listings per host**, indicating that the market is largely composed of small-scale hosts. Most hosts operate **a single listing**, as reflected by the minimum of one listing per host. However, there is evidence of **professional or portfolio-style hosting**, with the largest host, **Samra Apartments**, managing **19 listings**. This highlights a market structure dominated by individual hosts alongside a small number of high-volume operators.

# Geographic/Neighborhood Patterns


```python
plt.figure(figsize=(8, 6))
plt.scatter(df['longitude'], df['latitude'], c=df['avg_rate_per_year'], alpha=0.6)
plt.colorbar(label='Average Nightly Rate')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Pricing Distribution Across Nairobi')
plt.show()
```


    
![png](/images/blog/airbnb_analysis_nairobi_75_0.png)
    A distribution of our listings



```python
NAIROBI_BOUNDS = {
    "lat_min": -1.5,
    "lat_max": -1.1,
    "lon_min": 36.6,
    "lon_max": 37.1
}

```


```python
df_nairobi = df[
    (df['latitude'] >= NAIROBI_BOUNDS['lat_min']) &
    (df['latitude'] <= NAIROBI_BOUNDS['lat_max']) &
    (df['longitude'] >= NAIROBI_BOUNDS['lon_min']) &
    (df['longitude'] <= NAIROBI_BOUNDS['lon_max'])
].copy()

print(f"Listings before: {len(df)}")
print(f"Listings in Nairobi: {len(df_nairobi)}")

```

    Listings before: 300
    Listings in Nairobi: 300



```python
import folium
from IPython.display import display

m = folium.Map(
    location=[-1.286389, 36.817223],  # Nairobi CBD
    zoom_start=12,
    min_zoom=11,
    max_zoom=16,
    max_bounds=True,
    bounds=NAIROBI_BOUNDS,
    tiles="OpenStreetMap"
)

```


```python
#m.fit_bounds(NAIROBI_BOUNDS)
```


```python
for row in df_nairobi.itertuples():
    if row.avg_rate_per_year < 5000:
        color = '#2EC4B6'   # Budget
    elif row.avg_rate_per_year < 10000:
        color = '#1F77B4'   # Mid-range
    elif row.avg_rate_per_year < 15000:
        color = '#FF9F1C'   # Premium
    else:
        color = '#E63946'   # Luxury

    # Create popup with more details
    popup_text = f"""
    <b style='font-size: 14px'>{row.listing_name}</b><br>
    <b>Type:</b> {row.listing_type}<br>
    <b>Room:</b> {row.room_type}<br>
    <b>Rating:</b> {row.rating_overall}/5.0<br>
    <b>Price:</b> KSh {row.avg_rate_per_year:.0f}/night
    """
    
    folium.CircleMarker(
        location=[row.latitude, row.longitude],
        radius=4,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

display(m)
```

![image](/images/blog/nairobi_heatmap.webp)
#### STEP 2: Prepare data for clustering

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

X = neighbourhoods_vs_pricing[['avg_rate_per_year']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

#### STEP 3: Apply KMeans clustering


```python
kmeans = KMeans(n_clusters=3, random_state=42)
neighbourhoods_vs_pricing['price_cluster'] = kmeans.fit_predict(X_scaled)

```

#### STEP 4: Inspect the clusters


```python
neighbourhoods_vs_pricing.sort_values('avg_rate_per_year')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>suburb</th>
      <th>avg_rate_per_year</th>
      <th>price_cluster</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Nyayo Highrise ward</td>
      <td>1427.50</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>South C</td>
      <td>1717.10</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Pipeline</td>
      <td>1819.50</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>South B</td>
      <td>2341.67</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mugumo-ini ward</td>
      <td>2796.90</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Nairobi West</td>
      <td>2857.30</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>CBD division</td>
      <td>3373.79</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Komarock ward</td>
      <td>4296.90</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Imara Daima ward</td>
      <td>4452.97</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Harambee ward</td>
      <td>4460.60</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Githurai division</td>
      <td>5098.80</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>South C ward</td>
      <td>5177.70</td>
      <td>0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Kangemi division</td>
      <td>5242.46</td>
      <td>0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Nairobi West ward</td>
      <td>5552.50</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Kawangware division</td>
      <td>5684.97</td>
      <td>0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Roysambu division</td>
      <td>6030.61</td>
      <td>0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Woodley/Kenyatta/Golf Course ward</td>
      <td>6614.90</td>
      <td>2</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Kasarani location</td>
      <td>6667.00</td>
      <td>2</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Kilimani division</td>
      <td>7002.30</td>
      <td>2</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Tassia</td>
      <td>7173.10</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Highridge division</td>
      <td>8471.39</td>
      <td>2</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Karen C</td>
      <td>8600.96</td>
      <td>2</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Karen</td>
      <td>8606.50</td>
      <td>2</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Karen Hardy</td>
      <td>10907.72</td>
      <td>2</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Karen ward</td>
      <td>17108.63</td>
      <td>2</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Lower Savannah ward</td>
      <td>37484.90</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



#### STEP 5: Visualization


```python
sns.barplot(
    data=neighbourhoods_vs_pricing,
    x='price_cluster',
    y='avg_rate_per_year'
)
plt.title("Average Nightly Rate by Neighborhood Price Cluster")
plt.show()

```


    
![png](/images/blog/airbnb_analysis_nairobi_94_0.png)
    Price clusters and the rate they fall under


*   **Cluster 0 (Economy/Budget):** This category contains the highest volume of listings, representing the lower-tier accommodations.
    
*   **Cluster 2 (Mid-range):** These listings represent the middle tier of the market.
    
*   **Cluster 1 (High-end/Outlier):** This cluster contains only a single listing, suggesting it is unique or an outlier."

## Do certain neighborhoods favor specific room types?

#### Create a neighborhood × room type distribution


```python
neighborhood_room_type = (
    df
    .groupby(['suburb', 'room_type'])
    .size()
    .reset_index(name='count')
)
```


```python
room_type_pivot = neighborhood_room_type.pivot(
    index='suburb',
    columns='room_type',
    values='count'
).fillna(0)
room_type_pivot
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>room_type</th>
      <th>entire_home</th>
      <th>hotel_room</th>
      <th>private_room</th>
    </tr>
    <tr>
      <th>suburb</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>CBD division</th>
      <td>8.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>Githurai division</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>Harambee ward</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Highridge division</th>
      <td>31.0</td>
      <td>1.0</td>
      <td>13.0</td>
    </tr>
    <tr>
      <th>Imara Daima ward</th>
      <td>3.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Kangemi division</th>
      <td>7.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Karen</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>3.0</td>
    </tr>
    <tr>
      <th>Karen C</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>Karen Hardy</th>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Karen ward</th>
      <td>17.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>Kasarani location</th>
      <td>5.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Kawangware division</th>
      <td>3.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Kilimani division</th>
      <td>130.0</td>
      <td>0.0</td>
      <td>21.0</td>
    </tr>
    <tr>
      <th>Komarock ward</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Lower Savannah ward</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Mugumo-ini ward</th>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Nairobi West</th>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Nairobi West ward</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Nyayo Highrise ward</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>Pipeline</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Roysambu division</th>
      <td>13.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>South B</th>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>South C</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>South C ward</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Tassia</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>Woodley/Kenyatta/Golf Course ward</th>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
room_type_pivot_sorted = (
    room_type_pivot
    .assign(total=room_type_pivot.sum(axis=1))
    .sort_values('total')
    .drop(columns='total')
)

```


```python
room_type_pivot_sorted.plot(
    kind='barh',
    stacked=True,
    figsize=(12, 10)
)
plt.title("Room Type Distribution by Neighborhood")
plt.xlabel("Number of Listings")
plt.ylabel("Suburb")
plt.tight_layout()
plt.show()

```


    
![png](/images/blog/airbnb_analysis_nairobi_101_0.png)
    room distribution by suburb


Neighborhood × Room Type Insights
---------------------------------

### 1\. **Strong geographic concentration**

*   **Kilimani division** overwhelmingly dominates the market, with the highest number of listings by a wide margin.
    
*   **Highridge division** follows as a distant second.
    
*   All other neighborhoods have relatively **low listing density**, many with fewer than 10 listings.
    

**Insight:** Airbnb supply in Nairobi is highly concentrated in a few prime neighborhoods rather than evenly distributed.

### 2\. **Entire homes dominate across neighborhoods**

*   **Entire homes** make up the majority of listings in almost every suburb.
    
*   This dominance is most pronounced in **Kilimani** and **Highridge**, indicating strong demand for full-unit stays in these areas.
    

**Interpretation:** These neighborhoods likely attract:

*   Longer stays
    
*   Families, business travelers, or groups
    
*   Guests prioritizing privacy and space
    

### 3\. **Private rooms play a secondary role**

*   **Private rooms** appear mainly in:
    
    *   Kilimani
        
    *   Highridge
        
    *   Karen-related areas
        
*   Their presence is limited elsewhere.
    

**Interpretation:** Private rooms serve as a **price-sensitive alternative** in high-demand areas but are not a primary offering city-wide.

### 4\. **Hotel rooms are extremely rare**

*   **Hotel room listings are almost nonexistent**, appearing only marginally in a few neighborhoods.
    

**Insight:** Airbnb supply in this dataset is driven by **individual hosts and residential properties**, not traditional hospitality players.

### 5\. **Neighborhood character matters**

*   **Karen ward** shows lower volume but a mix that leans toward **entire homes**, consistent with its low-density, high-end residential profile.
    
*   Peripheral neighborhoods show **minimal diversification**, often only one room type.

## Which areas have the highest revenue potential?


```python
area_revenue = (
    df
    .groupby('suburb')
    .agg(
        avg_annual_revenue=('revenue_per_year', 'mean'),
        avg_nightly_rate=('avg_rate_per_year', 'mean'),
        avg_occupancy=('annual_occupancy', 'mean'),
        listings_count=('listing_id', 'count')
    )
    .sort_values('avg_annual_revenue', ascending=False)
    .round(2)
)

area_revenue.head(10)

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>avg_annual_revenue</th>
      <th>avg_nightly_rate</th>
      <th>avg_occupancy</th>
      <th>listings_count</th>
    </tr>
    <tr>
      <th>suburb</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Karen ward</th>
      <td>1962535.22</td>
      <td>17108.63</td>
      <td>36.13</td>
      <td>18</td>
    </tr>
    <tr>
      <th>Karen</th>
      <td>811678.25</td>
      <td>8606.50</td>
      <td>35.85</td>
      <td>4</td>
    </tr>
    <tr>
      <th>Nairobi West ward</th>
      <td>712218.00</td>
      <td>5552.50</td>
      <td>37.60</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Tassia</th>
      <td>702593.00</td>
      <td>7173.10</td>
      <td>35.40</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Kangemi division</th>
      <td>661358.00</td>
      <td>5242.46</td>
      <td>21.89</td>
      <td>7</td>
    </tr>
    <tr>
      <th>Karen Hardy</th>
      <td>648590.50</td>
      <td>10907.72</td>
      <td>18.00</td>
      <td>6</td>
    </tr>
    <tr>
      <th>Kilimani division</th>
      <td>521143.23</td>
      <td>7002.30</td>
      <td>24.41</td>
      <td>151</td>
    </tr>
    <tr>
      <th>Highridge division</th>
      <td>509475.96</td>
      <td>8471.39</td>
      <td>23.61</td>
      <td>45</td>
    </tr>
    <tr>
      <th>Harambee ward</th>
      <td>502857.00</td>
      <td>4460.60</td>
      <td>34.40</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Lower Savannah ward</th>
      <td>471464.00</td>
      <td>37484.90</td>
      <td>6.50</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
area_revenue.head(10)['avg_annual_revenue'] \
    .sort_values() \
    .plot(kind='barh', figsize=(10, 6))

plt.title("Top 10 Areas by Average Annual Revenue")
plt.xlabel("Average Annual Revenue (KSh)")
plt.ylabel("Suburb")
plt.show()

```


    
![png](/images/blog/airbnb_analysis_nairobi_105_0.png)
    room distribution by suburb


#### **1\. The Luxury Tier: Karen’s "High-Value" Dominance**

*   **Performance:** **Karen Ward** is the undisputed market leader, generating nearly **KSh 2,000,000** annually—more than double the next highest contender.
    
*   **The Strategy:** This dominance is driven by high **Average Daily Rates (ADR)** rather than sheer volume. These listings (villas, large homes) cater to the "Long Stay" market (diplomats, expats) where a single booking can secure months of revenue.
    
*   **Verdict:** High entry cost, but unrivaled revenue per booking.
    

#### **2\. The Efficiency Tier: The Hidden Gems (Tassia & Nairobi West)**

*   **Performance:** Surprisingly, lower-middle-income areas like **Nairobi West** (~KSh 700k) and **Tassia** (~KSh 680k) significantly outperform premium hubs.
    
*   **The Strategy:** These areas thrive on a **Volume/Occupancy** model. With lower nightly rates but consistent local demand (traders, short-term work stays), they avoid the "vacancy gaps" that plague seasonal tourist spots.
    
*   **Verdict:** Lower entry cost with higher yield efficiency.
    

#### **3\. The Saturated Tier: The "Popularity Trap" (Kilimani & Highridge)**

*   **Performance:** despite being the most famous rental hubs, **Kilimani** and **Highridge** appear in the bottom half of the top 10 (averaging ~KSh 500k).
    
*   **The Strategy:** These areas suffer from **Oversupply**. The sheer number of apartments creates fierce price competition, diluting the _average_ revenue per host. While top-tier units earn well, the "average" unit struggles to match the returns of less saturated areas.
    
*   **Verdict:** High demand is offset by extreme competition; success here requires a standout product.

# Quality & Features

## How many amenities do high-revenue listings typically have?

#### Step 1: Define high-revenue listings


```python
# Define high-revenue threshold
high_revenue_threshold = df['revenue_per_year'].quantile(0.75)

df['high_revenue'] = (
    df['revenue_per_year'] >= high_revenue_threshold
)
```

#### Step 2: Convert amenities into a count


```python
# Create amenities count
df['amenities_count'] = (
    df['amenities']
    .fillna('')
    .apply(lambda x: len(str(x).split(',')))
)

```

#### Step 3: Compare high vs non-high revenue listings


```python
amenities_vs_revenue = (
    df
    .groupby('high_revenue')['amenities_count']
    .agg(['mean', 'median', 'min', 'max', 'count'])
    .round(1)
)

amenities_vs_revenue

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>mean</th>
      <th>median</th>
      <th>min</th>
      <th>max</th>
      <th>count</th>
    </tr>
    <tr>
      <th>high_revenue</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>False</th>
      <td>34.8</td>
      <td>33.0</td>
      <td>11</td>
      <td>78</td>
      <td>225</td>
    </tr>
    <tr>
      <th>True</th>
      <td>38.2</td>
      <td>37.0</td>
      <td>14</td>
      <td>76</td>
      <td>75</td>
    </tr>
  </tbody>
</table>
</div>



#### Step 4: Visualization


```python
sns.boxplot(
    data=df,
    x='high_revenue',
    y='amenities_count'
)

plt.xticks([0, 1], ['Lower Revenue', 'High Revenue'])
plt.title("Amenities Count vs Revenue Tier")
plt.ylabel("Number of Amenities")
plt.xlabel("")
plt.show()
```


    
![png](/images/blog/airbnb_analysis_nairobi_116_0.png)
    amenities and the revenue they attract


From the box plot, **high-revenue listings typically have about** _**35–40 amenities**_.

More precisely:

*   The **median** (the line inside the box) is around **36–37 amenities**
    
*   Most high-revenue listings (the interquartile range) fall roughly between **30 and 42 amenities**
    

So a “typical” high-revenue listing offers **mid-to-high 30s in amenities**, slightly more than lower-revenue listings.

## What's the relationship between listing name length and bookings?

#### Step 1: Define the variables


```python
df['listing_name_length'] = (
    df['listing_name']
    .fillna('')
    .str.len()
)

```

#### Step 2: Measure correlation


```python
correlation = df['listing_name_length'].corr(
    df['reserved_days_in_year']
)

correlation
```




    np.float64(0.10077962524781812)



#### Weak Positive


```python
df['name_length_bin'] = pd.qcut(
    df['listing_name_length'],
    q=4,
    labels=['Short', 'Medium', 'Long', 'Very Long']
)

df.groupby('name_length_bin')['reserved_days_in_year'].mean().sort_values(ascending=False)

```

    /tmp/ipykernel_54075/1443461262.py:7: FutureWarning: The default of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
      df.groupby('name_length_bin')['reserved_days_in_year'].mean().sort_values(ascending=False)





    name_length_bin
    Very Long    86.812500
    Long         73.047059
    Short        70.526316
    Medium       65.720000
    Name: reserved_days_in_year, dtype: float64



#### Step 3: Visualize the relationship


```python
sns.scatterplot(
    data=df,
    x='listing_name_length',
    y='reserved_days_in_year',
    alpha=0.6
)

sns.regplot(
    data=df,
    x='listing_name_length',
    y='reserved_days_in_year',
    scatter=False,
    color='red'
)

plt.title("Listing Name Length vs Booked Nights per Year")
plt.xlabel("Listing Name Length (characters)")
plt.ylabel("Booked Nights per Year")
plt.show()

```


    
![png](/images/blog/airbnb_analysis_nairobi_126_0.png)
    Correlation between listing name and booked nights per year


### Direction of the relationship

*   The **red regression line slopes slightly upward**, indicating a **weak positive relationship** between listing name length and booked nights per year.
    
*   This means that, _on average_, listings with longer names tend to receive **slightly more bookings**, but the effect is **not strong**.
    

### Strength of the relationship

*   The points are **widely scattered** around the line.
    
*   This high dispersion shows that **listing name length alone explains very little** of the variation in bookings.
    
*   Many listings with long names still have low bookings, and some short names perform very well.
    

**Conclusion:** The relationship exists, but it is **weak**.

### Practical interpretation

*   Longer names likely help by:
    
    *   Including keywords (location, amenities, “near CBD”, “luxury”, etc.)
        
    *   Improving clarity and search visibility
        
*   However, bookings are **far more influenced** by:
    
    *   Location
        
    *   Price
        
    *   Reviews
        
    *   Amenities
        
    *   Professional management


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>listing_id</th>
      <th>listing_name</th>
      <th>listing_type</th>
      <th>room_type</th>
      <th>cover_photo_url</th>
      <th>photos_count</th>
      <th>minimum_nights</th>
      <th>cancellation_policy</th>
      <th>professional_management</th>
      <th>registration</th>
      <th>...</th>
      <th>price_range</th>
      <th>neighbourhood</th>
      <th>suburb</th>
      <th>county</th>
      <th>city</th>
      <th>postcode</th>
      <th>high_revenue</th>
      <th>amenities_count</th>
      <th>listing_name_length</th>
      <th>name_length_bin</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>75683</td>
      <td>Kiloranhouse Apt Prime Bedroom</td>
      <td>Private room in home</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/5499026/ef...</td>
      <td>13</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Mid-range (5-10k)</td>
      <td>Kilimani ward</td>
      <td>Kilimani division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>30728</td>
      <td>False</td>
      <td>42</td>
      <td>30</td>
      <td>Short</td>
    </tr>
    <tr>
      <th>1</th>
      <td>471581</td>
      <td>Located In a Serene Environment</td>
      <td>Entire cottage</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/6434524/bc...</td>
      <td>37</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Mid-range (5-10k)</td>
      <td>Roysambu location</td>
      <td>Roysambu division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>31224</td>
      <td>True</td>
      <td>24</td>
      <td>31</td>
      <td>Short</td>
    </tr>
    <tr>
      <th>2</th>
      <td>906958</td>
      <td>Makena's Place Karen - Flamingo Room</td>
      <td>Private room in cottage</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/68ecc57f-d...</td>
      <td>29</td>
      <td>1</td>
      <td>Firm</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Mid-range (5-10k)</td>
      <td>None</td>
      <td>Karen</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>00505</td>
      <td>False</td>
      <td>30</td>
      <td>36</td>
      <td>Medium</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1023556</td>
      <td>Guesthouse Near Nairobi National Park &amp; Airport</td>
      <td>Entire guesthouse</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/ddd8badc-1...</td>
      <td>20</td>
      <td>1</td>
      <td>Flexible</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Budget (0-5k)</td>
      <td>None</td>
      <td>Mugumo-ini ward</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>00517</td>
      <td>False</td>
      <td>33</td>
      <td>47</td>
      <td>Long</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1237886</td>
      <td>Hob House</td>
      <td>Room in bed and breakfast</td>
      <td>hotel_room</td>
      <td>https://a0.muscache.com/im/pictures/cbdab7e1-f...</td>
      <td>8</td>
      <td>1</td>
      <td>Flexible</td>
      <td>True</td>
      <td>False</td>
      <td>...</td>
      <td>Luxury (15k+)</td>
      <td>Highridge location</td>
      <td>Highridge division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>11403</td>
      <td>False</td>
      <td>42</td>
      <td>9</td>
      <td>Short</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>295</th>
      <td>42123446</td>
      <td>Mvuli Luxury Suites</td>
      <td>Entire rental unit</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/238557fd-c...</td>
      <td>24</td>
      <td>1</td>
      <td>Firm</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Budget (0-5k)</td>
      <td>Ngara location</td>
      <td>CBD division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>45046</td>
      <td>False</td>
      <td>32</td>
      <td>19</td>
      <td>Short</td>
    </tr>
    <tr>
      <th>296</th>
      <td>42139551</td>
      <td>Modern 1BR | King Bed | Fast Wi-Fi | Near CBD</td>
      <td>Entire condo</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/a10f889a-4...</td>
      <td>27</td>
      <td>1</td>
      <td>Flexible</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Mid-range (5-10k)</td>
      <td>Kilimani ward</td>
      <td>Kilimani division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>30728</td>
      <td>False</td>
      <td>53</td>
      <td>45</td>
      <td>Long</td>
    </tr>
    <tr>
      <th>297</th>
      <td>42187559</td>
      <td>Cosy &amp; Airy Studio with Balcony WI-FI and Netflix</td>
      <td>Tiny home</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/miso/Hosti...</td>
      <td>43</td>
      <td>1</td>
      <td>Moderate</td>
      <td>True</td>
      <td>False</td>
      <td>...</td>
      <td>Budget (0-5k)</td>
      <td>Kangemi location</td>
      <td>Kangemi division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>29326</td>
      <td>False</td>
      <td>60</td>
      <td>49</td>
      <td>Very Long</td>
    </tr>
    <tr>
      <th>298</th>
      <td>42207619</td>
      <td>Kazuri Ivy Serene &amp; Spacious Nairobi Apartment</td>
      <td>Entire rental unit</td>
      <td>entire_home</td>
      <td>https://a0.muscache.com/im/pictures/hosting/Ho...</td>
      <td>19</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Budget (0-5k)</td>
      <td>Ngara location</td>
      <td>CBD division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>45046</td>
      <td>False</td>
      <td>20</td>
      <td>46</td>
      <td>Long</td>
    </tr>
    <tr>
      <th>299</th>
      <td>42223689</td>
      <td>Airy &amp; Light-Filled: Indoor-Outdoor Home-Stay</td>
      <td>Private room in rental unit</td>
      <td>private_room</td>
      <td>https://a0.muscache.com/im/pictures/fd146f8e-5...</td>
      <td>17</td>
      <td>2</td>
      <td>Moderate</td>
      <td>False</td>
      <td>False</td>
      <td>...</td>
      <td>Budget (0-5k)</td>
      <td>Kileleshwa location</td>
      <td>Kilimani division</td>
      <td>None</td>
      <td>Nairobi</td>
      <td>54102</td>
      <td>False</td>
      <td>55</td>
      <td>45</td>
      <td>Long</td>
    </tr>
  </tbody>
</table>
<p>300 rows × 52 columns</p>
</div>



# Market Opportunities

## What's underrepresented in the market (low supply, high demand)?

#### Create price bands


```python
price_bins = [0, 3000, 6000, 10000, 15000, df['avg_rate_per_year'].max()]
price_labels = [
    'Low (0–3k)',
    'Lower-Mid (3k–6k)',
    'Mid (6k–10k)',
    'Upper-Mid (10k–15k)',
    'Premium (15k+)'
]

df['price_band'] = pd.cut(
    df['avg_rate_per_year'],
    bins=price_bins,
    labels=price_labels,
    include_lowest=True
)

```

#### Define supply and demand


```python
market_summary = (
    df.groupby(['room_type', 'price_band'])
      .agg(
          listings_count=('listing_id', 'count'),
          avg_occupancy=('annual_occupancy', 'mean'),
          avg_revenue=('revenue_per_year', 'mean')
      )
      .reset_index()
)

```

    /tmp/ipykernel_54075/1390846018.py:2: FutureWarning: The default of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
      df.groupby(['room_type', 'price_band'])


#### Establish “low supply” and “high demand” thresholds


```python
supply_threshold = market_summary['listings_count'].median()
occupancy_threshold = market_summary['avg_occupancy'].median()
revenue_threshold = market_summary['avg_revenue'].median()

```

#### Flag underrepresented segments


```python
market_summary['underrepresented'] = (
    (market_summary['listings_count'] < supply_threshold) &
    (
        (market_summary['avg_occupancy'] > occupancy_threshold) |
        (market_summary['avg_revenue'] > revenue_threshold)
    )
)

underrepresented_segments = market_summary[
    market_summary['underrepresented']
].sort_values(['avg_occupancy', 'avg_revenue'], ascending=False)

underrepresented_segments

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>room_type</th>
      <th>price_band</th>
      <th>listings_count</th>
      <th>avg_occupancy</th>
      <th>avg_revenue</th>
      <th>underrepresented</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>14</th>
      <td>private_room</td>
      <td>Premium (15k+)</td>
      <td>5</td>
      <td>5.32</td>
      <td>363316.2</td>
      <td>True</td>
    </tr>
  </tbody>
</table>
</div>



## Are there price gaps where new listings could compete?

#### Measure supply per price band


```python
supply_by_price = (
    df.groupby('price_band')
      .agg(
          listings_count=('listing_id', 'count'),
          avg_price=('avg_rate_per_year', 'mean')
      )
      .reset_index()
)

```

    /tmp/ipykernel_54075/1042693843.py:2: FutureWarning: The default of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
      df.groupby('price_band')


#### Measure demand/performance per price band


```python
performance_by_price = (
    df.groupby('price_band')
      .agg(
          avg_occupancy=('annual_occupancy', 'mean'),
          avg_revenue=('revenue_per_year', 'mean')
      )
      .reset_index()
)

```

    /tmp/ipykernel_54075/2880606656.py:2: FutureWarning: The default of observed=False is deprecated and will be changed to True in a future version of pandas. Pass observed=False to retain current behavior or observed=True to adopt the future default and silence this warning.
      df.groupby('price_band')


#### Combine supply + performance


```python
price_gap_analysis = supply_by_price.merge(
    performance_by_price,
    on='price_band'
)

price_gap_analysis.sort_values('listings_count')

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>price_band</th>
      <th>listings_count</th>
      <th>avg_price</th>
      <th>avg_occupancy</th>
      <th>avg_revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>4</th>
      <td>Premium (15k+)</td>
      <td>21</td>
      <td>23956.961905</td>
      <td>23.223810</td>
      <td>1.874120e+06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Upper-Mid (10k–15k)</td>
      <td>30</td>
      <td>11954.396667</td>
      <td>22.013333</td>
      <td>8.627922e+05</td>
    </tr>
    <tr>
      <th>0</th>
      <td>Low (0–3k)</td>
      <td>41</td>
      <td>2346.365854</td>
      <td>23.697561</td>
      <td>1.668768e+05</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Lower-Mid (3k–6k)</td>
      <td>97</td>
      <td>4616.963918</td>
      <td>23.797938</td>
      <td>3.463240e+05</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mid (6k–10k)</td>
      <td>111</td>
      <td>7618.214414</td>
      <td>23.310811</td>
      <td>5.501002e+05</td>
    </tr>
  </tbody>
</table>
</div>



#### Identify price gaps


```python
price_gap_analysis['potential_gap'] = (
    (price_gap_analysis['listings_count'] < price_gap_analysis['listings_count'].median()) &
    (price_gap_analysis['avg_occupancy'] > price_gap_analysis['avg_occupancy'].median())
)

price_gap_analysis

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>price_band</th>
      <th>listings_count</th>
      <th>avg_price</th>
      <th>avg_occupancy</th>
      <th>avg_revenue</th>
      <th>potential_gap</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Low (0–3k)</td>
      <td>41</td>
      <td>2346.365854</td>
      <td>23.697561</td>
      <td>1.668768e+05</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Lower-Mid (3k–6k)</td>
      <td>97</td>
      <td>4616.963918</td>
      <td>23.797938</td>
      <td>3.463240e+05</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mid (6k–10k)</td>
      <td>111</td>
      <td>7618.214414</td>
      <td>23.310811</td>
      <td>5.501002e+05</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Upper-Mid (10k–15k)</td>
      <td>30</td>
      <td>11954.396667</td>
      <td>22.013333</td>
      <td>8.627922e+05</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Premium (15k+)</td>
      <td>21</td>
      <td>23956.961905</td>
      <td>23.223810</td>
      <td>1.874120e+06</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



## Which listing types have declining revenue trends?

Revenue trend analysis typically requires time-series data. As this dataset provides a snapshot of listing performance rather than longitudinal observations, it does not support direct analysis of declining or increasing revenue trends by listing type. Instead, the analysis focuses on comparing current revenue performance across listing categories.