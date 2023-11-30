import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('.csv')

# '거래금액'을 숫자로 변환
df['거래금액'] = df['거래금액'].str.replace(',', '').astype(int)
print(df)
# '년'과 '월'을 합쳐서 새로운 열 '년월' 생성
df['년월'] = df['년'].astype(str) + '-' + df['월'].astype(str)

# '년월'로 그룹화하여 거래금액의 평균 계산
monthly_avg = df.groupby('년월')['거래금액'].mean().reset_index()

# 시각화
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg['년월'], monthly_avg['거래금액'], marker='o')
plt.title('Average Transaction Amount by Month (2015-2021)')
plt.xlabel('Year-Month')
plt.ylabel('Transaction Amount (Average)')
plt.xticks(rotation=45)
plt.show()