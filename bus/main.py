import pandas as pd
import folium


usage_file_path = '정류소이용현황(202405).csv'         
location_file_path = '대구광역시_시내버스 정류소 위치정보_20230731.csv'     

usage_data = pd.read_csv(usage_file_path)       
location_data = pd.read_csv(location_file_path)

columns = usage_data.iloc[0].fillna('') + usage_data.iloc[1].fillna('')         

usage_data.columns = columns

usage_data = usage_data.drop([0, 1])

usage_data.reset_index(drop=True, inplace=True)     

usage_data.rename(columns={         
    '구분': 'Station',
}, inplace=True)

stations = usage_data['Station']

boarding_cols = [col for col in usage_data.columns if '승차' in col]

alighting_cols = [col for col in usage_data.columns if '하차' in col]


total_boarding = usage_data[boarding_cols].astype(int).sum(axis=1)

total_alighting = usage_data[alighting_cols].astype(int).sum(axis=1)

usage_summary_df = pd.DataFrame({
    'Station': stations,
    'Total Boarding': total_boarding,
    'Total Alighting': total_alighting
})

location_data.rename(columns={
    '정류소명': 'Station',
    '위도': 'Latitude',
    '경도': 'Longitude'
}, inplace=True)

merged_df = pd.merge(usage_summary_df, location_data, on='Station', how='inner')

daegu_location = [35.8714, 128.6014]

m = folium.Map(location=daegu_location, zoom_start=12)


for index, row in merged_df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']], 
        radius=row['Total Boarding'] / 1000,  
        popup=f"Station: {row['Station']}\nBoarding: {row['Total Boarding']}\nAlighting: {row['Total Alighting']}", 
        color='blue',  
        fill=True, 
        fill_color='blue' 
    ).add_to(m)

map_path = 'daegu_bus_stops_map.html'
m.save(map_path)
