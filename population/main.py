import pandas as pd
import matplotlib.pyplot as plt

file_path = 'population/대구광역시_주민등록인구및세대현황_20240531.csv'
data = pd.read_csv(file_path, encoding='cp949')

data.columns = [
    'Region', 'Total_Population', 'Households', 'Population_per_Household',
    'Male_Population', 'Female_Population', 'Gender_Ratio'
]

filtered_data = data[data['Region'] != '대구광역시  (2700000000)']

filtered_data.loc[:, 'Region_Label'] = filtered_data['Region'].apply(lambda x: x.split(' ')[-2])

plt.rcParams['font.family'] = 'AppleGothic'

plt.figure(figsize=(10, 6))
plt.bar(filtered_data['Region_Label'], filtered_data['Total_Population'], color='skyblue')
plt.xticks(rotation=90)
plt.title('Total Population by Region (excluding Daegu top-level)')
plt.ylabel('Total Population')
plt.xlabel('Region')

plt.tight_layout()
plt.savefig('total_population_by_region.png')

plt.show()
