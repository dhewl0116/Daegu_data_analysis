import pandas as pd
import matplotlib.pyplot as plt
import platform

stations_df = pd.read_excel('middle/대구광역시 구군별 역 개수.xlsx')
passengers_df = pd.read_excel('middle/대구광역시 구군별 일일 도시철도 이용객수.xlsx')

stations_count = stations_df.set_index('구군별')['역 개수']
passengers_sum = passengers_df.groupby('구군')['이용객'].sum()
data_combined = pd.concat([stations_count, passengers_sum], axis=1)

if platform.system() == 'Darwin':  
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')

plt.rcParams['axes.unicode_minus'] = False

fig, ax1 = plt.subplots(figsize=(10, 6))

bars = ax1.bar(data_combined.index, data_combined['역 개수'], color='skyblue', label='역 개수')
ax1.set_xlabel('구군')
ax1.set_ylabel('역 개수', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
line, = ax2.plot(data_combined.index, data_combined['이용객'], color='blue', marker='o', linestyle='-', label='이용객')
ax2.set_ylabel('이용객 수', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + [line], labels + ['이용객 수'], loc='upper right')

plt.title('구군별 역 개수와 이용객 수')
fig.tight_layout()

plt.savefig('구군별_역_개수와_이용객_수.png')

plt.show()
