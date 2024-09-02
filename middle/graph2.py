import pandas as pd
import matplotlib.pyplot as plt
import platform

new_passenger_data = pd.read_excel('middle/대구광역시 구군별 이용객 인구.xlsx')

if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')

plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))
plt.barh(new_passenger_data['구군별'], new_passenger_data['이용객/인구'], color='skyblue', label='이용객/인구 비율')
plt.xlabel('이용객/인구 비율')
plt.ylabel('구군')
plt.title('구군별 이용객/인구 비율')
plt.legend(loc='upper right')

plt.savefig('구군별_이용객_인구_비율_가로막대.png')

plt.show()
