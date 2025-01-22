import streamlit as st
from streamlit_option_menu  import option_menu 
import plotly_express as px
import mysql.connector
from mysql.connector import connect
import pandas as pd
import json
import requests
import base64
from PIL import Image
import streamlit.components.v1 as components
import os


mydb=mysql.connector.connect(
                             host="127.0.0.1",
                             user="root",
                             password="root",
                             database="Phone_pe_db",
                             port="3306")

cursor=mydb.cursor()

#aggregated insurance

cursor.execute("select * from aggregated_insurance")

table1 =cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1, columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

mydb.commit()


#aggregated transaction

cursor.execute("select * from aggregated_transaction")

table2 =cursor.fetchall()

Aggre_transaction = pd.DataFrame(table2, columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

mydb.commit()

#aggregated user

cursor.execute("select * from aggregated_user")

table3 =cursor.fetchall()

Aggre_user = pd.DataFrame(table3, columns=("States","Years","Quarter","Brands","Transaction_count","percentage"))

mydb.commit()

#map insurance

cursor.execute("select * from map_insurance")

table4 =cursor.fetchall()

map_insurance= pd.DataFrame(table4, columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

mydb.commit()

#map transaction

cursor.execute("select * from map_transaction")

table5 =cursor.fetchall()

map_transaction= pd.DataFrame(table5, columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

mydb.commit()

#map user

cursor.execute("select * from map_user")

table6 =cursor.fetchall()

map_user= pd.DataFrame(table6, columns=("States","Years","Quarter","Districts","RegisteredUsers","AppOpens"))

mydb.commit()

#top insurance

cursor.execute("select * from top_insurance")

table7 =cursor.fetchall()

top_insurance= pd.DataFrame(table7, columns=("States","Years","Quarter","pincodes","Transaction_count","Transaction_amount"))

mydb.commit()

#top transaction

cursor.execute("select * from top_transaction")

table8 =cursor.fetchall()

top_transaction= pd.DataFrame(table8, columns=("States","Years","Quarter","pincodes","Transaction_count","Transaction_amount"))

mydb.commit()

#top user

cursor.execute("select * from top_user")

table9 =cursor.fetchall()

top_user= pd.DataFrame(table9, columns=("States","Years","Quarter","pincodes","RegisteredUsers"))

mydb.commit()

def Transaction_amount_count_Y(df,year):

    tacy = df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()

    tacyg.reset_index(inplace=True) 

    col1,col2 = st.columns(2)

    with col1:

        fig_amount=px.bar(tacyg, x="States",y="Transaction_amount",title=f"TRANSACTION AMOUNT - {year}", color_discrete_sequence=px.colors.sequential.Oranges_r,height=600,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg, x="States",y="Transaction_count",title=f"TRANSACTION COUNT - {year}", color_discrete_sequence=px.colors.sequential.Turbo,height=600,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        data1=json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1 = px.choropleth(tacyg,geojson=data1, locations="States", featureidkey="properties.ST_NM",color="Transaction_amount",color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),hover_name="States", title=f"TRANSACTION AMOUNT - {year}",
                                    fitbounds="locations",height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(tacyg,geojson=data1, locations="States", featureidkey="properties.ST_NM",color="Transaction_count",color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),hover_name="States", title=f"TRANSACTION COUNT - {year}",
                                    fitbounds="locations",height=600,width=600)
        
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy
 
def Transaction_amount_count_Y_Q(df,quarter):

    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True,inplace= True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()

    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:

        fig_amount=px.bar(tacyg, x="States",y="Transaction_amount",title=f"TRANSACTION AMOUNT - Year {tacy["Years"].min()} Quarter {quarter}", color_discrete_sequence=px.colors.sequential.Oranges_r,height=600,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg, x="States",y="Transaction_count",title=f"TRANSACTION COUNT - Year {tacy["Years"].min()} Quarter {quarter}", color_discrete_sequence=px.colors.sequential.Turbo,height=600,width=600)
        st.plotly_chart(fig_count)

    col1,col2 = st.columns(2)

    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

        response = requests.get(url)
        data1=json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1 = px.choropleth(tacyg,geojson=data1, locations="States", featureidkey="properties.ST_NM",color="Transaction_amount",color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),hover_name="States", title=f"TRANSACTION AMOUNT - Year {tacy["Years"].min()} Quarter {quarter}",
                                    fitbounds="locations",height=600,width=600)
        
        fig_india_1.update_geos(visible=False)
        
        st.plotly_chart(fig_india_1)

    with col2:
            
        fig_india_2 = px.choropleth(tacyg,geojson=data1, locations="States", featureidkey="properties.ST_NM",color="Transaction_count",color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),hover_name="States", title=f"TRANSACTION COUNT - Year {tacy["Years"].min()} Quarter {quarter}",
                                    fitbounds="locations",height=600,width=600)
        
        fig_india_2.update_geos(visible=False)
        
        st.plotly_chart(fig_india_2)

    return tacy

def Aggre_tran_transaction_type(df,state):

    tacy = df[df["States"] == state] 
    tacy.reset_index(drop= True,inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg,names= "Transaction_type", values="Transaction_amount", 
                        width=600,height = 600,title= f"TRANSACTION AMOUNT - {state.upper()}", hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg,names= "Transaction_type", values="Transaction_count", 
                        width=600,height = 600,title= f"TRANSACTION COUNT - {state.upper()}", hole=0.5 )
        st.plotly_chart(fig_pie_2)


#Aggregated_user_analysis_1

def Aggre_user_plot_1(df,year):

    aguy= df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg, x="Brands",y="Transaction_count",title = f"BRANDS AND TRANSACTION COUNTS - {year}", 
                       width = 800, height=600, color_discrete_sequence=px.colors.sequential.Peach_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated_user_analysis_2

def Aggre_user_plot2(df,quarter):

    aguyq= df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyqg, x="Brands",y="Transaction_count",title = f"BRANDS AND TRANSACTION COUNT - {quarter} Quarter", width = 800, height=600, color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_bar_1)

    return aguyq

# Aggregated analysis 3

def Aggre_user_plot_3(df,state):
    auyqs = df[df["States"]== state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1 = px.line(auyqs, x="Brands", y="Transaction_count",hover_data="percentage",title=f"BRANDS AND TRANSACTION COUNT - {state.upper()}",width=1000,markers=True)
    st.plotly_chart(fig_line_1)

#Map_Insurance_District

def Map_insur_dist(df,state):

    tacy = df[df["States"] == state] 
    tacy.reset_index(drop= True,inplace= True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1 = px.bar(tacyg, x="Transaction_amount", y="Districts",orientation="h",title=f"DISTRICT TRANSACTION AMOUNT - {state.upper()} STATE",
                        color_discrete_sequence=px.colors.sequential.Purp_r,height=800,width=600)
        fig_bar_1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar(tacyg, x="Transaction_count", y="Districts",orientation="h",title=f"DISTRICT TRANSACTION COUNT - {state.upper()} STATE",
                        color_discrete_sequence=px.colors.sequential.Purp_r,height=800,width=600)
        fig_bar_2.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar_2)

#Map_user_plot_1

def map_user_plot_1(df,year):
    muy= df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)

    muyg=pd.DataFrame(muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum())
    muyg.reset_index(inplace=True)

    fig_line_1 = px.line(muyg, x="States", y=["RegisteredUsers","AppOpens"],title=f"REGISTERED USERS AND APP_OPENS - {year}",height=700,width=1000,markers=True)
    st.plotly_chart(fig_line_1)  

    return muy

#map_user_plot_2

def map_user_plot_2(df,quarter):
    muyq= df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg=pd.DataFrame(muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum())
    muyqg.reset_index(inplace=True)

    fig_line_1 = px.line(muyqg, x="States", y=["RegisteredUsers","AppOpens"],title=f"REGISTERED USERS AND APP_OPENS - YEAR {df['Years'].min()} {quarter} QUARTER",
                         height=700,width=1000,markers=True,color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_line_1)   

    return muyq

#map_user_plot_3

def map_user_plot_3(df,states):
    muyqs= df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)

    col1,col2 = st.columns(2)

    with col1:

        fig_map_user_1 = px.bar(muyqs,x="RegisteredUsers",y="Districts", orientation="h",
                                title=f"REGISTERED USER - {states}",height=800,width=800,color_discrete_sequence=px.colors.sequential.Redor_r)
        st.plotly_chart(fig_map_user_1)
    
    with col2:

        fig_map_user_2 = px.bar(muyqs,x="AppOpens",y="Districts", orientation="h",
                                title=f"USER APPOPENS - {states}",height=800,width=800,color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_map_user_2)

#top_insurance_plot_1

def top_insurance_plot_1(df,state):
    tiy = df[df["States"]== state]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2 = st.columns(2)

    with col1:

        fig_top_insur_1 = px.bar(tiy,x="Quarter",y="Transaction_amount",hover_data="pincodes",
                                    title="TRANSACTION AMOUNT",height=700,width=700,color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(fig_top_insur_1)

    with col2:

        fig_top_insur_2 = px.bar(tiy,x="Quarter",y="Transaction_count",hover_data="pincodes",
                                    title="TRANSACTION COUNT",height=700,width=700,color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_top_insur_2)

def top_user_plot_1(df,year):

    tuy= df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1 = px.bar(tuyg, x="States", y="RegisteredUsers", color="Quarter",width=1000,height=800,
                            color_discrete_sequence=px.colors.sequential.__cached__,hover_name="States",
                            title = f"REGISTERED USERS - {year}")
    st.plotly_chart(fig_top_plot_1)

    return tuy 

#top_user_plot_2
def top_user_plot_2(df,state):

    tuys= df[df["States"]== state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2 = px.bar(tuys, x="Quarter", y="RegisteredUsers",title = "REGISTERED USERS and PINCODE",
                            width=1000, height=800,color="RegisteredUsers",color_discrete_sequence=px.colors.sequential.BuGn_r,
                            hover_data="pincodes", color_continuous_scale=px.colors.sequential.Oryel_r)

    st.plotly_chart(fig_top_plot_2)

def top_chart_transaction_amount(table_name):
    mydb= mysql.connector.connect(host='127.0.0.1',user='root',password='root',database='Phone_pe_db',port=3306)
    cursor=mydb.cursor()

    query1=f'''SELECT States, sum(Transaction_amount) as Top_Transaction_amount 
            FROM {table_name}
            group by States 
            order by Top_Transaction_amount 
            desc limit 10;'''

    cursor.execute(query1)

    table=cursor.fetchall()

    mydb.commit()

    df1=pd.DataFrame(table, columns=("States","Top 10 Transaction Amount"))

    col1,col2=st.columns(2)

    with col1:

        bar1=px.bar(df1, x='States',y='Top 10 Transaction Amount', title = 'TOP PERFORMING STATES',height=800,width=600,color_discrete_sequence=px.colors.sequential.Purples_r)

        st.plotly_chart(bar1)

    query2=f'''SELECT States, sum(Transaction_amount) as Low_Transaction_amount 
            FROM {table_name} 
            group by States 
            order by Low_Transaction_amount 
            limit 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()

    df2=pd.DataFrame(table2, columns=("States","Low Transaction Amounts"))

    with col2:

        bar2=px.bar(df2, x="States", y="Low Transaction Amounts", title = "LOW PERFORMING STATES",height=800, width=600,color_discrete_sequence=px.colors.sequential.OrRd_r)

        st.plotly_chart(bar2)

    query3=f'''SELECT States, round(Avg(Transaction_amount),2) as Average_Transaction_amount 
                FROM {table_name} 
                group by States 
                order by Average_Transaction_amount'''

    cursor.execute(query3)

    table3=cursor.fetchall()

    df3=pd.DataFrame(table3, columns=("States","Low Transaction Amounts"))

    bar3=px.bar(df3, y="States", x="Low Transaction Amounts", title = "AVG PERFORMING STATES ",orientation='h'
                ,height=800,width=1200,color_discrete_sequence=px.colors.sequential.Greens_r)

    st.plotly_chart(bar3)

def top_chart_transaction_count(table_name):
    mydb= mysql.connector.connect(host='127.0.0.1',user='root',password='root',database='Phone_pe_db',port=3306)
    cursor=mydb.cursor()

    query1=f'''SELECT States, sum(Transaction_count) as Top_Transaction_count 
            FROM {table_name}
            group by States 
            order by Top_Transaction_count 
            desc limit 10;'''

    cursor.execute(query1)

    table=cursor.fetchall()

    mydb.commit()

    df1=pd.DataFrame(table, columns=("States","Top 10 Transaction count"))

    col1,col2=st.columns(2)

    with col1:

        bar1=px.bar(df1, x='States',y='Top 10 Transaction count', title ='TOP PERFORMING STATES',height=800,width=600,color_discrete_sequence=px.colors.sequential.Purples_r)

        st.plotly_chart(bar1)

    query2=f'''SELECT States, sum(Transaction_count) as Low_Transaction_count
            FROM {table_name} 
            group by States 
            order by Low_Transaction_count 
            limit 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()

    df2=pd.DataFrame(table2, columns=("States","Low Transaction Counts"))

    with col2:

        bar2=px.bar(df2, x="States", y="Low Transaction Counts", title ="LOW PERFORMING STATES",height=800, width=600,color_discrete_sequence=px.colors.sequential.OrRd_r)

        st.plotly_chart(bar2)

    query3=f'''SELECT States, round(Avg(Transaction_count),2) as Average_Transaction_count 
                FROM {table_name} 
                group by States 
                order by Average_Transaction_count'''

    cursor.execute(query3)

    table3=cursor.fetchall()

    df3=pd.DataFrame(table3, columns=("States","Low Transaction Counts"))

    bar3=px.bar(df3, y="States", x="Low Transaction Counts", title = "AVG PERFORMING STATES",orientation='h'
                ,height=800, width=1000,color_discrete_sequence=px.colors.sequential.Greens_r)

    st.plotly_chart(bar3)


def top_chart_registered_user(table_name,state):
    mydb= mysql.connector.connect(host='127.0.0.1',user='root',password='root',database='Phone_pe_db',port=3306)
    cursor=mydb.cursor()

    query1=f'''select Districts,sum(RegisteredUsers) as RegisteredUsers
                from {table_name} where States = '{state}' group by Districts
                order by RegisteredUsers desc
                limit 10'''

    cursor.execute(query1)

    table=cursor.fetchall()

    mydb.commit()

    df1=pd.DataFrame(table, columns=("Districts","Registered Users"))

    col1,col2 = st.columns(2)

    with col1:

        bar1=px.bar(df1, x='Districts',y='Registered Users', title = 'TOP PERFORMING RegisteredUsers',hover_name='Districts',
                    height=800,width=800,color_discrete_sequence=px.colors.sequential.Purples_r)

        st.plotly_chart(bar1)

    query2=f'''select Districts,sum(RegisteredUsers) as RegisteredUsers
                from {table_name} where States = '{state}' group by Districts
                order by RegisteredUsers
                limit 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()

    df2=pd.DataFrame(table2, columns=("Districts","RegisteredUsers"))

    with col2:

        bar2=px.bar(df2, x="Districts", y="RegisteredUsers", title = "LOW PERFORMING RegisteredUsers",height=800, width=800, hover_name='Districts',
                    color_discrete_sequence=px.colors.sequential.OrRd_r)

        st.plotly_chart(bar2)

    query3=f''' select Districts,avg(RegisteredUsers) as RegisteredUsers
                from {table_name} where States = '{state}' group by Districts
                order by RegisteredUsers;'''

    cursor.execute(query3)

    table3=cursor.fetchall()

    df3=pd.DataFrame(table3, columns=("Districts","RegisteredUsers"))

    bar3=px.bar(df3, y="Districts", x="RegisteredUsers", title = "AVG PERFORMING RegisteredUsers",orientation='h',hover_name="Districts",
                height=800, width=1000,color_discrete_sequence=px.colors.sequential.Greens_r)

    st.plotly_chart(bar3)

def top_chart_App_Opens(table_name,state):
    mydb= mysql.connector.connect(host='127.0.0.1',user='root',password='root',database='Phone_pe_db',port=3306)
    cursor=mydb.cursor()

    query1=f'''select Districts,sum(AppOpens) as AppOpens
                from {table_name} where States = '{state}' group by Districts
                order by AppOpens desc
                limit 10'''

    cursor.execute(query1)

    table=cursor.fetchall()

    mydb.commit()

    df1=pd.DataFrame(table, columns=("Districts","AppOpens"))

    col1,col2 = st.columns(2)
        
    with col1:

        bar1=px.bar(df1, x='Districts',y='AppOpens', title = 'TOP 10 APP_OPENS',hover_name='Districts',
                    height=800,width=800,color_discrete_sequence=px.colors.sequential.Purples_r)

        st.plotly_chart(bar1)

    query2=f'''select Districts,sum(AppOpens) as AppOpens
                from {table_name} where States = '{state}' group by Districts
                order by AppOpens
                limit 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()

    df2=pd.DataFrame(table2, columns=("Districts","AppOpens"))

    with col2:

        bar2=px.bar(df2, x="Districts", y="AppOpens", title = "LAST 10 APP_OPENS",height=800, width=800, hover_name='Districts',
                    color_discrete_sequence=px.colors.sequential.OrRd_r)

        st.plotly_chart(bar2)

    query3=f''' select Districts,avg(AppOpens) as AppOpens
                from {table_name} where States = '{state}' group by Districts
                order by AppOpens;'''

    cursor.execute(query3)

    table3=cursor.fetchall()

    df3=pd.DataFrame(table3, columns=("Districts","AppOpens"))

    bar3=px.bar(df3, y="Districts", x="AppOpens", title = "AVG APP_OPENS",orientation='h',hover_name="Districts",
                height=800, width=1000,color_discrete_sequence=px.colors.sequential.Greens_r)

    st.plotly_chart(bar3)

def top_chart_registered_users(table_name):
    mydb= mysql.connector.connect(host='127.0.0.1',user='root',password='root',database='Phone_pe_db',port=3306)
    cursor=mydb.cursor()

    query1=f'''select States,sum(RegisteredUsers) as RegisteredUsers from {table_name} 
                group by States 
                order by RegisteredUsers desc 
                limit 10;'''

    cursor.execute(query1)

    table=cursor.fetchall()

    mydb.commit()

    df1=pd.DataFrame(table, columns=("States","Registered Users"))

    col1,col2 = st.columns(2)

    with col1:

        bar1=px.bar(df1, x='States',y='Registered Users', title = 'TOP PERFORMING RegisteredUsers',hover_name='States',
                    height=800,width=800,color_discrete_sequence=px.colors.sequential.Purples_r)

        st.plotly_chart(bar1)

    query2=f'''select States,sum(RegisteredUsers) as RegisteredUsers from {table_name} 
                group by States 
                order by RegisteredUsers  
                limit 10;'''

    cursor.execute(query2)

    table2=cursor.fetchall()

    df2=pd.DataFrame(table2, columns=("States","RegisteredUsers"))

    with col2:

        bar2=px.bar(df2, x="States", y="RegisteredUsers", title = "LOW PERFORMING RegisteredUsers",height=800, width=800, hover_name='States',
                    color_discrete_sequence=px.colors.sequential.OrRd_r)

        st.plotly_chart(bar2)

    query3=f''' select States,Avg(RegisteredUsers) as RegisteredUsers from {table_name} 
                group by States 
                order by RegisteredUsers;'''

    cursor.execute(query3)

    table3=cursor.fetchall()

    df3=pd.DataFrame(table3, columns=("States","RegisteredUsers"))

    bar3=px.bar(df3, y="States", x="RegisteredUsers", title = "AVG PERFORMING RegisteredUsers",orientation='h',hover_name="States",
                height=800, width=1000,color_discrete_sequence=px.colors.sequential.Greens_r)

    st.plotly_chart(bar3)





#streamlit part

st.set_page_config(layout="wide")
 
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )

set_background("C:/Users/Mr Yogeshwaran/Videos/24bf315b351f19cb0db7159e8b49b4e8.jpg")

with st.sidebar:

    select = option_menu("Main Menu",["HOME","ABOUT PROJECT","DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
    image1=Image.open("C:/Users/Mr Yogeshwaran/Pictures/download.png")
    col1, col2 = st.columns(2)

    with col1:
        st.image(image1, use_column_width=True)

    with col2:
        st.header("ABOUT:")
        st.markdown("""
        <style>
        .about-text {
            font-size: 18px;
        }
        .about-text p {
            margin: 0 0 10px;
        }
        .about-text strong {
            font-size: 20px;
        }
        </style>
        <div class="about-text">
            <p><strong>PhonePe</strong> is an Indian digital payments and financial services company.</p>
            <p><strong>Headquartered in</strong> Bengaluru, Karnataka, India.</p>
            <p><strong>Founded in</strong> December 2015.</p>
            <p><strong>Founders:</strong></p>
            <ul>
                <li>Sameer Nigam,Rahul Chari,Burzin Engineer</li>
            </ul>
            <p><strong>Interesting Points:</strong></p>
            <ul>
                <li>PhonePe was the first payment app to be built on Unified Payments Interface (UPI).</li>
                <li>It offers services like mobile recharges, utility bill payments, and more.</li>
                <li>PhonePe has over 300 million registered users.</li>
                <li>It has partnerships with over 20 million merchants across India.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif select =="ABOUT PROJECT":
    st.header("DATASET:")
    st.write()


elif select == "DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"] )

    with tab1:

        method=st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method == "Insurance Analysis":

            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)   

            col1,col2 = st.columns(2)

            with col1:
                quarters=st.slider("select the quarters",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(tac_Y,quarters)
                              

        elif method=="Transaction Analysis":
            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years) 

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state", Aggre_tran_tac_Y["States"].unique())  
            Aggre_tran_transaction_type(Aggre_tran_tac_Y,states)
            
            col1,col2 = st.columns(2)

            with col1:
                quarters=st.slider("select the quarters",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state Quat", Aggre_tran_tac_Y_Q["States"].unique())  
            Aggre_tran_transaction_type(Aggre_tran_tac_Y_Q,states)
            

        elif method=="User Analysis":
            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user  ,years) 

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("select the quarters",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot2(Aggre_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state", Aggre_user_Y_Q["States"].unique())  
            Aggre_user_plot_3(Aggre_user_Y_Q,states)


    with tab2:
        method2=st.radio("Select the Method",["Map Insurance","Map Transaction","Map User"])
        
        if method2 == "Map Insurance":
            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year  ",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min())
            Map_insur_tac_Y=Transaction_amount_count_Y(map_insurance,years) 

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state for map", Map_insur_tac_Y["States"].unique())  
            Map_insur_dist(Map_insur_tac_Y,states)

            col1,col2 = st.columns(2)

            with col1:
                quarters=st.slider("select the quarters for map",Map_insur_tac_Y["Quarter"].min(),Map_insur_tac_Y["Quarter"].max(),Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state Quat", Map_insur_tac_Y_Q["States"].unique())  
            Map_insur_dist(Map_insur_tac_Y_Q,states)
            

        elif method2 == "Map Transaction":
            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year  ",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
            Map_tran_tac_Y=Transaction_amount_count_Y(map_transaction,years) 

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state for map", Map_tran_tac_Y["States"].unique())  
            Map_insur_dist(Map_tran_tac_Y,states)

            col1,col2 = st.columns(2)

            with col1:
                quarters=st.slider("select the quarters for map",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state Quat", Map_tran_tac_Y_Q["States"].unique())  
            Map_insur_dist (Map_tran_tac_Y_Q,states)

        elif method2 == "Map User":
            col1,col2=st.columns(2)
            
            with col1:
                years=st.slider("select the year map user ",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
            map_user_Y=map_user_plot_1(map_user,years) 

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("select the quarters map user",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y,quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state map user", map_user_Y_Q["States"].unique())  
            map_user_plot_3(map_user_Y_Q,states)

    with tab3:
        method3=st.radio("Select the Method",["Top Insurance","Top Transaction","Top User"])
        
        if method3 == "Top Insurance":
            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year (Top Insurance) ",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
            top_insur_tac_Y=Transaction_amount_count_Y(top_insurance,years) 

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state (Top Insurance)", top_insur_tac_Y["States"].unique())  
            top_insurance_plot_1(top_insur_tac_Y,states)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("select the quarters (Top Insurance)",top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)

        elif method3 == "Top Transaction":
             
            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year (Top Transaction) ",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
            top_tran_tac_Y=Transaction_amount_count_Y(top_transaction,years) 

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state (Top Transaction)", top_tran_tac_Y["States"].unique())  
            top_insurance_plot_1(top_tran_tac_Y,states)

            col1,col2=st.columns(2)

            with col1:
                quarters=st.slider("select the quarters (Top Transaction)",top_tran_tac_Y["Quarter"].min(),top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y,quarters)
            

        elif method3 == "Top User":

            col1,col2=st.columns(2)

            with col1:
                years=st.slider("select the year (Top user) ",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
            top_user_Y=top_user_plot_1(top_user,years) 

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("select the state (Top user)", top_user_Y["States"].unique())  
            top_user_plot_2(top_user_Y,states)

            

elif select == "TOP CHARTS":

    question= st.selectbox("select the questions",['1.Transaction Amount and Count of Aggregated Insurance',
                                                  '2.Transaction Amount and Count of Map Insurance',
                                                  '3.Transaction Amount and Count of Top Insurance',
                                                  '4.Transaction Amount and Count of Aggregated Transaction',
                                                  '5.Transaction Amount and Count of Map Transaction',
                                                  '6.Transaction Amount and Count of Top transaction',
                                                  '7.Transaction Count of Aggregated User',
                                                  '8.Registered users of Map User',
                                                  '9.App opens of map user',
                                                  '10.Registered users of Top User'])
    
    
    if question == "1.Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2.Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3.Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
    
    elif question == "4.Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5.Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6.Transaction Amount and Count of Top transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7.Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8.Registered users of Map User":

        states=st.selectbox("select the state", map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user",states)

    elif question == "9.App opens of map user":

        states=st.selectbox("select the state", map_user["States"].unique())
        st.subheader("APP_OPENS")
        top_chart_App_Opens("map_user",states)

    elif question == "10.Registered users of Top User":

        st.subheader("Registered users")
        top_chart_registered_users("top_user")





