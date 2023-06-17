import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import pycountry
import openai

# openai.api_key = "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"

df_full = pd.read_csv("df_full_with_predictions.csv")

st.title(f"{st.session_state.country} Investment Gap Analysis")
st.divider()

col1, col2 = st.columns([2, 1])

fig = px.line(df_full[df_full.Country == st.session_state.country], x="Year", y=["Foreign Direct Investment billion USD","Predicted FDI billion USD"], width=900)
# fig.update_xaxes([i for i in range(2000,2020,5)])
fig.update_layout(
    xaxis_range=[2000,2030],
    legend=dict(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="white"
        )
    )
)
col1.plotly_chart(fig)

col2.title('Gap to Actual 2023 %')

st.divider()
st.title("Investment Insights")

c1, c2, c3 = st.columns([1.5, 1, 5])

prompt = c1.selectbox('Prompt', ['Top five reasons to invest', 'Top five industries', 'Key risk factors', 'Outlook'],
                      label_visibility="hidden")
c2.write("#")
c2.write(st.session_state.country)

if prompt != 'Outlook':
    messages = [{"role": "system", "content": "You are a intelligent assistant."},
                {"role": "user",
                 "content": prompt + 'in' + st.session_state.country + 'give short and concise bullet points with small explaination do not give header and footer'}]
else:
    messages = [{"role": "system", "content": "You are a intelligent assistant."},
                {"role": "user",
                 "content": st.session_state.country + 'economic' + prompt + 'give short and concise bullet points with small explaination do not give header and footer'}]

chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", messages=messages
)
reply = chat.choices[0].message.content
st.text_area(label="ChatGPT", value=reply, height=500, key="chatgpt", label_visibility='hidden')  # chatGPT

st.divider()
if st.session_state.country == "USA":
    c_name = "United States"
else:
    c_name = st.session_state.country
country = pycountry.countries.get(name=c_name).alpha_2
url = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey=cbac75915fd14f34a61e925e5881113e"
r = requests.get(url)
r = r.json()
title = ''
articles = r['articles']
for article in articles:
    title += article['title'] + '\n\n'

st.title(f"{st.session_state.country} News Feed")
st.text_area(label="Google News", value=title, height=500, key="google_news", label_visibility='hidden')  # Google News
