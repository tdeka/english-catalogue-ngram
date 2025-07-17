import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import string

st.set_page_config(layout="wide")

# Load data and preprocess
@st.cache_data
def load_data():
    df = pd.read_csv("all_titles_by_year.csv")
    df['year'] = df['year'].astype(int)
    df['title'] = df['title'].astype(str).str.lower()
    # Remove punctuation from titles
    df['title'] = df['title'].str.translate(str.maketrans('', '', string.punctuation))
    return df

df = load_data()

# Sidebar input
st.sidebar.title("Search Settings")
search_terms_input = st.sidebar.text_input("Enter words/phrases separated by commas", "poem")
search_terms = [term.strip().lower() for term in search_terms_input.split(",") if term.strip()]
min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Select year range", min_year, max_year, (min_year, max_year))

# Filter data by year
filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Count search terms per year
year_counts = {}
for word in search_terms:
    year_counts[word] = []
    for year in range(year_range[0], year_range[1] + 1):
        titles_this_year = filtered_df[filtered_df["year"] == year]["title"]
        count = titles_this_year.str.contains(word, regex=False).sum()
        year_counts[word].append((year, count))

# Plotting
plt.figure(figsize=(12, 6))
for word, counts in year_counts.items():
    years, counts = zip(*counts)
    plt.plot(years, counts, label=word)
plt.xlabel("Year")
plt.ylabel("Count")
plt.title("Frequency of Terms in Titles Over Time")
plt.legend()
plt.grid(True)
st.pyplot(plt)

# Optional Debug Output
st.subheader("Matching Titles (Sample)")
sample_year = st.sidebar.selectbox("Choose a year to preview matches", list(range(year_range[0], year_range[1] + 1)))
titles_this_year = filtered_df[filtered_df["year"] == sample_year]["title"]

for word in search_terms:
    matching_titles = titles_this_year[titles_this_year.str.contains(word, regex=False)]
    st.markdown(f"**Matches for '{word}' in {sample_year}:**")
    for title in matching_titles.head(10):  # show only first 10 matches for brevity
        st.write(f"– {title}")

