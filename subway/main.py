import pandas as pd
import folium

usage_file_path = 'subway/대구도시철도공사_월별승차인원.csv'
location_file_path = 'subway/대구도시철도공사역위치.xlsx'


usage_data = pd.read_csv(usage_file_path, encoding='euc-kr')


location_data = pd.read_excel(location_file_path)


usage_data['년도'] = usage_data['년'].str.replace('년', '').astype(int)
usage_2020 = usage_data[usage_data['년도'] == 2019]


station_columns = usage_2020.columns[4:]  
station_columns_clean = station_columns.str.replace(r'\d+', '', regex=True)


usage_2020.columns = usage_2020.columns[:4].tolist() + station_columns_clean.tolist()
usage_2020_sum = usage_2020.groupby(axis=1, level=0).sum()


usage_summary_df = usage_2020_sum.sum().reset_index()
usage_summary_df.columns = ['Station', 'Total Boarding']


location_data.rename(columns={
    '역명': 'Station',
    '위도': 'Latitude',
    '경도': 'Longitude'
}, inplace=True)


merged_df = pd.merge(usage_summary_df, location_data, on='Station', how='inner')

daegu_location = [35.8714, 128.6014]


m = folium.Map(location=daegu_location, zoom_start=12)

for index, row in merged_df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],  
        radius=row['Total Boarding'] / 100000,
        popup=f"Station: {row['Station']}\nBoarding: {row['Total Boarding']}",  #
        color='red',  
        fill=True, 
        fill_color='red'  
    ).add_to(m)

map_path = 'daegu_metro_stops_usage_map.html'


m.save(map_path)

print(f"Map saved to {map_path}")