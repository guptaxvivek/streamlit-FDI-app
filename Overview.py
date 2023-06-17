import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_plotly_events import plotly_events
from streamlit_extras.switch_page_button import switch_page
import seaborn as sns

st.set_page_config(page_title='Overview',
                   layout='wide',
                   initial_sidebar_state='collapsed')

df = pd.read_csv("df_full_with_predictions.csv")
df_slim = pd.read_csv("df_2021_slim.csv")
df['diff_pred_real_fdi'] = df['Predicted FDI billion USD'] - df['Foreign Direct Investment billion USD']

fdi_diff = df.groupby('Country').mean().sort_values('Average FDI Potential in billion USD (Last 5 Years)',ascending=False)

def jump():
    switch_page('Analysis')


header_left, header_mid, header_right = st.columns(3)

with header_mid:
    st.title('Global FDI flows')

c1, c2 = st.columns([10, 1.5])

slider = c2.select_slider('Normal', ['Map', 'Grid'], label_visibility='hidden')

if slider == 'Map':
    st.header("Global FDI Flows View")
    fig1 = px.choropleth(df, locations='Country', locationmode='country names', color='Average FDI Potential in billion USD (Last 5 Years)',
                         color_continuous_scale='Purples')

    fig1.update_layout(
        autosize=False,
        width=1400,
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-.50,
            xanchor="right",
            x=1
        ),
        paper_bgcolor='rgb(4,12,44)',
        geo=dict(bgcolor='rgb(4,12,44)')
    )

    selected_points = plotly_events(fig1)

    if selected_points:
        a = selected_points[0]
        a = pd.DataFrame.from_dict(a, orient='index')

        st.session_state.country = df.iloc[a[0]['pointIndex']]['Country']
        switch_page('Analysis')

if slider == 'Grid':

    st.header("Investment Potential Ranking")
    st.write("#")
    st.write("#")


    sns.set(rc={'axes.facecolor': '#040c2c', 'figure.facecolor': '#040c2c'})

    col1, col2 = st.columns([1, 2])

    col1.write("Countries ranked based on the difference between predicted and status quo FDI flows.")
    def_val = "Select a Country"
    buttons = list(df_slim.head(25)['Country'])
    buttons.insert(0, def_val)

    selected_button = col1.selectbox("Choose a button", buttons, label_visibility='hidden')
    if selected_button != def_val:
        st.session_state.country = selected_button
        selected_button = def_val
        switch_page('Analysis')

    barchr = plt.figure(figsize=(13, 3))

    fig = sns.barplot(
        y='Country',
        x='Rank',
        data=df_slim.head(5)[::-1],
        palette=['white', 'aqua', 'deepskyblue', 'fuchsia', 'blueviolet']
    )
    fig.set_title(label="Ranking", fontdict={
        'size': 20, 'weight': 'bold', 'color': 'white'})
    fig.set(xlabel='')
    fig.yaxis.label.set_color('white')
    fig.tick_params(axis='x', colors='white')
    fig.tick_params(axis='y', colors='white')
    col2.pyplot(barchr)

st.divider()
c1, space, c2 = st.columns([1, 1, 3])
with c1:
    st.session_state.country = st.selectbox(label='Select The Country',
                                options=df['Country'].unique())

fdi_diff.Country = fdi_diff.index
selected_data = fdi_diff[fdi_diff.Country == st.session_state.country]
with c2:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("FDI (b$)", format(float(selected_data['Foreign Direct Investment billion USD']),".2f"))
    col2.metric("FDI Potential(avg. 5y in b$)", format(float(selected_data['Average FDI Potential in billion USD (Last 5 Years)']),".2f"))
    col3.metric("FDI Potential(avg. 5y in %)", format(float(selected_data['Average FDI Potential in % (Last 5 Years)']),".2f"))
    col4.metric("Rank", int(df_slim[df_slim.Country == st.session_state.country]['Rank']))

    d0, sp = st.columns(2)
    with d0:
        st.write(f"{format(float(selected_data['Gross Domestic Product billions of U.S. dollars']),'.2f')}   GDP (b$)")

    d1, d2 = st.columns(2)
    with d1:
        st.write(f"{format(float(selected_data['Value added by the manufacturing sector as percent of GDP']),'.2f')}    Manufacturing Contribution(% of GDP)")
    with d2:
        st.write(f"{format(float(selected_data['Tax rate percent of commercial profits']),'.2f')}    Commercial Profit Tax (%)")

    d3, d4 = st.columns(2)
    with d3:
        st.write(f"{format(float(selected_data['Value added in the services sector as percent of GDP']),'.2f')}    Services Contribution(% of GDP)")
    with d4:
        st.write(f"{format(float(selected_data['Political stability index (-2.5 weak; 2.5 strong)']),'.2f')} Political Stability(-2.5/2.5)")

    d5, d6 = st.columns(2)
    with d5:
        st.write(f"{format(float(selected_data['Value added in the agricultural sector as percent of GDP']),'.2f')} Agricultral Contribution(% of GDP)")
    with d6:
        st.write(f"{format(float(selected_data['Regulatory quality index (-2.5 weak; 2.5 strong)']),'.2f')} Regulatory Quality(-2.5/2.5)")