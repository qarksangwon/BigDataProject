import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Malgun Gothic')

files = [file for file in os.listdir() if file.endswith('.csv')]

# 파일들을 읽어와서 데이터를 합치기
merged_data = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

merged_data['거래금액'] = merged_data['거래금액'].str.replace(',', '').astype(int)

# 아파트별 거래 횟수 계산
apartment_counts = merged_data['아파트'].value_counts().reset_index()
apartment_counts.columns = ['아파트', '거래횟수']

# 거래 횟수가 많은 순으로 10개 아파트 선택
top_apartments = apartment_counts.head(10)['아파트'].tolist()

# 상위 10개 아파트에 해당하는 데이터만 필터링
top_apartments_data = merged_data[merged_data['아파트'].isin(top_apartments)]

# 거래 횟수가 10개 이상인 아파트 중에서 데이터가 적은 순으로 10개 아파트 선택
bottom_apartments = apartment_counts[apartment_counts['거래횟수'] >= 10].nsmallest(10, '거래횟수')['아파트'].tolist()

# 상위 10개 아파트에 해당하는 데이터만 필터링
bottom_apartments_data = merged_data[merged_data['아파트'].isin(bottom_apartments)]

# 년도별 아파트별로 평균 거래가 계산
avg_price_top_apartments = top_apartments_data.groupby(['년', '아파트'])['거래금액'].mean().reset_index()
avg_price_bottom_apartments = bottom_apartments_data.groupby(['년', '아파트'])['거래금액'].mean().reset_index()

# 거래 횟수를 추가
avg_price_top_apartments = pd.merge(avg_price_top_apartments, top_apartments_data.groupby(['년', '아파트']).size().reset_index(name='거래횟수'), on=['년', '아파트'])
avg_price_bottom_apartments = pd.merge(avg_price_bottom_apartments, bottom_apartments_data.groupby(['년', '아파트']).size().reset_index(name='거래횟수'), on=['년', '아파트'])

# 시각화
plt.figure(figsize=(15, 12))

# 상위 10개 아파트 - 거래 횟수와 평균 거래가의 관계
plt.subplot(2, 1, 1)
sns.scatterplot(x='거래횟수', y='거래금액', hue='아파트', data=avg_price_top_apartments)
plt.xlabel('거래 횟수')
plt.ylabel('평균 거래가')
plt.title('상위 10개 아파트 - 거래 횟수와 평균 거래가의 관계')

# 하위 10개 아파트 - 거래 횟수와 평균 거래가의 관계
plt.subplot(2, 1, 2)
sns.scatterplot(x='거래횟수', y='거래금액', hue='아파트', data=avg_price_bottom_apartments)
plt.xlabel('거래 횟수')
plt.ylabel('평균 거래가')
plt.title('하위 10개 아파트 - 거래 횟수와 평균 거래가의 관계')

plt.tight_layout()
plt.show()
