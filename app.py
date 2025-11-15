"""import streamlit as st
import pandas as pd
import plotly.express as px

st.title("COVID-19 Data Visualization Dashboard")
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'])
    return df
df = load_data()
st.sidebar.header("Filter Options")
country = st.sidebar.selectbox("Select Country", df['Country'].unique())
metric = st.sidebar.radio("Select Metric", ['Confirmed', 'Recovered', 'Deaths'])
filtered_df = df[df['Country'] == country]
fig = px.line(filtered_df, x='Date', y=metric, title=f"{metric} Cases in {country}")
st.plotly_chart(fig, use_container_width=True)
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Titanic Data Visualization Dashboard")

# Use @st.cache_data to load the data only once
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
    df = pd.read_csv(url)
    # Create a new column with user-friendly labels for 'Survived'
    df['Survived_Status'] = df['survived'].apply(lambda x: 'Survived' if x == 1 else 'Died')
    # Fill missing 'embarked' values with 'Unknown' for filtering
    df['embarked'] = df['embarked'].fillna('Unknown')
    return df

df = load_data()

st.sidebar.header("Filter Options")

# --- New Filters for Titanic Data ---

# Filter 1: Passenger Class (Multiselect)
classes = sorted(df['pclass'].unique())
selected_classes = st.sidebar.multiselect(
    "Select Passenger Class", 
    classes, 
    default=classes
)

# Filter 2: Sex (Multiselect)
sexes = df['sex'].unique()
selected_sexes = st.sidebar.multiselect(
    "Select Sex", 
    sexes, 
    default=sexes
)

# Filter 3: Port of Embarkation (Multiselect)
ports = df['embarked'].unique()
selected_ports = st.sidebar.multiselect(
    "Select Port of Embarkation", 
    ports, 
    default=ports
)

# Apply all filters to the DataFrame
filtered_df = df[
    (df['pclass'].isin(selected_classes)) &
    (df['sex'].isin(selected_sexes)) &
    (df['embarked'].isin(selected_ports))
]

st.header(f"Showing Data for {len(filtered_df)} Passengers")

# --- New Charts for Titanic Data ---

# Chart 1: Survival Counts Bar Chart
st.subheader("Survival Counts")
survival_counts = filtered_df['Survived_Status'].value_counts().reset_index()
survival_counts.columns = ['Status', 'Count']

fig_bar = px.bar(
    survival_counts,
    x='Status',
    y='Count',
    color='Status',
    color_discrete_map={'Survived': 'green', 'Died': 'red'},
    title="Survival Counts for Filtered Passengers"
)
st.plotly_chart(fig_bar, use_container_width=True)


# Chart 2: Age Distribution Histogram
st.subheader("Age Distribution by Survival Status")
fig_hist = px.histogram(
    filtered_df,
    x='age',
    color='Survived_Status', # Show survival split within the histogram
    barmode='overlay', # Overlay the two histograms
    nbins=30,
    color_discrete_map={'Survived': 'green', 'Died': 'red'},
    title="Age Distribution by Survival Status"
)
fig_hist.update_traces(opacity=0.75) # Make it easier to see overlays
st.plotly_chart(fig_hist, use_container_width=True)


# Chart 3: Age vs. Fare Scatter Plot
st.subheader("Age vs. Fare by Survival Status")
fig_scatter = px.scatter(
    filtered_df,
    x='age',
    y='fare',
    color='Survived_Status',
    symbol='sex', # Add another dimension
    hover_data=['pclass', 'name'], # Show useful info on hover
    color_discrete_map={'Survived': 'green', 'Died': 'red'},
    title="Age vs. Fare, Colored by Survival"
)
st.plotly_chart(fig_scatter, use_container_width=True)


# Show the filtered raw data if the checkbox is ticked
if st.checkbox("Show Filtered Raw Data"):
    st.write(filtered_df)
