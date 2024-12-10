# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:27:37 2024

@author: anneg
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the filtered data (assuming it's saved as 'counts_filtered.csv')
df = pd.read_csv('C:/Users/anneg/Master_jaar_2/MORE/Group_project/counts_filtered.csv')

# Verify column names for vehicle counts, lat, long, and year
vehicle_columns = ["HGVs_2_rigid_axle","HGVs_3_rigid_axle","HGVs_4_or_more_rigid_axle","HGVs_3_or_4_articulated_axle","HGVs_5_articulated_axle","HGVs_6_articulated_axle","all_HGVs"]  # adjust as needed
lat_column = 'latitude'
long_column = 'longitude'
year_column = 'year'
total_trucks_by_year = df.groupby(year_column)[vehicle_columns].sum()
years = total_trucks_by_year.index.tolist()

# Check if all required columns exist
assert all(col in df.columns for col in vehicle_columns + [lat_column, long_column, year_column])

# --- 1. Histograms for each vehicle type per year ---

# Create histograms for vehicle counts, one for each vehicle type
# Calculate total number of trucks for each type by year
# Calculate total number of trucks for each type by year


# Determine chunk size
chunk_size = 3  # Number of years per figure

# Plot in chunks
for start in range(0, len(years), chunk_size):
    # Create a new figure for each chunk
    plt.figure(figsize=(12, 10))
    chunk_years = years[start:start + chunk_size]  # Select years for this chunk
    
    for i, year in enumerate(chunk_years, 1):
        plt.subplot(1, len(chunk_years), i)  # Adjust layout to fit chunk size
        year_totals = total_trucks_by_year.loc[year]
        plt.bar(vehicle_columns, year_totals, alpha=0.7, color='skyblue')
        
        plt.title(f'Total Trucks by Type in Year {year}')
        plt.xlabel('Truck Type')
        plt.ylabel('Total Count')
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'total_trucks_years_{chunk_years[0]}_to_{chunk_years[-1]}.png', dpi=300)
    plt.show()



# --- 2. Scatterplot of lat-long data with color based on total number of vehicles ---
# =============================================================================
# 
# # Create a new column that sums all vehicle counts to get total vehicles
# years = total_trucks_by_year.index.tolist()
# df['total_vehicles'] = df[vehicle_columns].sum(axis=1)/len(years)
# 
# # 2.1 Scatterplot for the whole dataset (total number of vehicles)
# plt.figure(figsize=(8, 6))
# sns.scatterplot(x='longitude', y='latitude', hue='total_vehicles', data=df, palette='viridis', size='total_vehicles', sizes=(20, 200))
# plt.title('Scatterplot of Lat-Long with Total Number of Vehicles')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.legend(title='Total Vehicles', loc='upper right')
# plt.savefig('busyroads.jpg')
# plt.show()
# 
# 
# # Verify column for road identifiers
# road_column = 'road_name'  # Replace with the actual column name representing roads
# 
# # Calculate total trucks for each road
# total_trucks_by_road = df.groupby(road_column)[vehicle_columns].sum()
# 
# # Add a column for the total across all truck types
# total_trucks_by_road['total_trucks'] = total_trucks_by_road.sum(axis=1)
# 
# # Sort roads by the total trucks in descending order
# sorted_roads = total_trucks_by_road.sort_values(by='total_trucks', ascending=False)
# 
# # Display the sorted list of roads
# print(sorted_roads[['total_trucks']])
# =============================================================================
