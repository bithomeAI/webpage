import requests
import pandas as pd
import json
import time


# #【一分一档表】
# headers = {
#     "sec-ch-ua-platform": "\"Windows\"",
#     "Referer": "https://www.gaokao.cn/",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
#     "Accept": "application/json, text/plain, */*",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0"
# }
# url = "https://static-data.gaokao.cn/www/2.0/section2021/2024/13/2073/3/lists.json"
# params = {
#     "a": "www.gaokao.cn"
# }
# response = requests.get(url, headers=headers, params=params)
# # print(response.text)
# # print(response.json()["data"])
# df=pd.DataFrame(response.json()["data"]["search"]).T
# df.to_csv("一分一档表.csv",index=False,encoding="utf_8_sig")



#【热门专业】
headers = {
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://www.gaokao.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Accept": "application/json, text/plain, */*",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0"
}
url = "https://static-data.gaokao.cn/www/2.0/special/level/hot.json"
params = {
    "a": "www.gaokao.cn"
}
response = requests.get(url, headers=headers, params=params)
print(response.text)
print(response)
df=pd.DataFrame(response.json()["data"]["1"])
print(df)
df["男女比例"]=df.apply(lambda x:f"{x["boy_rate"]}/{x["girl_rate"]}",axis=1)
df["专业名称"]=df["name"]
df=df.rename(columns={"hightitle":"专业名称","spcode":"专业代码",
                            "degree":"学位名称","level1_name":"本科专科",
                            "level2_name":"专业大类","level3_name":"专业小类",
                            # "name":"专业名称",
                            "fivesalaryavg":"最近五年平均薪酬",
                            "salaryavg":"平均薪酬",
                            "limit_year":"学制",
                            })
df.to_csv("热门专业.csv",index=False,encoding="utf_8_sig")


#【专业薪酬】
try:
    alldf=pd.read_csv("各专业薪酬.csv")
    num=int(df["level3"].max())
except:
    print("没有文件")
    alldf=pd.DataFrame()
    num=0
for a in range(1,1000):
    if a>num:
        try:
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "content-type": "application/json",
                "origin": "https://www.gaokao.cn",
                "priority": "u=1, i",
                "referer": "https://www.gaokao.cn/",
                "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
            }
            url = "https://api.zjzw.cn/web/api/"
            params = {
                "keyword": "",
                "level3": f"{int(a)}",
                "page": "1",
                "size": "2000",
                "uri": "apidata/api/gkv3/special/lists",
                "signsafe": "0b8c62335685625f3e2e05eeb98708b5"
            }
            data = {
                "keyword": "",
                "level3": f"{int(a)}",
                "page": 1,
                "size": 2000,
                "uri": "apidata/api/gkv3/special/lists",
                "signsafe": "0b8c62335685625f3e2e05eeb98708b5",
            }
            data = json.dumps(data, separators=(',', ':'))
            response = requests.post(url, headers=headers, params=params, data=data)
            print(response.text)
            print(response)
            df=pd.DataFrame(response.json()["data"]["item"])
            df=df.rename(columns={"hightitle":"专业名称","spcode":"专业代码",
                                        "degree":"学位名称","level1_name":"本科专科",
                                        "level2_name":"专业大类","level3_name":"专业小类",
                                        # "name":"专业名称",
                                        "fivesalaryavg":"最近五年平均薪酬",
                                        "salaryavg":"平均薪酬",
                                        "limit_year":"学制",
                                        })
            if not df.empty:
                alldf=pd.concat([alldf,df])
                print(alldf)
            time.sleep(0.5)
        except:
            break
alldf.to_csv("各专业薪酬.csv",index=False,encoding="utf_8_sig")


# #【专业】
# headers = {
#     "sec-ch-ua-platform": "\"Windows\"",
#     "Cache-Control": "no-cache",
#     "Referer": "https://mnzy.gaokao.cn/",
#     "Pragma": "no-cache",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "strategy-type": "X-Is-Cacheable-Cache-First-Config",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
#     "Accept": "application/json, text/plain, */*",
#     "token": "2abf5bca98824756a3aab9aa4bbd7f8d"
# }
# url = "https://static-api.syeol.cn/api/hint/v3/majorClassHint"
# params = {
#     "gradeType": "本科"
# }
# response = requests.get(url, headers=headers, params=params)
# # print(response.text)
# # print(response)
# df=pd.DataFrame(response.json()["body"])
# print(df)
# alldf=pd.DataFrame()
# for indnex,thisdf in df.iterrows():
#     indexthisdf=pd.DataFrame(thisdf["children"])
#     print(indexthisdf)
#     oneid=thisdf['id']
#     onename=thisdf['name']
#     for indnex,thisdf in indexthisdf.iterrows():
#         twoindexthisdf=pd.DataFrame(thisdf["children"])
#         twoid=thisdf['id']
#         twoname=thisdf['name']
#         twoindexthisdf['一级专业id']=oneid
#         twoindexthisdf['一级专业']=onename
#         twoindexthisdf['二级专业id']=twoid
#         twoindexthisdf['二级专业']=twoname
#         twoindexthisdf['三级专业id']=twoindexthisdf["id"]
#         twoindexthisdf['三级专业']=twoindexthisdf["name"]
#         alldf=pd.concat([alldf,twoindexthisdf])
# alldf.to_csv("专业类别.csv",encoding="utf_8_sig")
# alldf=alldf[["一级专业id","一级专业","二级专业id","二级专业","三级专业id","三级专业"]]
# alldf=alldf.rename(columns={"allname":"职业类别","name":"职业名称"})
# #【包含列名】
# json_str = alldf.to_json(orient='records', 
#                          force_ascii=False,#避免非force_ascii字符被转义【保留中文】
#                          )
# # print(json_str)
# # with open('志愿填报数据.json','w',encoding='utf-8') as json_file:#encoding='utf-8'保留中文字符
# #     json_file.write(json_str)
# #【去掉列名】
# import json
# records=json.loads(json_str)
# # 处理每个记录，移除列名
# # records_without_column_names = str([record.items() for record in records])#【这里获取的是元素】
# records_without_column_names = str([list(record.values()) for record in records])#【这里获取的是值】
# # # 将处理后的记录转换回 JSON 字符串
# # json_str = json.dumps(records_without_column_names, ensure_ascii=False)
# # print(records_without_column_names)
# with open('特殊格式专业类别数据.json','w',encoding='utf-8') as json_file:#encoding='utf-8'保留中文字符
#     json_file.write(records_without_column_names)



# #【职业】
# headers = {
#     "sec-ch-ua-platform": "\"Windows\"",
#     "Cache-Control": "no-cache",
#     "Referer": "https://mnzy.gaokao.cn/",
#     "Pragma": "no-cache",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "strategy-type": "X-Is-Cacheable-Cache-First",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
#     "Accept": "application/json, text/plain, */*",
#     "token": "2abf5bca98824756a3aab9aa4bbd7f8d"
# }
# url = "https://mnzy.gaokao.cn/api/cp/queryAllList"
# response = requests.get(url, headers=headers)
# # print(response.text)
# # print(response)
# df=pd.DataFrame(response.json()["body"])
# alldf=pd.DataFrame()
# for indnex,thisdf in df.iterrows():
#     indexthisdf=pd.DataFrame(thisdf["list"])
#     print(indexthisdf)
#     indexthisdf['allid']=thisdf['id']
#     indexthisdf['allname']=thisdf['name']
#     alldf=pd.concat([alldf,indexthisdf])
# alldf.to_csv("职业列表.csv",encoding="utf_8_sig")
# alldf=alldf[["allname","name"]]
# alldf=alldf.rename(columns={"allname":"职业类别","name":"职业名称"})
# #【包含列名】
# json_str = alldf.to_json(orient='records', 
#                          force_ascii=False,#避免非force_ascii字符被转义【保留中文】
#                          )
# # print(json_str)
# # with open('志愿填报数据.json','w',encoding='utf-8') as json_file:#encoding='utf-8'保留中文字符
# #     json_file.write(json_str)
# #【去掉列名】
# import json
# records=json.loads(json_str)
# # 处理每个记录，移除列名
# # records_without_column_names = str([record.items() for record in records])#【这里获取的是元素】
# records_without_column_names = str([list(record.values()) for record in records])#【这里获取的是值】
# # # 将处理后的记录转换回 JSON 字符串
# # json_str = json.dumps(records_without_column_names, ensure_ascii=False)
# # print(records_without_column_names)
# with open('特殊格式职业列表数据.json','w',encoding='utf-8') as json_file:#encoding='utf-8'保留中文字符
#     json_file.write(records_without_column_names)



# #【理科专业】缺东西
# headers = {
#     "sec-ch-ua-platform": "\"Windows\"",
#     "Cache-Control": "no-cache",
#     "Referer": "https://mnzy.gaokao.cn/",
#     "Pragma": "no-cache",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0",
#     "strategy-type": "X-Is-Cacheable-Cache-First",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
#     "Accept": "application/json, text/plain, */*",
#     "token": "2abf5bca98824756a3aab9aa4bbd7f8d"
# }
# url = "https://mnzy.gaokao.cn/api/cp/queryRmMajor"
# params = {
#     "classify": "物理",
#     # "level": "1"
# }
# response = requests.get(url, headers=headers, params=params)
# # print(response.text)
# # print(response)
# df=pd.DataFrame(response.json()["body"]["tbList"])
# print(df)
# df.to_csv("理科专业列表.csv",index=False,encoding="utf_8_sig")


# #【考试类型】
# headers = {
#     "sec-ch-ua-platform": "\"Windows\"",
#     "Referer": "https://mnzy.gaokao.cn/",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
#     "Accept": "application/json, text/plain, */*",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0"
# }
# url = "https://static-data.gaokao.cn/www/2.0/single/config/province.json"
# params = {
#     "a": "mnzy.gaokao.cn"
# }
# response = requests.get(url, headers=headers, params=params)
# # print(response.text)
# # print(response)
# df=pd.DataFrame(response.json())
# print(df)
# df.to_csv("考试类型.csv",index=False,encoding="utf_8_sig")


# #【广告页面】
# headers = {
#     "sec-ch-ua-platform": "\"Windows\"",
#     "Referer": "https://mnzy.gaokao.cn/",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
#     "Accept": "application/json, text/plain, */*",
#     "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
#     "sec-ch-ua-mobile": "?0"
# }
# url = "https://static-gkcx.gaokao.cn/www/2.0/json/operate/2/13/3.json"
# params = {
#     "a": "mnzy.gaokao.cn"
# }
# response = requests.get(url, headers=headers, params=params)
# # print(response.text)
# # print(response)
# df=pd.DataFrame(response.json()["data"])
# print(df)
# df.to_csv("考试类型.csv",index=False,encoding="utf_8_sig")


