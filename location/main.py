import pandas as pd
import folium

# Load the data from the uploaded Excel files
file_path1 = 'location/골목길_위도_경도.xlsx'
file_path2 = 'location/대구도시철도공사역위치.xlsx'

data1 = pd.read_excel(file_path1)
data2 = pd.read_excel(file_path2)

# Extract latitude and longitude from both datasets
coordinates1 = data1[['위도', '경도']].values.tolist()
coordinates2 = data2[['위도', '경도']].values.tolist()

# Create a map centered around Daegu
map_daegu = folium.Map(location=[35.87222, 128.60250], zoom_start=12)

# Add markers for the 골목길 data
for coord in coordinates1:
    folium.Marker(location=coord, icon=folium.Icon(color='blue')).add_to(map_daegu)

# Add markers for the 대구도시철도공사역위치 data
for coord in coordinates2:
    folium.Marker(location=coord, icon=folium.Icon(color='red')).add_to(map_daegu)

# Save the map to an HTML file
map_daegu.save('daegu_raod_map.html')
