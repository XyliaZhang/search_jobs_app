from flask import Flask, request,render_template
import find_jobs_104
import find_jobs_1111
app = Flask(__name__, static_url_path="/static",static_folder="./static")

@app.route('/',methods=['GET','POST'])
def hello():
    welcom_str = """
    <html>
        <head>
            <title>jobs</title>
        </head>
        <body>
            <h1>歡迎進入search jobs app</h1>
            <form action='/search_jobs/result' method="POST">
                <h2>輸入相關條件後會到104及1111爬取資料。</h2>
                <label>設定搜尋關鍵詞:</label>
                <br>
                <input type="textbox" name="query">
                <br>
                <label>設定爬取幾日內更新資料:</label>
                <br>
                <input type="textbox" name="days">
                <br>
                <label>設定爬取頁數:</label>
                <br>
                <input type="textbox" name="pages">
                <br>
                <button type="submit">GO!</button>
            </form>
            """
    return welcom_str

@app.route('/search_jobs/result', methods=['POST'])
def result():
    query = request.form.get('query')
    days = request.form.get('days')
    pages = request.form.get('pages')
    a = find_jobs_104.find_jobs_104(query, days, pages)
    c = find_jobs_1111.find_jobs_1111(query, days, pages)

    m_1 = a.iloc[:,0].tolist()
    n_1 = a.iloc[:,1].tolist()
    o_1 = a.iloc[:,2].tolist()
    p_1 = a.iloc[:,3].tolist()
    q_1 = a.iloc[:,4].tolist()
    r_1 = a.iloc[:,5].tolist()
    s_1 = a.iloc[:,7].tolist()

    result = """
            <html>
                <body>
                    <h4>104結果：</h4>
                    <table border="5">
                        <tr>
                            <td>職稱</td>
                            <td>公司</td>
                            <td>學歷</td>
                            <td>地址</td>
                            <td>職務內容</td>
                            <td>104url</td>
                            <td>薪資</td>
                        </tr>
                        <tr>
                            <td>"""
    for i in range(len(m_1)):
        m = str(m_1[i])
        n = str(n_1[i])
        o = str(o_1[i])
        p = str(p_1[i])
        q = str(q_1[i])
        r = str(r_1[i])
        s = str(s_1[i])

        result += m
        result += "</td>  <td>"
        result += n
        result += "</td>  <td>"
        result += o
        result += "</td>  <td>"
        result += p
        result += "</td>  <td>"
        result += q
        result += "</td>  <td>"
        result += r
        result += "</td>  <td>"
        result += s
        result += "</td> </tr> <tr> <td>"
    result += "</td> <td> </td> </tr> </table> "
    result += """
                <h4>1111結果：</h4>
                    <table border="5">
                        <tr>
                            <td>職稱</td>
                            <td>公司</td>
                            <td>學歷</td>
                            <td>地址</td>
                            <td>職務內容</td>
                            <td>104url</td>
                            <td>薪資</td>
                        </tr>
                        <tr>
                            <td>"""
    m_2 = c.iloc[:, 0].tolist()
    n_2 = c.iloc[:, 1].tolist()
    o_2 = c.iloc[:, 2].tolist()
    p_2 = c.iloc[:, 3].tolist()
    q_2 = c.iloc[:, 5].tolist()
    r_2 = c.iloc[:, 6].tolist()
    s_2 = c.iloc[:, 4].tolist()

    for j in range(len(m_2)):
        M = str(m_2[j])
        N = str(n_2[j])
        O = str(o_2[j])
        P = str(p_2[j])
        Q = str(q_2[j])
        R = str(r_2[j])
        S = str(s_2[j])

        result += M
        result += "</td>  <td>"
        result += N
        result += "</td>  <td>"
        result += O
        result += "</td>  <td>"
        result += P
        result += "</td>  <td>"
        result += Q
        result += "</td>  <td>"
        result += R
        result += "</td>  <td>"
        result += S
        result += "</td> </tr> <tr> <td>"
    result += "</td> <td> </td> </tr> </table> </body> </html>"

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
