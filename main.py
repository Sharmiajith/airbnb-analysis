import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time

# Multi page initialization
import home,explore,geo,visual

st.set_page_config(page_title='Airbnb Analysis using Streamlit and Plotly')
# Initialize a class
class Multiapp:
    def __init__(self):
        self.apps = []
    def add_app(self,title,function):
        self.apps.append({
            "title":title,
            "function":function
        })

    def run():
# Inputs for Side bar option 
        with st.sidebar:
            app = option_menu(
            menu_title='Airbnb',
            options=["Home", "Explore_Airbnb", "Geovisualization", "Data_analization"],
            menu_icon='building',  # A general icon for Airbnb menu
            icons=['house-door', 'search', 'map', 'bar-chart'],
            default_index=0  # Start with the "Home" tab selected
    )
            
    # Function call for use other pages
        if app=='Home':
            home.app()
        elif app=='Explore_Airbnb':
            explore.app()
        elif app=='Geovisualization':
            geo.app()
        elif app=='Data_analization':
            visual.app()

    run()
    
    def app():
        st.title(":blue[Airbnb Analysis Using Streamit and Plotly]")
        col2,col1=st.columns([2,1])
        with col2:
            st.write("""
        ### :green[About Airbnb:]
        Airbnb is an online marketplace that connects travelers with local hosts who offer unique accommodations and experiences. Founded in 2008, Airbnb has grown into a global platform with millions of listings in over 220 countries and regions.
        """)
            st.write("""
        ### :green[Key Features of Airbnb:]
        - **Accommodations**: Airbnb offers a wide range of accommodations, including apartments, houses, villas, and unique properties like treehouses and yurts.
        - **Experiences**: In addition to lodging, Airbnb hosts can offer experiences such as guided tours, cooking classes, and outdoor adventures.
        - **Host Program**: Individuals can become Airbnb hosts by listing their properties or experiences on the platform, allowing them to earn income and connect with travelers.
        - **Reviews and Ratings**: Airbnb incorporates a review system where guests and hosts can leave feedback, helping to build trust and transparency within the community.
        """)

        st.write("""
        ### :green[About the Dataset:]
        You have Airbnb 2018 data, which includes information about listings, hosts, reviews, and other relevant details. This dataset can provide insights into the types of accommodations available, pricing trends, and popular destinations during the year 2018.
        """)
        with col1:
            st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2JocjltNzB4ZHhncGo3MHZ6Yms4cjNzOXNvamU0dG40cW9oaWJ4ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/J1LEDZftGWZrQNrCr5/giphy.gif")


mydb = mysql.connector.connect(host="localhost",user="root",password="")
mycursor = mydb.cursor(buffered=True,)

#create a engine to insert data value
engine = create_engine("mysql+mysqlconnector://root:@localhost/airbnb") 
def app():
 

    #create database and use for table creation
    mycursor.execute('create database if not exists airbnb')
    mycursor.execute('use airbnb')
    icon='https://avatars.githubusercontent.com/u/698437?s=280&v=4'
    st.title(':blue[Airbnb]')
    col1,col2=st.columns([2,1])

    with col2:
            st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnY5bXJ4ZTV3NW1ndWVmNHQzZm5vaDNhZzRpN2tuYm1weGptaTFiZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/geSnRnLiLYKUbQ8ODK/giphy.gif",use_column_width=True)

    with col1:
        st.write(' ')
        st.subheader(':blue[Welcome to the Airbnb Explorer!]')
        st.markdown(':orange[Embark on Your Journey with us]')
        df_Country=pd.read_sql_query('''SELECT DISTINCT Country from airbnb.hotels_info''',con=engine)
        selected_country= st.selectbox("Search destinations",options=df_Country['Country'].tolist(),index=None)
        st.write(' ')

        df_street=pd.read_sql_query('''SELECT DISTINCT Street from airbnb.hotels_info WHERE country =%s''',
                                    con=engine,params=[(selected_country,)])
        selected_street= st.selectbox("Select Street",options=df_street['Street'].tolist(),index=None)
        st.write(' ')

        df_hotels=pd.read_sql_query('''SELECT DISTINCT Name from airbnb.hotels_info WHERE street =%s''',
                                    con=engine,params=[(selected_street,)])
        selected_Hotel=st.selectbox('Select Hotel',options=df_hotels['Name'].tolist(),index=None)


        st.write("Selected Accommodation:", f"<span style='color:#F8CD47'>{selected_Hotel}</span>", unsafe_allow_html=True)

    if selected_Hotel:
            more=st.button('Click for Details')

                
            df=pd.read_sql_query('''SELECT Name,Listing_url,Description,Country,Price,Images,Property_Type,Room_Type,Amenities,
                                            Host_Name,Host_about,Host_location,Overall_score,Rating,Number_of_review
                                            from hotels_info
                                            join rooms_info on hotels_info.id=rooms_info.id
                                            JOIN hosts_info on hotels_info.id = hosts_info.id
                                            join reviews_info on hotels_info.id = reviews_info.id
                                            where Name= %s ''',con=engine,params=[(selected_Hotel,)])
                    
            extract_detail = df.to_dict(orient='records')[0] 

            c1,c2=st.columns(2)
            with c1:
                        st.write('**:green[Basic Details]**')
                        st.write("**:violet[Name :]**", f'**{extract_detail['Name']}**')
                        st.write("**:violet[Website Url :]**",extract_detail['Listing_url'])
                        st.write("**:violet[country :]**",f'**{extract_detail['Country']}**')
                        st.write("**:violet[Description :]**",f'**{extract_detail['Description']}**')
                        st.write("**:violet[Price in $ :]**",f'**{extract_detail['Price']}**')
                        st.write("**:violet[Total Reviews :]**",f'**{extract_detail['Number_of_review']}**')
                        st.write("**:violet[Overall Score:]**", f"**{extract_detail['Overall_score']} &nbsp;&nbsp;&nbsp; **:violet[Rating:]** {extract_detail['Rating']}**")
                        st.write("**:violet[Room Picture :]**")
                        st.image(extract_detail['Images'],width=300)

            with c2:
                        st.write('**:green[Room Details]**')
                        st.write("**:violet[Property Type :]**",f'**{extract_detail['Property_Type']}**')
                        st.write("**:violet[Room Type :]**",f'**{extract_detail['Room_Type']}**')
                        st.write("**:violet[Amenities :]**",f'**{extract_detail['Amenities']}**')
                        st.write('**:green[Host Details]**')
                        st.write("**:violet[Host Name :]**",f'**{extract_detail['Host_Name']}**')
                        st.write("**:violet[Host location :]**",f'**{extract_detail['Host_location']}**')
                        st.write("**:violet[Host About :]**",f'**{extract_detail['Host_about']}**')
                       
 
    def app():
        mydb = mysql.connector.connect(host="localhost",user="root",password="")
        mycursor = mydb.cursor(buffered=True,)

    #create a engine to insert data value
    engine = create_engine("mysql+mysqlconnector://root:@localhost/airbnb") 

    #create database and use for table creation
    mycursor.execute('create database if not exists airbnb')
    mycursor.execute('use airbnb')

    st.subheader(":red[Explore Accommodation by Country]")

    df_Country=pd.read_sql_query('''SELECT DISTINCT Country from hotels_info''',con=engine)
    selected_country= st.selectbox("select Country",options=df_Country['Country'].tolist(),index=None)

    if selected_country:
        on=st.toggle('switch to view')

        if on:
            
            df=pd.read_sql_query('''  SELECT Name as 'HotelName', Longitude, Latitude  FROM hotels_info
                                where Country = %s  ''',con=engine,params=[(selected_country,)])
            
            df[['Longitude','Latitude']]=df[['Longitude','Latitude']].astype('float')
            
            fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",
                                    zoom=10,hover_name='HotelName',
                                    color_discrete_sequence=px.colors.colorbrewer.Blues_r)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig,use_container_width=True)

mydb = mysql.connector.connect(host="localhost",user="root",password="")
mycursor = mydb.cursor(buffered=True,)

#create a engine to insert data value
engine = create_engine("mysql+mysqlconnector://root:@localhost/airbnb") 

#create database and use for table creation
mycursor.execute('create database if not exists airbnb')
mycursor.execute('use airbnb')
def app():
    with st.sidebar:
        selected_insight = option_menu(
            "Insights",
            ["Average Price", "Number of Review","General Analysis"],
            icons=["currency-dollar", "star","bar-chart"],
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#002b36"},
                "icon": {"color": "#F8CD47", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#FF69B4"},
                "nav-link-selected": {"background-color": "#FF69B4"}
            }
        )

    if selected_insight=="Average Price":

        df_Country=pd.read_sql_query('''SELECT DISTINCT Country from hotels_info''',con=engine)
        selected_country= st.selectbox("select Country",options=df_Country['Country'].tolist(),index=None)

        if selected_country:
            on=st.toggle('switch to view')

            if on:
                
                    df=pd.read_sql_query('''  SELECT Name as 'HotelName',Avg(price) as Average_price FROM hotels_info \
                                        where Country = %s \
                                        Group BY HotelName \
                                        ORDER BY Average_price DESC ''',con=engine,params=[(selected_country,)])
                    
                    fig = px.scatter(df, 
                            x='HotelName', 
                            y='Average_price', 
                            title=f'Average Prices of Hotels in {selected_country}',
                            labels={'HotelName': 'Hotel Name', 'Average_price': 'Average Price'},
                            height=600)

                # Display the chart using Streamlit
                    st.plotly_chart(fig)

                    st.dataframe(df[['HotelName', 'Average_price']])

                    fig = px.sunburst(df,
                                path=['Average_price', 'HotelName'],
                                values='Average_price',
                                title=f'Average Prices of Hotels in {selected_country}',
                                labels={'Country': 'Country', 'HotelName': 'Hotel Name', 'Average_price': 'Average Price'},
                                height=600)

                # Display the chart using Streamlit
                    st.plotly_chart(fig)
                
                    



    if selected_insight=="Number of Review":

        
        df_Country=pd.read_sql_query('''SELECT DISTINCT Country from hotels_info''',con=engine)
        selected_country= st.selectbox("select Country",options=df_Country['Country'].tolist(),index=None)
        if selected_country:
            on=st.toggle('switch to view')

            if on:
                df=pd.read_sql_query('''  SELECT r.Number_of_review,h.Country,h.Name FROM airbnb.reviews_info r \
                                    JOIN hotels_info h ON r.id=h.id \
                                    where Country = %s \
                                    Group BY Name \
                                    ORDER BY Number_of_review DESC ''',con=engine,params=[(selected_country,)])
                fig = px.bar(df, x='Name', y='Number_of_review', color='Number_of_review', 
                        title=f'Number of Reviews for Hotels in {selected_country}',
                        labels={'Name': 'Hotel Name', 'Number_of_review': 'Number of Reviews'},
                        height=1000)
                st.plotly_chart(fig)
                st.write("Hotel Review Details")
                st.dataframe(df[['Name', 'Number_of_review']])

                
    if selected_insight=="General Analysis":


        query=st.selectbox(":violet[Select Your Query]",("Select the Query","Top 10 Hotels With Maximum Price",
                                                        "Top 10 Hotels with Minimum Price","Number of Hotels by Country",
                                                        "Average Price of Rooms by Country","Average Price of Room Types",
                                                        "Count of Room Types by Country","Average Monthly Price",
                                                        "Average Weekly Price","Maximum Security Deposit",
                                                        "Minimum Security Deposit"))
       
        
        if query=="Select the Query":
            st.write("Your are getting the View about airbnb Analysis ")

        elif query=="Top 10 Hotels With Maximum Price":
            # Execute SQL query to fetch data
            query_top_hotels = "SELECT Name, Country, MAX(Price) as price FROM airbnb.hotels_info GROUP BY Name ORDER BY price DESC LIMIT 10"
            top_hotels_df = pd.read_sql_query(query_top_hotels, engine)

            # Create bar plot for top hotels
            fig_bar = go.Figure(data=[go.Bar(x=top_hotels_df['Name'], y=top_hotels_df['price'], text=top_hotels_df['Country'], textposition='auto')])
            fig_bar.update_layout(title='Top 10 Hotels with Maximum Prices',
                                xaxis_title='Hotel Name',
                                yaxis_title='Maximum Price',
                                template='plotly_white')
            st.plotly_chart(fig_bar)
            st.write('''Istanbul, Turkey:Hotel Name: "Center of Istanbul Sisli"
                     Location: Sisli District Minimum Price: 48,842 Turkish Lira 
                     Insight: This hotel is the most expensive in the dataset, reflecting its prime location in Istanbul's vibrant Sisli district, known for its shopping and cultural attractions.''')
            st.write('''Brazil:
                Hotel Names: "Apartamento de luxo em Copacabana - 4 quartos", "Deslumbrante apartamento na AV.Atlantica"
                Location: Copacabana, Avenida Atlantica
                Minimum Price: Exceeding 6,000 Brazilian Reais
                Insight: These luxurious accommodations cater to travelers seeking premium experiences along Brazil's picturesque coastlines, particularly in the iconic Copacabana area.''')
            

            st.dataframe(top_hotels_df)

            # Calculate total maximum price for each country
            query_total_prices = "SELECT Country, SUM(Price) as total_price FROM airbnb.hotels_info GROUP BY Country"
            total_prices_df = pd.read_sql_query(query_total_prices, engine)

            # Create pie chart for total maximum prices by country
            fig_pie = px.pie(total_prices_df, values='total_price', names='Country', title='Pie Chart of Total Maximum Prices by Country')
            st.plotly_chart(fig_pie)
            
        elif query=="Top 10 Hotels with Minimum Price":
            # Execute SQL query to fetch data
            query_top_hotels = "SELECT Name, Country, MIN(Price) as price FROM airbnb.hotels_info GROUP BY Name ORDER BY price ASC LIMIT 10"
            top_hotels_df = pd.read_sql_query(query_top_hotels, engine)

            # Display the top hotels data
            st.write("Top 10 Hotels with Minimum Prices")
            

            # Create bar plot for top hotels
            fig_bar = go.Figure(data=[go.Bar(x=top_hotels_df['Name'], y=top_hotels_df['price'], text=top_hotels_df['Country'], textposition='auto')])
            fig_bar.update_layout(title='Top 10 Hotels with Minimum Prices',
                                xaxis_title='Hotel Name',
                                yaxis_title='Minimum Price',
                                template='plotly_white')
            st.plotly_chart(fig_bar)
            st.write('''A hotel from Portugal Economy INN give the lowest price 50 currency we get insights This hotel offers the lowest price among the top 10, 
                making it an attractive option for budget travelers. Its central location adds to its appeal, providing easy access to the city’s main attractions.''')
            st.write('''Secondly a hotel name Budget stay INN which offers 55 currency the Insight: Situated in the suburbs, this hotel provides affordable accommodation slightly away from the hustle and bustle of the city center. Ideal for travelers looking for a peaceful stay at a lower cost. ''')

            st.dataframe(top_hotels_df)

            # Calculate total maximum price for each country
            query_total_prices = "SELECT Country, SUM(Price) as total_price FROM airbnb.hotels_info GROUP BY Country"
            total_prices_df = pd.read_sql_query(query_total_prices, engine)

            # Create pie chart for total maximum prices by country
            fig_pie = px.pie(total_prices_df, values='total_price', names='Country', title='Pie Chart of Total Minimum Prices by Country')
            st.plotly_chart(fig_pie)
        
        elif query=="Number of Hotels by Country":
            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)
            
            mycursor.execute( """SELECT Country, COUNT(Name) AS Hotel_Count FROM airbnb.hotels_info \
                     GROUP BY Country \
                     ORDER BY Hotel_Count DESC LIMIT 10""")

            
            out = mycursor.fetchall()
            mydb.commit()

            # Create a DataFrame
            df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])
            
                        

            # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                fig = px.bar(df, x='Country', y='Hotel_Count', title='Number of Hotels by Country')
                st.plotly_chart(fig)
            elif chart_type == "Pie Chart":
                fig = px.pie(df, values='Hotel_Count', names='Country', title='Hotel Counts by Country')
                st.plotly_chart(fig)
            st.write('''## Insights:
                        ### Top Countries
                        The countries with the highest number of hotels indicate a robust hospitality infrastructure. These nations are well-equipped to accommodate large numbers of tourists, which is crucial for both domestic and international tourism.''')

                        
            st.write("### Tourism Hotspots:")
            st.write("-Countries leading in hotel counts are likely significant tourist destinations or major business hubs. This high hotel density suggests a strong demand for accommodations driven by tourism, business travel, and events.")

            st.write("### Strategic Planning for Businesses")
            st.write(" - **Market Entry**: Companies looking to enter the hospitality market can identify potential regions for expansion based on hotel density. Countries with higher hotel counts might offer more opportunities but also face more competition.")
            st.write(" ### Customer Insights")
            st.write("For businesses focusing on customer acquisition and retention, knowing the countries with high hotel density helps in tailoring services to meet the specific needs of tourists from these regions. This could include language services, local cuisine options, and culturally relevant hospitality practices.")           
                       

        elif query=="Average Price of Rooms by Country":
            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)
                                    
            mycursor.execute("SELECT Avg(Price) as average_price,Country,Name FROM airbnb.hotels_info \
                            GROUP BY Country \
                            ORDER BY average_price ASC LIMIT 10")
            out=mycursor.fetchall()
            mydb.commit()
            df=pd.DataFrame(out,columns=[i[0] for i in mycursor.description])
            # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                fig=px.bar(df,x='Country',y='average_price',color='Country',
                    title='Average Price By Country',barmode='stack')
                st.plotly_chart(fig)

            elif chart_type == "Pie Chart":
                # Create a pie chart
                fig = px.pie(df, values='average_price', names='Country', title='Pie Chart of Average price by Country')
                st.plotly_chart(fig)
            st.write('## Insights:')
            st.write("### Affordability Analysis:")
            st.write("- Countries with the lowest average room prices represent more affordable travel destinations. This can attract budget-conscious travelers and boost tourism in these regions.")
            st.write("### Market Positioning")
            st.write("- Businesses can use this data to position their offerings. Countries with lower average prices might need to focus on volume and attracting a larger number of guests, while countries with higher prices can target luxury and premium segments.")
            st.write("### Competitive Landscape")
            st.write("- Understanding the average room prices helps in assessing the competitive landscape. Hotels in countries with higher average prices might offer more premium services and amenities, setting a benchmark for other hotels.")


        elif query=="Average Price of Room Types":
            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)
                            
            mycursor.execute("SELECT Avg(Price) as average_price,Country,Name FROM airbnb.hotels_info \
                            GROUP BY Country \
                            ORDER BY average_price ASC LIMIT 10")
            out=mycursor.fetchall()
            mydb.commit()
            df=pd.DataFrame(out,columns=[i[0] for i in mycursor.description])
            # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                fig=px.bar(df,x='Country',y='average_price',color='Country',
                        title='Average Price By Country',barmode='stack')
                st.plotly_chart(fig)
            elif chart_type == "Pie Chart":
                # Create a pie chart
                fig = px.pie(df, values='average_price', names='Country', title='Pie Chart of Average price by Country')
                st.plotly_chart(fig)
            st.write("### Affordability Analysis")
            st.write("- Countries with the lowest average room prices are attractive destinations for budget-conscious travelers. These countries can leverage their affordability to boost tourism, attracting a larger volume of tourists who seek value for money.")
            st.write("Promotion and Marketing")
            st.write("Tourism boards and travel agencies can promote destinations with lower average prices to budget travelers and backpackers, potentially increasing tourist footfall and spending in these regions. Highlighting the affordability and unique experiences available in these destinations can attract a broader audience.")
        
        
        elif query=="Count of Room Types by Country":
            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute('use airbnb')
            mycursor.execute("SELECT Country,Room_Type,count(Room_Type) as Count_room_type from airbnb.rooms_info \
                             JOIN hotels_info on rooms_info.id = hotels_info.id \
                             GROUP by Country,Room_Type \
                             ORDER BY Count_room_type DESC")
            out=mycursor.fetchall()
            mydb.commit()
            df=pd.DataFrame(out,columns=[i[0] for i in mycursor.description])
            # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                # Create a stacked bar plot
                fig = px.bar(df, x='Country', y='Count_room_type', color='Room_Type', 
                                title='Count of Room Types by Country', barmode='stack')
                st.plotly_chart(fig)
            elif chart_type == "Pie Chart":
                #Create a pie chart
                fig = px.pie(df, values='Count_room_type', names='Country', title='Pie Chart of Room Type count by Country')
                st.plotly_chart(fig)
            st.write("## Insights:### Room Type Distribution")
            st.write("- Understanding the distribution of room types across different countries can help in identifying market trends and preferences. Countries with a higher count of specific room types might indicate a demand for those types, guiding hotels in their room offerings.")
            st.write("### Strategic Planning for Hotels")
            st.write("- Hotels can use this information to align their room offerings with market demand. For instance, if a country shows a high count of budget rooms, hotels might focus on offering more affordable options. Conversely, a high count of luxury rooms indicates a market for premium services.")

        elif query=="Average Monthly Price":
            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)

            # Execute the query
            mycursor.execute("SELECT Name,Country,Avg(Monthly_price) as Monthly_price FROM airbnb.hotels_info \
                            GROUP BY Country \
                            ORDER BY Monthly_price")

            # Fetch the results
            out = mycursor.fetchall()

            # Create a DataFrame from the results
            df = pd.DataFrame(out, columns=[i[0] for i in mycursor.description])

            # Create a Streamlit app
            st.title("Average Monthly Price of Airbnb Listings by Country")

            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(10, 8))

            # Create a horizontal bar chart
            ax.barh(df['Country'], df['Monthly_price'])

            # Set the labels and title
            ax.set_xlabel('Average Monthly Price')
            ax.set_ylabel('Country')
            ax.set_title('Average Monthly Price of Airbnb Listings by Country')
        # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                # Create a stacked bar plot
            # Show the plot in Streamlit
                st.pyplot(fig)
            elif chart_type == "Pie Chart":
                fig = px.pie(df, names='Country', values='Monthly_price', hole=0.5)
                st.plotly_chart(fig)
            st.write("### Average Monthly Price Variation")
            st.write("- The average monthly price varies significantly across countries, reflecting differences in cost of living, demand-supply dynamics, and tourism trends. Understanding these variations helps travelers plan their budgets and choose destinations that offer affordable long-term stays.")
            st.write("### Customer Preferences")
            st.write("- nalyzing average monthly prices helps businesses understand customer preferences and tailor offerings to meet diverse needs. Hotels and accommodation providers can adjust amenities, services, and pricing strategies to attract long-term guests and enhance customer satisfaction.")
        
        elif query=="Average Weekly Price":

            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("SELECT Name,Country,Avg(Weekly_price) as Weekly_price FROM airbnb.hotels_info \
                    GROUP BY Country \
                    ORDER BY Weekly_price")
            out=mycursor.fetchall()
            mydb.commit()
            df=pd.DataFrame(out,columns=[i[0] for i in mycursor.description])
            st.title("Average Weekly Price of Airbnb Listings by Country")

            # Create a figure and axis
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.barh(df['Country'], df['Weekly_price'])
            ax.set_xlabel('Average Weekly Price')
            ax.set_ylabel('Country')
            ax.set_title('Average Weekly Price of Airbnb Listings by Country')
            # Show the plot in Streamlit
            # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                # Create a stacked bar plot
            # Show the plot in Streamlit
                st.pyplot(fig)
            elif chart_type == "Pie Chart":
                fig = px.pie(df, names='Country', values='Weekly_price', hole=0.5)
            st.plotly_chart(fig)
            st.write("### Seasonal Variations")
            st.write("- Seasonal variations in tourism can influence average weekly prices, with peak seasons driving prices higher. Understanding these fluctuations helps businesses optimize pricing strategies and plan for demand fluctuations throughout the year.")
            st.write("### Economic Implications")
            st.write("- The average weekly price reflects economic factors such as currency strength, inflation rates, and overall economic stability. Policymakers can use this data to assess economic competitiveness and formulate policies to support tourism development and investment.")

        elif query=="Maximum Security Deposit":

            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("SELECT Name,Country,MAX(Security_deposit) as Security_deposit FROM airbnb.hotels_info \
                    GROUP BY Country,Name \
                    ORDER BY Security_deposit DESC Limit 20")
            out=mycursor.fetchall()
            mydb.commit()
            df=pd.DataFrame(out,columns=[i[0] for i in mycursor.description])
            # Create a bar chart
            fig = px.bar(df, 
                        x='Name', 
                        y='Security_deposit', 
                        color='Country', 
                        title='Maximum Security Deposits of Hotels by Country',
                        labels={'Name': 'Hotel Name', 'Security_deposit': 'Security Deposit'},
                        hover_data=['Country'],
                        hover_name='Country')
            # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                # Create a stacked bar plot
            # Show the plot in Streamlit
            # Show the chart
                st.plotly_chart(fig)
            elif chart_type == "Pie Chart":
                fig = px.pie(df, names='Country', values='Security_deposit', hole=0.5)
                st.plotly_chart(fig)
            st.write("### Maximum Security Deposit Variation")
            st.write("The maximum security deposit varies significantly across properties and countries, influenced by factors such as property type, location, and rental policies. Understanding these variations helps travelers budget for potential expenses and property owners set competitive deposit amounts.")
            st.write("### Policy Considerations")
            st.write("Policymakers may consider regulating security deposit practices to protect both guests and property owners. Establishing guidelines for deposit amounts, refund timelines, and dispute resolution can promote fairness and transparency in the rental market.")

        elif query=="Minimum Security Deposit":

            import mysql.connector
            mydb = mysql.connector.connect(host="localhost",user="root",password="")
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("SELECT Name,Country,Min(Security_deposit) as Security_deposit FROM airbnb.hotels_info \
                    GROUP BY Country,Name \
                    ORDER BY Security_deposit DESC Limit 20")
            out=mycursor.fetchall()
            mydb.commit()
            df=pd.DataFrame(out,columns=[i[0] for i in mycursor.description])
            # Create a bar chart
            fig = px.bar(df, 
                        x='Name', 
                        y='Security_deposit', 
                        color='Country', 
                        title='Minimum Security Deposits of Hotels by Country',
                        labels={'Name': 'Hotel Name', 'Security_deposit': 'Security Deposit'},
                        hover_data=['Country'],
                        hover_name='Country')
            # Add a selection box for the chart type
            chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart"])

            # Create and display the chart based on user selection
            if chart_type == "Bar Chart":
                # Create a stacked bar plot
            # Show the plot in Streamlit
            # Show the chart
                st.plotly_chart(fig)
            elif chart_type == "Pie Chart":
                fig = px.pie(df, names='Country', values='Security_deposit', hole=0.5)
                st.plotly_chart(fig)
            st.write("### Guest Experience")
            st.write("- Minimum security deposit requirements can impact the guest experience, with excessive deposit amounts potentially deterring bookings or causing dissatisfaction. Property owners should strike a balance between security needs and guest convenience to enhance the guest experience.")
            st.write("### Regulatory Compliance")
            st.write("- Property owners should ensure compliance with relevant laws and regulations governing security deposit practices. Understanding legal requirements and implementing transparent deposit policies help maintain guest trust and avoid legal issues.")
                        
                        