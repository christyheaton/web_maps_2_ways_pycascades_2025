import streamlit as st
import altair as alt
import geopandas as gpd
import folium
from streamlit_folium import st_folium

def main():
    st.title("Let's Find Your Next Washington Hike")
    hikes_gdf = gpd.read_file("../data/hikes_wta_20241219.json")
	
    hikes_gdf["Latitude"] = hikes_gdf.geometry.y
    hikes_gdf["Longitude"] = hikes_gdf.geometry.x

    st.subheader("Filters")

    min_dist = int(hikes_gdf["mileage"].min())
    max_dist = 30
    dist_slider = st.slider("Distance:", min_dist, max_dist, (min_dist, max_dist))

    min_elev = int(hikes_gdf["gain"].min())
    max_elev = 4500
    elev_slider = st.slider("Elevation Gain:", min_elev, max_elev, (min_elev, max_elev))

    pre_selected_region = "All"
    if st.query_params.get("region"):
        pre_selected_region = st.query_params.region

    region = st.selectbox("Region:", [pre_selected_region] + hikes_gdf["region"].tolist())
    if region != pre_selected_region:
        st.query_params.from_dict( { "region": region } )

    # Filtered data
    filtered_df = hikes_gdf[(hikes_gdf["mileage"] >= dist_slider[0]) &
                           (hikes_gdf["mileage"] <= dist_slider[1]) &
                           (hikes_gdf["gain"] >= elev_slider[0]) &
                           (hikes_gdf["gain"] <= elev_slider[1])]
    if region != "All":
        filtered_df = filtered_df[(filtered_df["region"] == region)]

    st.subheader("Hike Table")
    st.dataframe(filtered_df)

    st.subheader("Hike Map")
    st.map(data=filtered_df,
           latitude="Latitude",
           longitude="Longitude")

    # Display the map in Streamlit
    st.subheader("Interactive Hike Map")
    st_folium(filtered_df.explore(), width=700, height=500)

    # Hike ratings chart
    filtered_df["rounded_rating"] = filtered_df["rating"].round()
    rating_counts = filtered_df["rounded_rating"].value_counts().reset_index()
    rating_counts.columns = ["rating", "count"]

    st.subheader("Hike Ratings")

    bar_chart = alt.Chart(rating_counts).mark_bar(color="skyblue").encode(
        x=alt.X("rating:O", title="Rating"),
        y=alt.Y("count:Q", title="Count")
    )
    st.altair_chart(bar_chart, use_container_width=True)
    average_rating = f"{filtered_df['rating'].mean():.1f}"
    st.text(f"Average rating: {average_rating}")

    # Random hike selector
    if not filtered_df.empty:
        if st.button("Select Random Hike"):
            random_row = filtered_df.sample()
            st.subheader("Randomly Selected Hike")
            st.table(random_row.T)
            st.map(data=random_row,
                   latitude="Latitude",
                   longitude="Longitude")

    # Highest rated hike selector
    if not filtered_df.empty:
        if st.button("Select Highest Rated Hike"):
            highest = filtered_df.loc[filtered_df["rating"].idxmax()].to_frame().T
            st.subheader("Highest Rated Hike")
            st.table(highest.T)
            st.map(data=highest,
                   latitude="Latitude",
                   longitude="Longitude")


if __name__ == "__main__":
    main()
