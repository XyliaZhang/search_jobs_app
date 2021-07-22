import requests
from bs4 import BeautifulSoup
import pprint as pp
import pandas as pd
import jieba
from openpyxl import load_workbook

def find_jobs_1111(query, days, pages,filename):
  writer = pd.ExcelWriter(r'./jobs_' + filename + '.xlsx')
  jieba.load_userdict('./static/my_dict_skill')
  UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
  headers = {'User-Aagent': UserAgent}

  titles = []
  companies = []
  addresses = []
  salaries = []
  contents = []
  edus = []
  urls = []
  for x in range(int(pages)):
      url = "https://www.1111.com.tw/search/job?ks=" + query + '&page=' + str(x)
      # url = "https://www.1111.com.tw/job/79808792/"
      res = requests.get(url=url, headers=headers)
      soup = BeautifulSoup(res.text, 'html.parser')

      for i in range(len(soup)):
          new_url = soup.select('a.text-truncate')[i]['href']
          new_res = requests.get(url=new_url, headers=headers)
          new_soup = BeautifulSoup(new_res.text, 'html.parser')
          titles.append(new_soup.select('title')[0].text.split("｜")[0].strip())
          companies.append(new_soup.select('title')[0].text.split("｜")[1].strip())
          addresses.append(new_soup.select('title')[0].text.split("｜")[2].strip())
          salaries.append(new_soup.select('span.text--danger')[0].text.strip())
          contents.append(new_soup.select('div.job-detail-info-content')[0].text.strip())
          edus.append(new_soup.select('ul.vacancy-description-main > li > p > span')[5].text.strip())
          urls.append(new_url)
      columns = ['職稱', '公司', '學歷', '地址', '薪資', '職務內容', '1111的url']
      df = pd.DataFrame(columns=columns)
      df['職稱'] = titles
      df['公司'] = companies
      df['學歷'] = edus
      df['地址'] = addresses
      df['薪資'] = salaries
      df['職務內容'] = contents
      df['1111的url'] = urls

      df.drop_duplicates('1111的url', 'first', inplace=True)
      df = df.reset_index(drop=True)
      book = load_workbook(r'./jobs_' + filename + '.xlsx')
      writer.book = book

      df_all.to_excel(writer, sheet_name='104爬蟲資料', encoding='utf-8-sig')
      df_2.to_excel(writer, sheet_name='統計資料', header=True, encoding='utf-8-sig')
      df.to_excel(writer, sheet_name='1111爬蟲資料', encoding='utf-8-sig')
      writer.save()
      # writer.close()
  return df_2
  
  
if __name__ == "__main__":
    #令使用者可設定爬蟲關鍵資料
    query = str(input('設定搜尋關鍵詞:'))
    days = str(input('設定爬取幾日內更新資料:'))
    pages = int(input('設定爬取頁數:'))
    filename = str(input('設定儲存檔名:jobs_'))
    c = find_jobs_1111(query,days,pages,filename)
    print(c)  
