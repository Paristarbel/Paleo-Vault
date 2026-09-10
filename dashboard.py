import streamlit as st
from queries import get_records_by_year, get_records_by_institution, get_coordinates_validity, get_top_species
import plotly.express as px 
import folium
from streamlit_folium import st_folium
from queries import get_valid_coordinates

st.set_page_config(page_title = "Paleo_Vault", layout = "wide")
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
st.write("An interactive look at  fossil occurrence data based on south african fossil records from GBIF.")

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
x = "year",
y = "record_count",
labels = {"year": "Year" , "record_count" : "Number of Records"},
color_discrete_sequence =["#8b1313"]
)

st.plotly_chart(fig_year , use_container_width = True)

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
st.write(df_map.shape)
st.write(df_map.head())
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

st.subheader("Search by Species")
search_term = st.text_input("Enter a species name (e.g. Australopithecus)")

if search_term:
    filtered = df_map[df_map["scientificname"].str.contains(search_term, case=False, na=False)]
    st.write(f"Found {len(filtered)} matching records")

    m_search = folium.Map(location=[-29.0, 24.0], zoom_start=5)
    for _, row in filtered.iterrows():
        folium.CircleMarker(
            location=[row["decimallatitude"], row["decimallongitude"]],
            radius=4,
            popup=row["scientificname"],
            color="crimson",
            fill=True
        ).add_to(m_search)
    st_folium(m_search, width=1200, height=500)
