import pandas as pd
import chardet
import matplotlib.pyplot as plt
import seaborn as sns

# CSV 파일 불러오기
merged_data = pd.read_csv('./서울/강남구.csv')

# 거래금액을 숫자로 변환
merged_data['거래금액'] = merged_data['거래금액'].str.replace(',', '').astype(int)

# 년도별 거래금액 평균 계산
yearly_avg = merged_data.groupby('년')['거래금액'].mean().reset_index()

# 파일의 인코딩을 자동으로 감지
with open('출산율.csv', 'rb') as f:
    result = chardet.detect(f.read())

# 감지된 인코딩으로 파일 불러오기
df = pd.read_csv('출산율.csv', encoding=result['encoding'])

# 특정 행 제거 (index 1과 3)
df = df.drop([0, 1])

# '행정구역별'을 인덱스로 설정
df.set_index('행정구역별', inplace=True)

# 데이터 재구성
df = df.melt(var_name='년', value_name='값').reset_index(drop=True)
df = df.drop([7])

# '년' 컬럼의 데이터 타입을 int로 변환
df['년'] = df['년'].astype(int)

# 'yearly_avg'와 'df'를 '년'을 기준으로 합침
result_table = pd.merge(yearly_avg, df, on='년')

# 상관계수 계산
correlation = result_table['거래금액'].astype(float).corr(result_table['값'].astype(float))

# 시각화
plt.figure(figsize=(12, 8))

# 그래프 1: 거래금액
plt.subplot(2, 2, 1)
plt.plot(result_table['년'], result_table['거래금액'], marker='o', label='Transaction Amount')
plt.title('Transaction Amount by Year')
plt.xlabel('Year')
plt.ylabel('Transaction Amount')
plt.legend()

# 그래프 2: 출산율
plt.subplot(2, 2, 2)
plt.plot(result_table['년'], result_table['값'], marker='o', label='Birth Rate')
plt.title('Birth Rate by Year')
plt.xlabel('Year')
plt.ylabel('Birth Rate')
plt.gca().invert_yaxis()  # Invert y-axis
plt.legend()

# 그래프 3: 상관계수 표시 (타이틀)
plt.subplot(2, 2, 3)
plt.text(0.5, 0.5, f'Correlation: {correlation:.2f}', size=15, ha='center', va='center', transform=plt.gca().transAxes)
plt.gca().invert_yaxis()  # Invert y-axis
plt.axis('off')  # 빈 subplot 생성

# 그래프 4: 상관계수 산점도
plt.subplot(2, 2, 4)
plt.scatter(result_table['거래금액'], result_table['값'])
plt.title('Scatter Plot: Transaction Amount vs. Birth Rate')
plt.xlabel('Transaction Amount')
plt.ylabel('Birth Rate')

plt.tight_layout()
plt.show()
