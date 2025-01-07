import streamlit as st
import altair as alt
import geopandas as gpd
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
filtered_df = hikes_gdf[
    (hikes_gdf["mileage"] >= dist_slider[0])
    & (hikes_gdf["mileage"] <= dist_slider[1])
    & (hikes_gdf["gain"] >= elev_slider[0])
    & (hikes_gdf["gain"] <= elev_slider[1])
]

if primary_region != "All":
    filtered_df = filtered_df[
        filtered_df["primary_region"] == primary_region
    ]
    filtered_df = filtered_df.reset_index(drop=True)

# Display filtered hikes as a table
st.subheader("Hike Table")
st.dataframe(
    filtered_df[
        [
            "title",
            "region",
            "rating",
            "mileage",
            "gain",
            "geometry",
        ]
    ]
)

# Streamlit map
st.subheader("Streamlit Map")
st.map(
    data=filtered_df,
    latitude="Latitude",
    longitude="Longitude",
)

# Geopandas explore map
st.subheader("st_folium GeoPandas Map")
m = filtered_df.explore(
    tiles="CartoDB positron",
    marker_kwds={"radius": 4},
    column="mileage",
    cmap="copper_r",
    tooltip=["title", "mileage", "gain", "region"],
)
st_folium(m, width=800, height=500)

# Hike ratings chart
filtered_df["rounded_rating"] = filtered_df[
    "rating"
].round()
rating_counts = (
    filtered_df["rounded_rating"]
    .value_counts()
    .reset_index()
)
rating_counts.columns = ["rating", "count"]

st.subheader("Hike Ratings")
bar_chart = (
    alt.Chart(rating_counts)
    .mark_bar(color="skyblue")
    .encode(
        x=alt.X("rating:O", title="Rating"),
        y=alt.Y("count:Q", title="Count"),
    )
)
st.altair_chart(bar_chart, use_container_width=True)
average_rating = f"{filtered_df['rating'].mean():.1f}"
st.text(f"Average rating: {average_rating}")

# Highest-rated hike selector
if not filtered_df.empty:
    if st.button("Select Highest Rated Hike"):
        highest = (
            filtered_df.loc[filtered_df["rating"].idxmax()]
            .to_frame()
            .T
        )
        st.subheader("Highest Rated Hike")
        st.table(
            highest[
                [
                    "title",
                    "description",
                    "mileage",
                    "gain",
                    "region",
                    "passes",
                    "rating",
                    "url",
                    "Latitude",
                    "Longitude",
                ]
            ].T
        )
        st.map(
            data=highest,
            latitude="Latitude",
            longitude="Longitude",
        )
