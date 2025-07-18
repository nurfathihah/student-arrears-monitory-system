import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load Data
st.set_page_config(page_title="UiTM Student Arrears DSS", layout="wide")
st.title("🎓 UiTM Student Arrears Monitoring System")

uploaded_file = st.file_uploader("📂 Upload the arrears dataset (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Preprocessing
    df['Fines'] = df['Total_Fine'].fillna(0)
    if 'Total_Arrears' not in df.columns:
        df['Total_Arrears'] = df['Total_Fee'] - df['Amount_Paid'] + df['Fines']

    df['Risk_Level'] = pd.cut(
        df['Total_Arrears'],
        bins=[-1, 0, 500, 2000, np.inf],
        labels=['None', 'Low', 'Medium', 'High']
    )

    def fuzzy_priority(row):
        score = 0
        if row['Total_Arrears'] > 5000:
            score += 2
        elif row['Total_Arrears'] > 1000:
            score += 1
        if row['Level'] == 'Master':
            score += 2
        elif row['Level'] == 'Degree':
            score += 1
        if row['Status'] == 'Unpaid':
            score += 2
        elif row['Status'] == 'Partial':
            score += 1
        return 'High' if score >= 4 else 'Medium' if score >= 2 else 'Low'

    df['Fuzzy_Priority'] = df.apply(fuzzy_priority, axis=1)

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Options")
    levels = st.sidebar.multiselect("Filter by Program Level:", options=df['Level'].unique(), default=df['Level'].unique())
    statuses = st.sidebar.multiselect("Filter by Payment Status:", options=df['Status'].unique(), default=df['Status'].unique())
    risk = st.sidebar.multiselect("Filter by Risk Level:", options=df['Risk_Level'].unique(), default=df['Risk_Level'].unique())

    df_filtered = df[
        (df['Level'].isin(levels)) &
        (df['Status'].isin(statuses)) &
        (df['Risk_Level'].isin(risk))
    ]

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total Students", len(df_filtered))
    col2.metric("💸 Avg. Arrears", f"RM {df_filtered['Total_Arrears'].mean():,.2f}")
    col3.metric("⚠️ High Risk Students", df_filtered[df_filtered['Risk_Level'] == 'High'].shape[0])

    st.markdown("---")

    # Charts Section
    st.subheader("📈 Arrears Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Risk Level Distribution**")
        fig1, ax1 = plt.subplots()
        sns.countplot(data=df_filtered, x='Risk_Level', palette='Set2', ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.markdown("**Fuzzy Priority Categories**")
        fig2, ax2 = plt.subplots()
        sns.countplot(data=df_filtered, x='Fuzzy_Priority', palette='mako', ax=ax2)
        st.pyplot(fig2)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Average Arrears by School**")
        fig3, ax3 = plt.subplots(figsize=(10,5))
        sns.barplot(data=df_filtered, x='School', y='Total_Arrears', estimator=np.mean, palette='coolwarm', ax=ax3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    with col4:
        st.markdown("**Payment Status by Program Level**")
        fig4, ax4 = plt.subplots()
        sns.countplot(data=df_filtered, x='Level', hue='Status', palette='pastel', ax=ax4)
        st.pyplot(fig4)

    # Wordcloud for Fine Descriptions
    st.subheader("☁️ Most Frequent Fine Descriptions")
    text = " ".join(df_filtered['Fine_Descriptions'].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    ax5.imshow(wordcloud, interpolation='bilinear')
    ax5.axis("off")
    st.pyplot(fig5)

    # Arrears Table
    st.subheader("📋 Student Arrears Table")
    st.dataframe(df_filtered.sort_values(by="Total_Arrears", ascending=False))

    # Download option
    st.download_button(
        "📥 Download Filtered CSV",
        data=df_filtered.to_csv(index=False).encode('utf-8'),
        file_name="Filtered_Student_Arrears.csv",
        mime="text/csv"
    )
else:
    st.info("Upload your arrears CSV file to begin.")
