import requests
from bs4 import BeautifulSoup
import json
import pprint as pp
import pandas as pd
import jieba
import numpy as np
from openpyxl import load_workbook



def find_jobs_104(query, days, pages, filename ):
    writer = pd.ExcelWriter(r'./jobs_' + filename + '.xlsx')
    jieba.load_userdict('./static/my_dict_skill')
    UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    headers = {'User-Aagent': UserAgent}

    jobs = []
    companies = []
    addresses = []
    edus = []
    salaries = []
    job_descs = []
    skills = []
    analys_urls = []
    company_104urls = []
    df_1_list = []
    for x in range(int(pages)):
        url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&isnew=' + days + '&keyword=' + query + '&page=' + str(
            pages)
        res = requests.get(url=url, headers=headers)
        res_soup = BeautifulSoup(res.text, 'html.parser')
        company_soup = res_soup.select('h2.b-tit a')

        # 取得新url並再次請求
        for article in company_soup:
            article_title = article.text
            article_url = article['href'].replace('//', 'https://')
            article_json = 'https://www.104.com.tw/job/ajax/content/' + article_url.split('/')[-1]

            # 設定新headers
            headers_j = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
                'referer': article_url.split('?')[0]
            }
            res_article = requests.get(article_json, headers=headers_j)

            job_content = json.loads(res_article.text)
            job_name = job_content['data']['header']['jobName']
            jobs.append(job_name)

            compamy_name = job_content['data']['header']['custName']
            companies.append(compamy_name)

            company_104url = job_content['data']['header']['custUrl']
            company_104urls.append(company_104url)

            analys_url = job_content['data']['header']['analysisUrl'].replace('//', 'http://')
            analys_urls.append(analys_url)

            edu = str(job_content['data']['condition']['edu']) + ' // ' + str(
                job_content['data']['condition']['major']).strip('[]')
            edus.append(edu)

            job_desc = job_content['data']['jobDetail']['jobDescription']
            job_descs.append(job_desc)

            skill_1 = list(job_content['data']['condition']['specialty'])
            skill_2 = list(job_content['data']['condition']['skill'])
            skill_3 = job_content['data']['condition']['other']
            skills.append(skill_1)
            skills.append(skill_2)
            skills.append(skill_3)
            skills.append(job_desc)

            address = job_content['data']['jobDetail']['addressRegion'] + job_content['data']['jobDetail'][
                'addressDetail']
            addresses.append(address)

            salary = job_content['data']['jobDetail']['salary']
            salaries.append(salary)

            columns = ['職稱', '公司', '學歷', '地址', '職務內容', '104的url', '104分析']
            df = pd.DataFrame(columns=columns)
            df['職稱'] = jobs
            df['公司'] = companies
            df['學歷'] = edus
            df['地址'] = addresses
            df['薪資'] = salaries
            df['職務內容'] = job_descs
            df['104的url'] = company_104urls
            df['104分析'] = analys_urls
            for i in skills:
                aa = jieba.cut(str(i))
                skill_count = {'Python': 0, 'SQL': 0, 'MongoDB': 0, 'Linux': 0, 'Docker': 0, 'Java': 0,
                               'JavaScript': 0, 'AI': 0, 'Redis': 0, 'RESTful': 0, "統計": 0, 'Machine learning': 0,
                               '深度學習': 0, '爬蟲': 0, 'Flask': 0}
                for bb in aa:
                    if bb in skill_count:
                        skill_count[bb] = 1
                    else:
                        # skill_count[bb] = 0
                        pass
            
                values = str(skill_count.values()).strip('dict_values([').strip('])').split(', ')
            df_1_list.append(values)
            df_score = pd.DataFrame(np.reshape(df_1_list, (-1, 15), order='C'), dtype=np.int)
            df_score.columns = ['Python', 'SQL', 'MongoDB', 'Linux', 'Docker', 'Java', 'JavaScript', 'AI', 'Redis',
                                'RESTful', "統計", 'Machine learning', '深度學習', '爬蟲', 'Flask']

            df_all = pd.concat([df, df_score], axis=1)
            df_all = df
            df_all.drop_duplicates('104的url', 'first', inplace=True)
            df_all = df_all.reset_index(drop=True)
            df_all.to_excel(writer, sheet_name='104爬蟲資料', encoding='utf-8-sig')

            df_2 = pd.Series.sum(df_score)
            df_2.name = '統計次數'
            df_2.to_excel(writer, sheet_name='統計資料', header=True, encoding='utf-8-sig')
            writer.save()
#                 writer.close()
    return df_all

    


if __name__ == "__main__":
    #令使用者可設定爬蟲關鍵資料
    query = str(input('設定搜尋關鍵詞:'))
    days = str(input('設定爬取幾日內更新資料:'))
    pages = int(input('設定爬取頁數:'))
    filename = str(input('設定儲存檔名:jobs_'))
    a = find_jobs_104(query,days,pages,filename)
    print(a)
