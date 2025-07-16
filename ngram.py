import streamlit as st
import pandas as pd
import plotly.graph_objs as go

@st.cache_data
def load_data():
    df = pd.read_csv("all_titles_by_year.csv")
    df['year'] = df['year'].astype(int)
    df['title'] = df['title'].astype(str).str.lower()
    return df

df = load_data()

st.title("English Catalogue Title N-Gram Viewer (1912-1922)")
st.write("Enter one or more words (comma-separated). The plot shows how many times each word appears in titles per year.")

query = st.text_input("Search word(s):")

if query:
    words = [w.strip().lower() for w in query.split(",") if w.strip()]
    years = list(range(1912, 1923))
    
    counts_df = pd.DataFrame({'year': years})
    
    for word in words:
        counts = []
        for year in years:
            titles_this_year = df[df['year'] == year]['title']
            count = titles_this_year.str.contains(rf'\b{word}\b').sum()
            counts.append(count)
        counts_df[word] = counts
    
    # Create interactive plotly figure
    fig = go.Figure()
    
    for word in words:
        fig.add_trace(go.Scatter(
            x=counts_df['year'],
            y=counts_df[word],
            mode='lines+markers',
            name=word,
            hovertemplate='Year: %{x}<br>Count: %{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Word Frequency in English Catalogue Titles (1912-1922)",
        xaxis_title="Year",
        yaxis_title="Number of Titles Containing Word",
        hovermode='x unified',
        template='plotly_white',
        yaxis=dict(range=[0, None])  # This forces the y-axis to start at 0
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Type one or more words above and press enter to see the n-gram visualization.") 
