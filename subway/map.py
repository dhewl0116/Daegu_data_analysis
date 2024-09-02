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

excel_file_path = 'subway/대구광역시 구군별 일일 도시철도 이용객수.xlsx'
usage_data = pd.read_excel(excel_file_path)

print("Excel 파일의 컬럼 이름:", usage_data.columns)

usage_data = usage_data[['코드', '이용객']]
usage_data.columns = ['SGG_CD', 'Total_Usage']

daegu_gdf['SGG_CD'] = daegu_gdf['SGG_CD'].astype(str)
usage_data['SGG_CD'] = usage_data['SGG_CD'].astype(str)

daegu_gdf = daegu_gdf.merge(usage_data, on='SGG_CD')

daegu_center = [35.8714, 128.6014]

m = folium.Map(location=daegu_center, zoom_start=11)

color_scale = linear.Blues_09.scale(0, usage_data['Total_Usage'].max())
color_scale.caption = 'Total subway ride by Region'

folium.GeoJson(
    daegu_gdf,
    style_function=lambda feature: {
        'fillColor': color_scale(feature['properties']['Total_Usage']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['Region_Label', 'Total_Usage'],
        aliases=['구 이름:', '총 이용량:'],
        localize=True
    )
).add_to(m)

color_scale.add_to(m)

m.save('daegu_subway_usage_map.html')
