import streamlit as st
import pandas as pd
import preprocessor,helper
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")

st.sidebar.image("logo.png", caption='Olympics')
user_menu = st.sidebar.radio(
    'Select an Optin',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    
    Selected_year = st.sidebar.selectbox("Select Year", years)
    Selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,Selected_year, Selected_country)
    if Selected_year =='Overall' and Selected_country =='Overall':
        st.title("Overall Tally")
    if Selected_year != 'Overall' and Selected_country =='Overall':
        st.title("Medal Tally in " + str(Selected_year) + " Olympics")
    if Selected_year =='Overall' and Selected_country != 'Overall':
        st.title(Selected_country + " overall performance")
    if Selected_year != 'Overall' and Selected_country != 'Overall':
        st.title(Selected_country + " performance in " + str(Selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events =df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)


    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

   
        
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x= 'Edition', y= 'region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x= 'Edition', y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x= 'Edition', y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Event over time (Every Sport)")
    fig,ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax =sns.heatmap(x.pivot_table(index='Sport',columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)

    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successfull(df,selected_sport)
    st.table(x)

    
if user_menu =='Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    Selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df,Selected_country)
    fig = px.line(country_df, x="Year",y="Medal")
    st.title(Selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)


    st.title(Selected_country + " excels in the following sports")
    pt= helper.country_event_heatmap(df,Selected_country)
    fig, ax= plt.subplots(figsize=(25,25))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)  

    st.title("Top 10 athletes of " + Selected_country)
    top10_df = helper.most_successfull_countrywise(df,Selected_country)
    st.table(top10_df)


if user_menu == "Athlete wise Analysis":
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x1  = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    
    fig.update_layout(autosize = False, width= 1000, height= 600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x =[]
    name = []

    famous_sports = ['Basketball','Judo','Football','Tug-of-war','Athletics','Swimming','Badminton','Sailing','Gymnastics','Art Competition','Handball','Weightlifting','Wrestling','Water Polo','Hockey','Rowing','Fencing','Shooting','Boxing','Taekwondo','Cycling','Diving','Canoeing','Tennis','Golf','Softball','Archery','Volleyball','Synchronized Swimming','Table Tennis','BAseball','Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Triathlon','Rugby','Polo','Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[(athlete_df['Sport'] == sport) & (athlete_df['Medal'] == 'Gold')]
        if not temp_df.empty and not temp_df['Age'].dropna().empty:
            x.append(temp_df['Age'].dropna())
            name.append(sport)
    if x:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.show()
    else:
        print("No data to plot.")
    fig.update_layout(autosize = False, width= 1000, height= 600)
    st.title("Distribution of Age according to Sports(Gold Medalist)")
    st.plotly_chart(fig)


    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal',style='Sex',s=100, data=temp_df)
    st.pyplot(fig)



    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male","Female"])
    st.plotly_chart(fig)
