import geopandas as gpd
import pandas as pd
import folium
import os
import zipfile
from branca.colormap import linear

extracted_folder_path = 'population/2023년+06월+LX법정구역경계_시군구_대구광역시 2'
gdfs = []
for file_name in os.listdir(extracted_folder_path):
    if file_name.endswith('.zip'):
        zip_file_path = os.path.join(extracted_folder_path, file_name)
        subfolder_path = zip_file_path.replace('.zip', '')
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(subfolder_path)
        
        shp_file = [f for f in os.listdir(subfolder_path) if f.endswith('.shp')][0]
        shp_filepath = os.path.join(subfolder_path, shp_file)
        gdf = gpd.read_file(shp_filepath)
        gdfs.append(gdf)

daegu_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))

daegu_gdf['Region_Label'] = daegu_gdf['SGG_NM']

csv_file_path = 'population/대구광역시_주민등록인구및세대현황_20240531.csv'
data = pd.read_csv(csv_file_path, encoding='cp949')

data = data[data['행정구역'].str.contains('군위군') == False]
data.columns = ['Region', 'Total_Population', 'Households', 'Population_per_Household', 'Male_Population', 'Female_Population', 'Gender_Ratio']
data['Region_Label'] = data['Region'].apply(lambda x: x.split(' ')[-2])

data['Total_Population'] = pd.to_numeric(data['Total_Population'], errors='coerce')
daegu_gdf = daegu_gdf.merge(data[['Region_Label', 'Total_Population']], on='Region_Label')

daegu_center = [35.8714, 128.6014]

m = folium.Map(location=daegu_center, zoom_start=11)

color_scale = linear.Blues_09.scale(0, 550000)
color_scale.caption = 'Total Population by Region'

folium.GeoJson(
    daegu_gdf,
    style_function=lambda feature: {
        'fillColor': color_scale(feature['properties']['Total_Population']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['Region_Label', 'Total_Population'],
        aliases=['구 이름:', '총 인구수:'],
        localize=True
    )
).add_to(m)

color_scale.add_to(m)

m.save('daegu_population_map_with_text_labels.html')


