import json
import requests
import xmltodict
import pandas as pd


# api 사용을 위한 인증키 입력
serviceKey = "내 키는 비밀"
url ="http://openapi.molit.go.kr:8081/내 키는 비밀"


def get_df(lawd_cd, deal_ym): #lawd_cd= 법정동 코드 / deal_ym = 계약연월
    global serviceKey
    base_url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?serviceKey="+serviceKey
    base_url += f'&LAWD_CD={lawd_cd}'
    base_url += f'&DEAL_YMD={deal_ym}'

    res = requests.get(base_url)
    data = json.loads(json.dumps(xmltodict.parse(res.text)))
    df = pd.DataFrame(data['response']['body']['items']['item'])
    drop_df(df)
    return df
# 데이터 거래 금액/ 건축 년도/ 법정동/ 아파트/ 전용 면적/ 지번/ 지역 코드/ 층/ 년/ 월/ 일/ 등기 일자/ 중개사 소재지/ 거래 유형/ 해제 사유 발생일 / 해제 여부

def drop_df(df): # df로 변환과정에서 필요없는 데이터 제거
    df.drop(['건축년도','등기일자','일','중개사소재지','거래유형','지역코드','해제사유발생일','해제여부'], axis=1,inplace=True)

#서울--------------------------
# df = get_df(11680 ,201501) #강남구
# df2= get_df(11740,202309) #강동구
# df3= get_df(11305,202309) #강북구
# df4= get_df(11500,202309) #강서구
# df5= get_df(11620,202309) #관악구
# df6= get_df(11350,202309) #노원구

#경기---------------------------
# 41190 #부
# 41135 #성남시 분당구
# 41111 #수원시 장안구
# 41390 #시흥시
# 41273 #안산시 단원구
# 41173 #안양시 동안구
# 41590 #화성시

#강원도-------------------------
# 42150 강릉시
# 42750 영월군
# 42210 속초시
# 42780 철원군

#충북---------------------------
# 43740 영동군
# 43760 괴산군

#충남---------------------------
# 44250 계룡시
# 44150 공주시
# 44230 논산시
merge_df = pd.DataFrame()

for year in range(2015,2022):
    for month in range(1,13):
        ym = int(f'{year}{month:02d}')
        df = get_df(42750,ym)
        merge_df = pd.concat([merge_df,df],ignore_index = True)
        merge_df.to_csv('강릉시.csv', index=False)
