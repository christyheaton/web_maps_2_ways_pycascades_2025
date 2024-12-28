import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium

def main():
    hikes_gdf = gpd.read_file("https://raw.githubusercontent.com/christyheaton/web_maps_2_ways_pycascades_2025/refs/heads/main/data/hikes_wta_20241219.json")
    hikes_gdf = hikes_gdf[["title", "region", "rating", "mileage", "gain", "geometry"]] 
    st.title("Washington Hikes")
    st_folium(hikes_gdf.explore(), width=700, height=500)


if __name__ == "__main__":
    main()
