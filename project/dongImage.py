# import pandas as pd
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# sns.set(font='Malgun Gothic')
#
# # CSV 파일이 있는 디렉토리 경로 지정
# directory_path = './경기'
#
# # 디렉토리 안의 모든 CSV 파일 찾기
# files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
# # 파일들을 읽어와서 데이터를 합치기
# merged_data = pd.concat([pd.read_csv(os.path.join(directory_path, file)) for file in files], ignore_index=True)
#
# # 거래금액 처리
# merged_data['거래금액'] = merged_data['거래금액'].str.replace(',', '').astype(int)
#
# # 법정동별 데이터 개수 구하기
# count_by_dong = merged_data['법정동'].value_counts()
#
# # 1.5% 미만인 법정동들을 하나로 합치기
# threshold = 0.015
# small_dongs = count_by_dong[count_by_dong / count_by_dong.sum() < threshold].index
# merged_data['법정동'] = merged_data['법정동'].replace(small_dongs, '1.5%미만')
#
# # 갱신된 법정동별 데이터 개수 계산
# count_by_dong = merged_data['법정동'].value_counts()
#
# # Pie chart: 법정동별 데이터 개수
# plt.figure(figsize=(12, 6))
# plt.subplot(1, 2, 1)
# count_by_dong.plot.pie(autopct='%1.1f%%', startangle=90)
# plt.title('법정동별 데이터 개수')
#
# # Bar chart: 법정동별 평균 거래금액
# plt.subplot(1, 2, 2)
# avg_price_by_dong = merged_data.groupby('법정동')['거래금액'].mean()
# avg_price_by_dong.plot(kind='bar', color='skyblue')
# plt.title('법정동별 평균 거래금액')
#
# plt.tight_layout()
# plt.show()


#----------------- 위 두 데이터를 통한 상관관계 분석--------------------------------
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Malgun Gothic')

# CSV 파일이 있는 디렉토리 경로 지정
directory_path = './서울'

# 디렉토리 안의 모든 CSV 파일 찾기
files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
# 파일들을 읽어와서 데이터를 합치기
merged_data = pd.concat([pd.read_csv(os.path.join(directory_path, file)) for file in files], ignore_index=True)

# 거래금액 처리
merged_data['거래금액'] = merged_data['거래금액'].str.replace(',', '').astype(int)

# 법정동별 데이터 개수와 평균 거래금액 계산
count_by_dong = merged_data['법정동'].value_counts()
avg_price_by_dong = merged_data.groupby('법정동')['거래금액'].mean()

# Scatter plot: 거래 횟수 vs. 평균 거래금액
plt.figure(figsize=(10, 6))
sns.scatterplot(x=count_by_dong, y=avg_price_by_dong, hue=count_by_dong.index, palette='viridis', s=100)
plt.xlabel('거래 횟수')
plt.ylabel('평균 거래금액')
plt.title('법정동별 거래 횟수와 평균 거래금액 비교')

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
