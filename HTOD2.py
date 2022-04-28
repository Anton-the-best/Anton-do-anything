import requests as req
import json
import pandas as pd
import boto3
import matplotlib.pyplot as plt
import numpy as np

response1 = req.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&date=20210101')
json_rep1 = json.loads(response1.text)
response2 = req.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&date=20210301')
json_rep2 = json.loads(response2.text)
response3 = req.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&date=20210501')
json_rep3 = json.loads(response3.text)
response4 = req.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&date=20210701')
json_rep4 = json.loads(response4.text)
response5 = req.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&date=20210901')
json_rep5 = json.loads(response5.text)
response6 = req.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchangenew?json&date=20211101')
json_rep6 = json.loads(response6.text)
json_rep = json_rep1 + json_rep2 + json_rep3 + json_rep4 + json_rep5 + json_rep6

#convert list to json
jsonString = json.dumps(json_rep, ensure_ascii=False, indent = 4) #ensure_ascii - кодування, indent - таби
jsonFile = open("request.json", "w")
jsonFile.write(jsonString)
jsonFile.close()

df1 = pd.read_json("request.json") #json
#print(df1)

df2 = pd.read_json (r'request.json')
df2.to_csv (r'request.json.csv', index = None) #convert to csv

#read from bucket
s3 = boto3.client('s3')

obj = s3.get_object(Bucket= 'narn1bucket', Key= 'request.json.csv') 

df3 = pd.read_csv(obj['Body']) #read csv
print(df3)

#plot
x1 = []
y1 = []
j = 1

for i in df3.index:
    if df3.loc[i,"cc"] == "USD": 
        y1.append(float(df3.loc[i,"rate"]))
        x1.append(int(j))
        j += 2

plt.title("Exchange rate USD from month for 2021")
plt.plot(x1,y1)
plt.savefig('Exchange rate USD from month for 2021.png')
plt.show()

x2 = []
y2 = []
j = 1
for i in df3.index:
    if df3.loc[i,"cc"] == "EUR": 
        y2.append(float(df3.loc[i,"rate"]))
        x2.append(int(j))
        j += 2

plt.title("Exchange rate EUR from month for 2021")
plt.plot(x2,y2)
plt.savefig('Exchange rate EUR from month for 2021.png')
plt.show()