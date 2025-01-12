import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

# Read data as GeoDataFrame
hikes_gdf = gpd.read_file("./data/hikes_wta_20241219.json")

# Add latitude and longitude for Streamlit's st.map
hikes_gdf["Latitude"] = hikes_gdf.geometry.y
hikes_gdf["Longitude"] = hikes_gdf.geometry.x

# Create primary and sub region columns
hikes_gdf[["primary_region", "sub_region"]] = hikes_gdf[
    "region"
].str.split(" > ", expand=True)

# Add title
st.title("Find Your Next Washington Hike")

# Filters
st.sidebar.subheader("Filters")
min_dist = int(hikes_gdf["mileage"].min())
max_dist = 30
dist_slider = st.sidebar.slider(
    "Distance (miles):",
    min_dist,
    max_dist,
    (min_dist, max_dist),
)

min_elev = int(hikes_gdf["gain"].min())
max_elev = 4500
elev_slider = st.sidebar.slider(
    "Elevation Gain (ft):",
    min_elev,
    max_elev,
    (min_elev, max_elev),
)

region_options = ["All"] + list(
    hikes_gdf["primary_region"].dropna().unique()
)
primary_region = st.sidebar.selectbox(
    "Region:", region_options
)

# Filter hikes
filtered_gdf = hikes_gdf[
    (hikes_gdf["mileage"] >= dist_slider[0])
    & (hikes_gdf["mileage"] <= dist_slider[1])
    & (hikes_gdf["gain"] >= elev_slider[0])
    & (hikes_gdf["gain"] <= elev_slider[1])
]

if primary_region != "All":
    filtered_gdf = filtered_gdf[
        filtered_gdf["primary_region"] == primary_region
    ]
    filtered_gdf = filtered_gdf.reset_index(drop=True)

# Geopandas explore map
m = filtered_gdf.explore(
    tiles="CartoDB positron",
    marker_kwds={"radius": 4},
    column="mileage",
    cmap="copper_r",
    tooltip=["title", "mileage", "gain", "region"],
)
st_folium(m, width=800, height=500)