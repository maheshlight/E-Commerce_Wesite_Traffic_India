import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="E-commerce Website Traffic India", layout="wide")

st.title("🛒 E-commerce Website Traffic Analysis – India")
st.markdown("**Team 1 Data Science Project** | Analyze website traffic to identify peak visit times, user behavior, and conversion trends.")

# ─────────────────────────────────────────────
# FILE UPLOAD
# ─────────────────────────────────────────────
uploaded_file = st.sidebar.file_uploader("📂 Upload Dataset (.xlsx)", type=["xlsx"])

if uploaded_file is None:
    st.info("👈 Please upload your dataset file from the sidebar to get started.")
    st.stop()

# ─────────────────────────────────────────────
# LOAD & CLEAN DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_and_clean(file):
    df = pd.read_excel(file)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Remove duplicates
    df = df.drop_duplicates()

    # Drop rows where user_id or time is missing
    if 'user_id' in df.columns:
        df = df.dropna(subset=['user_id'])
    if 'time' in df.columns:
        df = df.dropna(subset=['time'])

    # Fill missing numeric with mean
    numeric_cols = df.select_dtypes(include=np.number).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Fill missing categorical with mode
    categorical_cols = df.select_dtypes(include='object').columns
    for col in categorical_cols:
        if df[col].mode().shape[0] > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    # Fix inconsistency
    for col in categorical_cols:
        df[col] = df[col].str.lower().str.strip()

    # Fix negatives
    for col in numeric_cols:
        df[col] = df[col].apply(lambda x: x if x >= 0 else np.nan)
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Fix data types
    if 'page_views' in df.columns:
        df['page_views'] = df['page_views'].astype(int)
    if 'revenue' in df.columns:
        df['revenue'] = df['revenue'].astype(float)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], errors='coerce')
        df['hour'] = df['time'].dt.hour
        df['time_slot'] = pd.cut(
            df['hour'],
            bins=[0, 6, 12, 18, 24],
            labels=['Night', 'Morning', 'Afternoon', 'Evening'],
            right=False
        )
        df['time_slot'] = df['time_slot'].cat.add_categories('Unknown')
        df['time_slot'] = df['time_slot'].fillna('Unknown')

    if 'age' in df.columns:
        df['age_group'] = pd.cut(
            df['age'],
            bins=[0, 18, 25, 35, 45, 60, 100],
            labels=['<18', '18-25', '26-35', '36-45', '46-60', '60+']
        )

    if 'session_duration_sec' in df.columns:
        df['session_minutes'] = df['session_duration_sec'] / 60

    if 'month' in df.columns:
        month_order = ['january', 'february', 'march', 'april', 'may', 'june',
                       'july', 'august', 'september', 'october', 'november', 'december']
        df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)

    return df

df = load_and_clean(uploaded_file)

st.sidebar.success(f"✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🕐 Peak Visit Times",
    "👤 User Behavior",
    "💰 Conversion Trends"
])

# ══════════════════════════════════════════════
# TAB 1 – OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    st.subheader("Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    if 'session_minutes' in df.columns:
        col3.metric("Avg Session (min)", round(df['session_minutes'].mean(), 2))

    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Basic Statistics")
    st.dataframe(df.describe(), use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 – PEAK VISIT TIMES
# ══════════════════════════════════════════════
with tab2:
    st.subheader("Problem Statement 1: Peak Visit Times")

    # a) State-wise visits by time slot
    if 'state' in df.columns and 'time_slot' in df.columns:
        st.markdown("#### a) State-wise Website Visits by Time Slot")
        state_time = df.groupby(['state', 'time_slot'], observed=True).size().reset_index(name='visits')
        pivot_bar = state_time.pivot(index='state', columns='time_slot', values='visits').fillna(0)
        time_order = ['Night', 'Morning', 'Afternoon', 'Evening']
        pivot_bar = pivot_bar.reindex(columns=[c for c in time_order if c in pivot_bar.columns], fill_value=0)

        fig, ax = plt.subplots(figsize=(12, 6))
        pivot_bar.plot(kind='bar', ax=ax)
        ax.set_title('State-wise Website Visits by Time Slot', fontsize=14)
        ax.set_xlabel('States')
        ax.set_ylabel('Number of Visits')
        plt.xticks(rotation=45, ha='right')
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig)

    # b) Age group vs time slot
    if 'age_group' in df.columns and 'time_slot' in df.columns:
        st.markdown("#### b) Age Category Distribution Across Time Slots")
        age_time = df.groupby(['age_group', 'time_slot'], observed=True).size().reset_index(name='visits')
        pivot_age = age_time.pivot(index='age_group', columns='time_slot', values='visits').fillna(0)

        colors = ["#4E79A7", "#A0CBE8", "#F28E2B", "#FFBE7D", "#59A14F", "#8CD17D"]
        fig, ax = plt.subplots(figsize=(12, 5))
        pivot_age.T.plot(kind='bar', ax=ax, color=colors)
        ax.set_title("Age Category Distribution Across Time Slots")
        ax.set_xlabel("Time Slots")
        ax.set_ylabel("Count")
        ax.yaxis.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        st.pyplot(fig)

    # c) City-wise average session time
    if 'city' in df.columns and 'session_minutes' in df.columns:
        st.markdown("#### c) Average Time Spent (Minutes) – City Wise")
        city_avg = df.groupby('city')['session_minutes'].mean().sort_values()
        fig, ax = plt.subplots(figsize=(12, 8))
        city_avg.plot(kind='barh', ax=ax)
        ax.set_title("Average Time Spent (Minutes) – City Wise", fontsize=14)
        ax.set_xlabel("Average Session Minutes")
        plt.tight_layout()
        st.pyplot(fig)

# ══════════════════════════════════════════════
# TAB 3 – USER BEHAVIOR
# ══════════════════════════════════════════════
with tab3:
    st.subheader("Problem Statement 2: User Behavior")

    # Gender donut
    if 'gender' in df.columns:
        st.markdown("#### Gender-wise Traffic Percentage")
        gender_count = df['gender'].value_counts()
        color_map = {'female': '#FFC0CB', 'male': '#ADD8E6', 'trans': '#E6E6FA'}
        colors = [color_map.get(g, '#CCCCCC') for g in gender_count.index]

        fig, ax = plt.subplots(figsize=(7, 7))
        wedges, texts, autotexts = ax.pie(
            gender_count.values,
            labels=gender_count.index,
            autopct='%1.1f%%',
            pctdistance=0.75,
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': 'black', 'width': 0.4},
            textprops={'fontsize': 12}
        )
        ax.text(0, 0, "Genders", ha='center', va='center', fontsize=16, fontweight='bold')
        ax.set_title("Gender-wise Traffic Percentage", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig)

    # Gender heatmap by state
    if 'state' in df.columns and 'gender' in df.columns:
        st.markdown("#### Gender Percentage by State (Heatmap)")
        gender_state = pd.crosstab(df['state'], df['gender'], normalize='index') * 100
        fig, ax = plt.subplots(figsize=(12, 9))
        im = ax.imshow(gender_state.values, cmap='coolwarm', aspect='auto')
        ax.set_xticks(range(len(gender_state.columns)))
        ax.set_xticklabels(gender_state.columns, fontsize=12)
        ax.set_yticks(range(len(gender_state.index)))
        ax.set_yticklabels(gender_state.index, fontsize=10)
        plt.colorbar(im, ax=ax, label="Percentage")
        ax.set_title("Gender Percentage by State", fontsize=14, fontweight='bold')
        ax.grid(False)
        plt.tight_layout()
        st.pyplot(fig)

    # Age vs pages viewed
    if 'age' in df.columns and 'pages_viewed' in df.columns:
        st.markdown("#### Age vs Search Behavior (2D Histogram)")
        fig, ax = plt.subplots(figsize=(10, 6))
        h = ax.hist2d(df['age'], df['pages_viewed'], cmap='coolwarm')
        plt.colorbar(h[3], ax=ax)
        ax.set_xlabel("Age")
        ax.set_ylabel("Pages Viewed")
        ax.set_title("Age vs Search Behavior")
        plt.tight_layout()
        st.pyplot(fig)

# ══════════════════════════════════════════════
# TAB 4 – CONVERSION TRENDS
# ══════════════════════════════════════════════
with tab4:
    st.subheader("Problem Statement 3: Conversion Trends")

    # Conversion funnel
    funnel_cols = [c for c in ['pages_viewed', 'add_to_cart', 'purchase'] if c in df.columns]
    if funnel_cols:
        st.markdown("#### Conversion Funnel")
        conversion = df[funnel_cols].sum()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(conversion.index, conversion.values, marker='o', linewidth=2, markersize=8, color='blue')
        ax.set_xlabel("Stage", fontsize=13)
        ax.set_ylabel("Count", fontsize=13)
        ax.set_title("Conversion Funnel", fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        st.pyplot(fig)

    # Festival sales
    if 'festival' in df.columns and 'purchase' in df.columns:
        st.markdown("#### Festival-wise Sales")
        festival_sales = df.groupby('festival')['purchase'].sum()
        colors = ['#4E79A7', '#A0CBE8', '#F28E2B', '#FFBE7D', '#59A14F', '#8CD17D', '#B6992D', '#499894']
        fig, ax = plt.subplots(figsize=(12, 5))
        festival_sales.plot(kind='bar', color=colors[:len(festival_sales)], edgecolor='black', ax=ax)
        ax.set_xlabel("Festival", fontsize=13)
        ax.set_ylabel("Total Purchases", fontsize=13)
        ax.set_title("Festival-wise Sales", fontsize=14, fontweight='bold')
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    # Monthly sales trend
    products = [c for c in ['home_appliances', 'office_equipments', 'beauty_products', 'clothing', 'technical_devices'] if c in df.columns]
    if 'month' in df.columns and products:
        st.markdown("#### Monthly Sales Trend")
        monthly_sales = df.groupby('month')[products].sum()
        fig, ax = plt.subplots(figsize=(12, 5))
        monthly_sales.sum(axis=1).plot(kind='bar', color='skyblue', edgecolor='black', ax=ax)
        ax.set_xlabel("Month", fontsize=13)
        ax.set_ylabel("Total Sales", fontsize=13)
        ax.set_title("Monthly Sales Trend", fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("#### Total Products Sold")
        total_sold = df[products].sum()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(total_sold.index, total_sold.values)
        ax.set_xlabel("Product Type", fontsize=13)
        ax.set_ylabel("Units Sold", fontsize=13)
        ax.set_title("Total Products Sold", fontsize=14)
        plt.xticks(rotation=30)
        plt.tight_layout()
        st.pyplot(fig)

    # Purchasing capacity boxplot
    if 'state' in df.columns and 'order_value' in df.columns:
        st.markdown("#### User Purchasing Capacity – Top States (Boxplot)")
        top_states = df.groupby('state')['order_value'].sum().sort_values(ascending=False).head(8).index
        df_top = df[df['state'].isin(top_states)]
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.boxplot(
            [df_top[df_top['state'] == s]['order_value'] for s in top_states],
            labels=top_states
        )
        plt.xticks(rotation=30)
        ax.set_ylabel("Order Value per Transaction")
        ax.set_title("User Purchasing Capacity Distribution (Top States)")
        plt.tight_layout()
        st.pyplot(fig)
