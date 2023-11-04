import streamlit as st
import pandas as pd
import numpy as np
import os

#mapping
import geopandas as gpd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import MarkerCluster,HeatMap,HeatMapWithTime
import branca.colormap as colormap
from collections import defaultdict

st.title("Seas the Day with Donations")

st.markdown('''
            ### Oil Spills & Garabage Patches
            
            
            ''')

# st.sidebar()

# plotting_file = gpd.read_file('./sea_micro.csv')
plotting_file = gpd.read_file('./marine_microplastic_density.csv')
oil_spill_df = pd.read_csv('./oilspills_1967-91.csv', encoding='latin-1')

#create a geom obj
def get_geom(df,adn):
    '''get a geometry variable'''
    df[['Latitude','Longitude']]=df[['Latitude','Longitude']].astype(dtype=float)
    df[adn] = df[adn].astype(dtype=float)
#     df[['Latitude','Longitude']]=df[['Latitude','Longitude']].astype('float16')
    df['Geometry'] = pd.Series([(df.loc[i,'Latitude'],df.loc[i,'Longitude']) for i in range(len(df['Latitude']))])
    
def to_datetime(df,date_col='Date',frmt='%Y-%m-%d'):
    '''add_date col as datetime'''
    df[date_col] =pd.to_datetime(df[date_col],errors='coerce')
    df['year'] = df[date_col].dt.year
    
# oil_spill_gdf = gpd.GeoDataFrame(oil_spill_df, 
#                                  geometry=gpd.points_from_xy(oil_spill_df['Longitude'], oil_spill_df['Latitude'],))


# oil_spill_gdf.crs = "EPSG:4326"

get_geom(plotting_file,'Total_Pieces_L')

#set to datetime'
to_datetime(plotting_file)
# to_datetime(geomar)
# to_datetime(sea_micro)

# find loc
max_plas = plotting_file['Total_Pieces_L'].max()
idx= plotting_file[plotting_file['Total_Pieces_L']==max_plas].index
loc1= plotting_file.iloc[idx][['Latitude','Longitude']].values

start_loc= (np.mean(plotting_file['Latitude']),np.mean(plotting_file['Longitude']))

#map
m_1=folium.Map(location=start_loc,
              tiles='Open Street Map',
              zoom_start=2,
              min_zoom=1.5)

#heatmap:
HeatMap(data=plotting_file[['Latitude','Longitude','Total_Pieces_L']].values, 
        # oil_spill_df[['Longtitude', 'Latitude', 'Density']],
        radius=10,
        blur=5).add_to(m_1)

#add area of highest concentration
folium.CircleMarker(location= (loc1[0][0],loc1[0][1]),
                  tooltip="<b>max plastic density</b>",
                  color='black',
                  radius=15).add_to(m_1)

# folium.GeoJson(oil_spill_df,
#                name='Oil Spill Data',
#                tooltip=folium.GeoJsonTooltip(fields=['Longitude', 'Latitude'])  # Specify the fields you want to show in the tooltip
#                ).add_to(m_1)

folium_static(m_1)

# st_data = st_folium(m_1, width=725)
