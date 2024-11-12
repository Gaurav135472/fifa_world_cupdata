import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
player_data = pd.read_csv('/mnt/data/all_player_info.csv')
fifa_data = pd.read_csv('/mnt/data/Fifa_world_cup3.csv')

# Set up the Streamlit layout
st.set_page_config(page_title="FIFA World Cup Player Stats", layout="wide")

# Sidebar filters
st.sidebar.title("Filters")
countries = player_data['Country'].unique()
selected_country = st.sidebar.selectbox("Select Country", ["All"] + list(countries))

positions = player_data['Position'].unique()
selected_position = st.sidebar.selectbox("Select Position", ["All"] + list(positions))

years = fifa_data['Year'].unique()
selected_year = st.sidebar.selectbox("Select Year", ["All"] + sorted(list(years)))

# Filter data based on selections
filtered_data = player_data.copy()
if selected_country != "All":
    filtered_data = filtered_data[filtered_data['Country'] == selected_country]
if selected_position != "All":
    filtered_data = filtered_data[filtered_data['Position'] == selected_position]
if selected_year != "All":
    fifa_filtered = fifa_data[fifa_data['Year'] == selected_year]
    filtered_data = filtered_data[filtered_data['Player'].isin(fifa_filtered['Player'])]

# Main section
st.title("FIFA World Cup Player Stats")

# Player Profile Display
st.subheader("Player Profiles")
for _, row in filtered_data.iterrows():
    st.image(row['PhotoURL'], width=100)  # Assuming there is a 'PhotoURL' column in your dataset
    st.write(f"**Name**: {row['Player']}")
    st.write(f"**Country**: {row['Country']}")
    st.write(f"**Position**: {row['Position']}")
    st.write(f"**Goals**: {row.get('Goals', 'N/A')}")
    st.write("---")

# Comparison Tool
st.subheader("Player Comparison Tool")
player1 = st.selectbox("Select First Player", player_data['Player'].unique())
player2 = st.selectbox("Select Second Player", player_data['Player'].unique())

# Retrieve stats for the selected players
player1_data = player_data[player_data['Player'] == player1].iloc[0]
player2_data = player_data[player_data['Player'] == player2].iloc[0]

# Display comparison in a table
comparison_df = pd.DataFrame({
    'Stat': ['Goals', 'Assists', 'Matches Played'],  # Add more stats if available
    player1: [player1_data['Goals'], player1_data.get('Assists', 'N/A'), player1_data.get('Matches', 'N/A')],
    player2: [player2_data['Goals'], player2_data.get('Assists', 'N/A'), player2_data.get('Matches', 'N/A')]
})
st.table(comparison_df)

# Visualization Section
st.subheader("Visualize Player Stats")
selected_players = st.multiselect("Select Players for Radar Chart", player_data['Player'].unique())

# Generate Radar Chart if more than one player is selected
if len(selected_players) > 1:
    radar_data = player_data[player_data['Player'].isin(selected_players)]
    stats = ['Goals', 'Assists', 'Matches']  # Select stats for radar chart

    # Normalize data for radar
    radar_data_normalized = radar_data[stats].copy()
    radar_data_normalized = (radar_data_normalized - radar_data_normalized.min()) / (radar_data_normalized.max() - radar_data_normalized.min())

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    angles = [n / float(len(stats)) * 2 * 3.1415 for n in range(len(stats))]
    angles += angles[:1]

    for idx, row in radar_data_normalized.iterrows():
        values = row.tolist()
        values += values[:1]
        ax.plot(angles, values, label=radar_data.loc[idx, 'Player'])
        ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    st.pyplot(fig)

st.write("Explore more filters and options on the sidebar to analyze FIFA World Cup player data.")
