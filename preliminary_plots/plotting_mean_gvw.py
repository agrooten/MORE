# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 09:28:59 2025

@author: anneg
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx
import geopandas as gpd

# Load the simulated data
mean_df = pd.read_csv('C:/Users/anneg/Master_jaar_2/MORE/MORE/mean_gvw.csv')



gdf = gpd.GeoDataFrame(
    mean_df,
    geometry=gpd.points_from_xy(mean_df['longitude'], mean_df['latitude']),
    crs="EPSG:4326"  # WGS84 coordinate system
)

# Reproject to Web Mercator (required for contextily basemaps)
gdf = gdf.to_crs(epsg=3857)

# Plot with map underlay
fig, ax = plt.subplots(figsize=(10, 8))

# Scatter plot with size proportional to 'total_vehicles'
gdf.plot(
    ax=ax,
    column='Mean GVW',
    cmap='viridis',
    markersize=gdf['Mean GVW'] / gdf['Mean GVW'].max() * 100,  # Scale marker size
    alpha=0.7,
    legend=True
)

# Add basemap from contextily
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# Convert tick labels back to latitude and longitude
def format_ticks_to_wgs84(ax, crs):
    """Convert axis tick labels from Web Mercator to WGS84 (lat/lon)."""
    def to_wgs84(x, y):
        # Create a temporary GeoDataFrame with the Web Mercator coordinates
        temp_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy([x], [y]), crs=crs)
        # Transform to WGS84
        temp_gdf = temp_gdf.to_crs("EPSG:4326")
        # Extract latitude and longitude
        return temp_gdf.geometry.x[0], temp_gdf.geometry.y[0]
    
    # Update X-axis ticks
    xticks = ax.get_xticks()
    xticks_labels = [f"{to_wgs84(tick, ax.get_ylim()[0])[0]:.2f}" for tick in xticks]
    ax.set_xticklabels(xticks_labels)
    
    # Update Y-axis ticks
    yticks = ax.get_yticks()
    yticks_labels = [f"{to_wgs84(ax.get_xlim()[0], tick)[1]:.2f}" for tick in yticks]
    ax.set_yticklabels(yticks_labels)

# Apply formatting
format_ticks_to_wgs84(ax, gdf.crs)

# Customize plot
ax.set_title('Scatterplot of Lat-Long with Mean GVW')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Show plot
plt.savefig('Mean_GVW.jpg')
plt.show()
