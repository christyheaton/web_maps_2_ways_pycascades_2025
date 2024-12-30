import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium

def main():
    hikes_gdf = gpd.read_file("./data/hikes_wta_20241219.json")

    st.title("Washington Hikes")
    m = hikes_gdf.explore(
        tiles="CartoDB positron",
        marker_kwds = {"radius": 4},
        column="mileage",
        cmap= "copper_r",
        tooltip=["title", "mileage", "gain", "region"]
    )
    st_folium(m, width=800, height=500)


if __name__ == "__main__":
    main()
