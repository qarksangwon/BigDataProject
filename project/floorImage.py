import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font='Malgun Gothic')

files = [file for file in os.listdir() if file.endswith('*.csv')]

# 파일들을 읽어와서 데이터를 합치기
merged_data = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

merged_data['거래금액'] = merged_data['거래금액'].str.replace(',', '').astype(int)

# '층' 값을 15층 미만, 15~30층, 30층 초과로 나누기
merged_data['층 구간'] = pd.cut(merged_data['층'], bins=[-float('inf'), 15, 30, float('inf')],
                              labels=['15층 미만', '15~30층', '30층 초과'])

# 년도별 층 구간별 평균 거래금액 계산
avg_price_by_year_floor_range = merged_data.groupby(['년', '층 구간'], observed=False)['거래금액'].mean().reset_index()

# 각 년도에 대한 서브플롯 생성
plt.figure(figsize=(15, 10))
for i, year in enumerate(avg_price_by_year_floor_range['년'].unique(), 1):
    plt.subplot(3, 3, i)

    # 해당 년도의 데이터 선택
    year_data = avg_price_by_year_floor_range[avg_price_by_year_floor_range['년'] == year]

    # 막대 그래프 생성
    sns.barplot(x='층 구간', y='거래금액', data=year_data)

    # 서브플롯 제목 설정
    plt.title(f'년도: {year}')

# 전체 그래프 제목 설정
plt.suptitle('년도별 층 구간별 평균 거래금액', y=1.02)

# 레이아웃 조절
plt.tight_layout()
plt.show()
