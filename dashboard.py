import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium
import json
import pandas as pd

from queries import (
    get_records_by_year,
    get_records_by_institution,
    get_coordinates_validity,
    get_top_species,
    get_valid_coordinates,
    search_species,
    get_species_records,
    get_species_summary,
    get_species_media,
    get_wikipedia_summary
)


st.set_page_config(page_title="Paleo_Vault", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    h1 {
        font-family: 'Playfair Display', serif !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Paleo_Vault")
st.write("An interactive look at fossil occurrence data based on south african fossil records from GBIF.")

df_year = get_records_by_year()
df_institution = get_records_by_institution()
df_coords = get_coordinates_validity()
df_species = get_top_species()

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", "15,070")
col2.metric("Unique Species", "2,793")
col3.metric("Institutions", "42")

st.subheader("Fossil Records by Year")
fig_year = px.bar(
    df_year,
    x="year",
    y="record_count",
    labels={"year": "Year", "record_count": "Number of Records"},
    color_discrete_sequence=["#8b1313"]
)
st.plotly_chart(fig_year, use_container_width=True)

st.subheader("Records by Institution")
fig_institution = px.bar(
    df_institution,
    x="institutioncode",
    y="records_per_institution",
    labels={"institutioncode": "Institution", "records_per_institution": "Number of Records"},
    color_discrete_sequence=["crimson"]
)
st.plotly_chart(fig_institution, use_container_width=True)

st.subheader("Fossil Locations Map")

df_map = get_valid_coordinates()
m = folium.Map(location=[-29.0, 24.0], zoom_start=5)

for _, row in df_map.iterrows():
    folium.CircleMarker(
        location=[row["decimallatitude"], row["decimallongitude"]],
        radius=3,
        popup=row["scientificname"],
        color="#8b1313",
        fill=True
    ).add_to(m)

st_folium(m, width=1200, height=500)

st.subheader("Species Explorer")

search_term = st.text_input(
    "Search for a species (e.g. Australopithecus, Homo, Bovidae)"
)

if search_term:

    species_results = search_species(search_term)

    if len(species_results) == 0:

        st.write("No matching species found.")

    else:

        species_names = species_results["scientificname"].tolist()

        selected_species = st.selectbox(
            "Select a species",
            species_names
        )

        species_records = get_species_records(selected_species)
        species_summary = get_species_summary(selected_species)

        col_img, col_info = st.columns([1, 2])

        with col_img:

            media_results = get_species_media(selected_species)

            image_found = False

            if len(media_results) > 0:

                for _, row in media_results.iterrows():

                    media_list = (
                        row["media"]
                        if isinstance(row["media"], list)
                        else json.loads(row["media"])
                    )

                    for item in media_list:

                        if "identifier" in item:

                            st.image(
                                item["identifier"],
                                width=250
                            )

                            image_found = True
                            break

                    if image_found:
                        break

            if not image_found:
                st.info("No image documented for this specimen yet.")

        with col_info:

            wiki_info = get_wikipedia_summary(selected_species)
        
            if wiki_info and wiki_info["extract"]:
                if wiki_info["thumbnail"]:
                    st.image(wiki_info["thumbnail"], width=250)
                st.write(wiki_info["extract"])
                st.caption("Description and image from Wikipedia (CC BY-SA)")

            st.markdown(f"## {selected_species}")

            record_count = species_summary.iloc[0]['record_count']
            institution_count = species_summary.iloc[0]['institution_count']
            earliest_year = species_summary.iloc[0]['earliest_year']
            latest_year = species_summary.iloc[0]['latest_year']

            st.write(
                f"This specimen has **{record_count}** documented fossil "
                f"record{'s' if record_count != 1 else ''}, held across "
                f"**{institution_count}** institution"
                f"{'s' if institution_count != 1 else ''} in South Africa."
            )

            if pd.notna(earliest_year) and pd.notna(latest_year):
                st.write(
                    f"**Recorded between:** {int(earliest_year)} and {int(latest_year)}"
                )
            else:
                st.write("**Recorded between:** Date not documented")

            st.write("**Country:** South Africa")

        st.markdown("### Occurrence Records")

        st.dataframe(
            species_records[
                [
                    "scientificname",
                    "country",
                    "year",
                    "institutioncode",
                    "collectioncode",
                    "decimallatitude",
                    "decimallongitude"
                ]
            ],
            use_container_width=True
        )

        st.markdown("### Fossil Locations")

        map_records = species_records.dropna(
            subset=["decimallatitude", "decimallongitude"]
        )

        if len(map_records) == 0:

            st.info("No specimen locations have been documented yet for this species.")

        else:

            m_search = folium.Map(
                location=[-29.0, 24.0],
                zoom_start=5
            )

            for _, row in map_records.iterrows():

                folium.CircleMarker(
                    location=[
                        row["decimallatitude"],
                        row["decimallongitude"]
                    ],
                    radius=4,
                    popup=row["scientificname"],
                    color="#8b1313",
                    fill=True
                ).add_to(m_search)

            st_folium(
                m_search,
                width=1200,
                height=500
            )