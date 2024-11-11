

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
fifa_data = pd.read_csv('C:\\fifa_world_cupdata\\Fifa_world_cup3.csv')

# Define the header navigation options
st.set_page_config(page_title="FIFA World Cup Dashboard", layout="wide")

# Sidebar filter for Year and Home/Away/Neutral
st.sidebar.header("Filters")
fifa_data["Date"] = pd.to_datetime(fifa_data["Date"], errors='coerce')  # Ensuring correct date parsing
selected_year = st.sidebar.selectbox("Select Year", sorted(fifa_data["Date"].dropna().dt.year.unique()))

# Define the options for Home/Away/Neutral filter
location_filter = st.sidebar.selectbox("Select Match Location", ["All", "Home", "Away", "Neutral"])

# Filter data based on selected year
year_filtered_data = fifa_data[fifa_data["Date"].dt.year == selected_year]

# Apply the Home/Away/Neutral filter
if location_filter == "Home":
    location_filtered_data = year_filtered_data[year_filtered_data["Home_Away_Neutral"] == "Home"]
elif location_filter == "Away":
    location_filtered_data = year_filtered_data[year_filtered_data["Home_Away_Neutral"] == "Away"]
elif location_filter == "Neutral":
    location_filtered_data = year_filtered_data[year_filtered_data["Home_Away_Neutral"] == "Neutral"]
else:
    location_filtered_data = year_filtered_data  # No additional filtering if "All" is selected

# Home Page - Top Teams, Players, and Most Frequent Teams in Stages
st.title("🏆 FIFA World Cup Dashboard - Home")
st.write("Explore top-performing teams, players, and stage-wise statistics based on year and location filters.")

# Top Team Performance with interactive bar chart
st.subheader("Top Team Performances")
home_scores = location_filtered_data.groupby("Home_Team")["Home_Score"].sum()
away_scores = location_filtered_data.groupby("Away_Team")["Away_Score"].sum()
top_teams = (home_scores.add(away_scores, fill_value=0)).nlargest(10)

fig = px.bar(top_teams.reset_index(), x="index", y=0, labels={"index": "Team", "0": "Total Goals"},
             title="Top 10 Teams by Goals Scored")
st.plotly_chart(fig, use_container_width=True)

# Top Players and Goals with pie chart
st.subheader("Top Players and Their Goals")
top_players = location_filtered_data["Player_Name"].value_counts().nlargest(10)
top_players_df = top_players.reset_index()
top_players_df.columns = ['Player', 'Goals']  # Rename columns directly after reset_index

fig = px.pie(top_players_df, names="Player", values="Goals", 
             title="Top 10 Players by Goals", hole=0.3)
st.plotly_chart(fig, use_container_width=True)

# Most Frequent Teams in Final and Quarter-Final Stages with a bar chart
st.subheader("Teams with Frequent Appearances in Final and Quarter-Final Stages")
finals_data = location_filtered_data[location_filtered_data["Tournament_Stage"].isin(["Final", "Quarter-Final"])]
finals_home = finals_data["Home_Team"].value_counts()
finals_away = finals_data["Away_Team"].value_counts()
finals_count = finals_home.add(finals_away, fill_value=0)

# Reset the index and rename columns to match Plotly's requirements
finals_count_df = finals_count.reset_index()
finals_count_df.columns = ['Team', 'Appearances']  # Renaming columns to be more descriptive

fig = px.bar(finals_count_df, x="Team", y="Appearances", 
             title="Teams with Most Appearances in Final & Quarter-Final Stages")
st.plotly_chart(fig, use_container_width=True)


# Define the header navigation options
st.set_page_config(page_title="FIFA World Cup Dashboard", layout="wide")

# Sidebar filter for Year
st.sidebar.header("Filter by Year")
fifa_data["Date"] = pd.to_datetime(fifa_data["Date"], errors='coerce')  # Ensuring correct date parsing
selected_year = st.sidebar.selectbox("Select Year", sorted(fifa_data["Date"].dropna().dt.year.unique()))

# Filter data based on selected year
year_filtered_data = fifa_data[fifa_data["Date"].dt.year == selected_year]

# Home Page - Top Teams, Players, and Most Frequent Teams in Stages
st.title("🏆 FIFA World Cup Dashboard - Home")
st.write("Explore top-performing teams, players, and stage-wise statistics.")

# Top Team Performance with interactive bar chart
st.subheader("Top Team Performances")
home_scores = year_filtered_data.groupby("Home_Team")["Home_Score"].sum()
away_scores = year_filtered_data.groupby("Away_Team")["Away_Score"].sum()
top_teams = (home_scores.add(away_scores, fill_value=0)).nlargest(10)

fig = px.bar(top_teams.reset_index(), x="index", y=0, labels={"index": "Team", "0": "Total Goals"},
             title="Top 10 Teams by Goals Scored")
st.plotly_chart(fig, use_container_width=True)

# Top Players and Goals with pie chart
st.subheader("Top Players and Their Goals")
top_players = year_filtered_data["Player_Name"].value_counts().nlargest(10)
top_players_df = top_players.reset_index()
top_players_df.columns = ['Player', 'Goals']  # Rename columns directly after reset_index

fig = px.pie(top_players_df, names="Player", values="Goals", 
             title="Top 10 Players by Goals", hole=0.3)
st.plotly_chart(fig, use_container_width=True)

# Most Frequent Teams in Final and Quarter-Final Stages with a bar chart
st.subheader("Teams with Frequent Appearances in Final and Quarter-Final Stages")
finals_data = year_filtered_data[year_filtered_data["Tournament_Stage"].isin(["Final", "Quarter-Final"])]
finals_home = finals_data["Home_Team"].value_counts()
finals_away = finals_data["Away_Team"].value_counts()
finals_count = finals_home.add(finals_away, fill_value=0)

# Reset the index and rename columns to match Plotly's requirements
finals_count_df = finals_count.reset_index()
finals_count_df.columns = ['Team', 'Appearances']  # Renaming columns to be more descriptive

fig = px.bar(finals_count_df, x="Team", y="Appearances", 
             title="Teams with Most Appearances in Final & Quarter-Final Stages")
st.plotly_chart(fig, use_container_width=True)
