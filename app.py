import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import warnings
warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")

st.title("Unicorn Companies across the Globe.")
st.warning("A unicorn company, or unicorn startup, is a private company with a valuation over $1 billion. As of June 2021, there are more than 700 unicorns around the world. Popular former unicorns include Airbnb, Facebook and Google. Variants include a decacorn, valued at over $10 billion, and a hectocorn, valued at over $100 billion.")

#Dataset
df=pd.read_csv("700_unicorn.csv")
df["Date Joined"]=pd.DatetimeIndex(df["Date Joined"])

#globe
st.header("Countries with Unicorn Companies")
dfx=df[['latitude', 'longitude']]
st.map(dfx,zoom=1.2,use_container_width=False)

#country-valuation
st.header("Total Valuation per Country")
st.write("Total valuation of unicorns for each country till date (June 2021)")
st.bar_chart(df.groupby(['Country of origin'])['Valuation (in $B)'].sum())

#line chart
# st.header("Companies with their Valuation")
# val_com=df[["Company name","Valuation (in $B)"]]
# val_com.set_index("Company name",inplace=True)
# st.line_chart(val_com,width=10000,use_container_width=False)
# x=df[["Company name"]]
# y=df[["Valuation (in $B)"]]
# p = figure(x_axis_label="Company",y_axis_label="Valuation (in $B)")
# p.line(x, y, legend_label='Trend', line_width=2)
# st.bokeh_chart(p, use_container_width=True)

#top valuation per year
st.header("Top Unicorn Companies with Valuation % ")
st.write("See the top unicorn companies and their percentage valuation per year, when they joined.")
l,r=st.beta_columns(2)
dropdown=l.multiselect("Select Year(s)",df.sort_values("Date Joined")["Date Joined"].dt.year.unique())
num=r.slider("Top N",min_value=1, max_value=100, value=10, step=1)
if len(dropdown)>0:
  col=st.beta_columns(len(dropdown))
  for i in range(len(dropdown)):
    dc=df[df["Date Joined"].dt.year==dropdown[i]].sort_values("Valuation (in $B)")[-num:][["Company name","Valuation (in $B)"]]
    # dc.set_index("Company name",inplace=True)
    st.subheader(dropdown[i])
    st.text("Valuation (in $B)")
    # col[i].bar_chart(dc)
    fig = go.Figure(data=[go.Pie(labels=dc["Company name"], values=dc["Valuation (in $B)"], hole=.5,name='Valuation (in $B)')])
    st.plotly_chart(fig)


#select counrty and time period
st.sidebar.header("Search for Unicorns Companies ")
country_list=df.sort_values("Country of origin")["Country of origin"].unique()

st.sidebar.subheader("Select Country")
country=st.sidebar.selectbox("Country",country_list)

st.sidebar.subheader("Select Time-Period")
start=pd.to_datetime(st.sidebar.date_input("From",value=pd.to_datetime("2007-07-20")))
end=pd.to_datetime(st.sidebar.date_input("To",value=pd.to_datetime(df["Date Joined"]).max()))
st.sidebar.write('**NOTE**: Date refers when the company became a Unicorn.')
st.sidebar.info("The data keeps on updating after every month.")

#country map
st.header("Country Map")
st.write("Cities with Unicorn Companies in "+country+".")
df_date=df[(df["Date Joined"]<end) & (df["Date Joined"]>start)].sort_values("Date Joined")
df_city=df_date[df_date["Country of origin"]==country]
dfx=df_city[['lat', 'lon']]
st.map(dfx,zoom=4,use_container_width=False)
with st.beta_expander("See Cities"):
  st.write(
  (df_city["City"].unique())
      )
# st.write(df_city)

st.header("Unicorn Companies in "+country)
dtc=df[df["Country of origin"]==country][["Company name", "Valuation (in $B)"]].sort_values("Valuation (in $B)")
dtc.reset_index(drop=True,inplace=True)
with st.beta_expander("List of all Unicorn Companies till date."):
  st.table(dtc)

      

st.header("Total Valuation by Cities")
st.write("Total valuation by the cities listed above in the selected time period.")
st.bar_chart(df_city.groupby(['City'])['Valuation (in $B)'].sum())

st.header("Total Valuation by the Industries of "+country)
st.write("Total valuation of different Industries in the cities of "+country+" in the selected time period.")
vb=(df_city.groupby(['Industry'])['Valuation (in $B)'].sum()).reset_index()
fig = px.pie(vb, values='Valuation (in $B)', names='Industry',color_discrete_sequence=px.colors.sequential.Aggrnyl)
st.plotly_chart(fig,use_container_width=True)

st.header("Valuation of Unicorn Companies ")
st.write("Valuation of Unicorn Companies in the listed city in the selected time period. ( Mouseover the points to see the company name.)")
city=df_city["City"].unique()
# if(len(city)>0):
#   col=st.beta_columns(len(city))
#   for i in range(len(city)):
#     dc=df_city[df_city["City"]==city[i]][["Company name","Valuation (in $B)"]]
#     dc.set_index("Company name",inplace=True)
#     col[i].subheader(city[i])
#     col[i].bar_chart(dc)
dct=df_city[df_city["City"].isin(city)][["City","Valuation (in $B)","Company name","Date Joined"]]
fig = px.scatter(dct, x='Valuation (in $B)', y='City',color_discrete_sequence=px.colors.sequential.RdBu, hover_data=['Company name'])
st.plotly_chart(fig,use_container_width=True)

st.header("Company Details")
st.write("Details of the Unicorn Companies in "+country+" in the selected time period.")
dcx=df_city[["Company name","Valuation (in $B)","Industry"]]
dcx.reset_index(drop=True, inplace=True)
l,r=st.beta_columns(2)
drop=r.multiselect("Select Industry(s)",dcx["Industry"].unique())
rad=l.radio("Sort by Valuation (Ascending/Descending)",["asce","desc"])
if (rad=="asce"):
  dcx.sort_values("Valuation (in $B)",ascending=True,inplace=True)
  if (len(drop)>0):
    dx=dcx[dcx["Industry"].isin(drop)]
    st.table(dx)
  else: 
    st.table(dcx)
if (rad=="desc"):
  dcx.sort_values("Valuation (in $B)",ascending=False,inplace=True)
  if (len(drop)>0):
    dx=dcx[dcx["Industry"].isin(drop)]
    st.table(dx)
  else:
    st.table(dcx)

st.header("Investors")
st.write("See the Investors of the above mentioned companies.")
# people=st.selectbox("Select Company(s)",dcx["Company name"])
# if(len(people)>0):
#   for i in range(len(com)):
inv=df_city[["Company name","Investors"]]
# inv=df_city[df_city["Company name"]==people]
inv.reset_index(drop=True, inplace=True)
st.table(inv)

st.header("SUMMARY")
st.subheader("Select the name of the company to know its details.")
company_list=df.sort_values("Company name")["Company name"].unique()
company=st.selectbox("Company",company_list)
detail=df[df["Company name"]==company]
map_=detail[["latitude","longitude"]]
map_.loc[len(map_.index)] = detail[["lat","lon"]].values[0]
l,r=st.beta_columns((1,1.2))
l.subheader("Origin")
l.map(map_,zoom=3,use_container_width=True)

fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = detail[["Valuation (in $B)"]].values[0][0],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Valuation (in $B)"}))
det=detail[["Date Joined","Investors","Industry"]]
r.subheader("Details")
det.reset_index(drop=True,inplace=True)
fmt = "%d-%m-%Y"
styler = det.style.format(
    {
        "Date Joined": lambda t: t.strftime(fmt),
        # "b": lambda t: datetime.fromtimestamp(t).strftime(fmt),
    }
)
r.table(styler)
r.plotly_chart(fig,use_container_width=True,height=50)


  








