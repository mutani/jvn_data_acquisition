import requests

def get_jvn_info(keyword, date, url):
    #プロキシ設定追加
    proxieUser = 'user'
    proxiePass = 'pass'
    proxies = {
        'http': '',
        'https': '',
    }
    #プロキシ設定をtxtから読み込む
    with open('proxies.txt', 'r') as f:
        #http=を除去して代入
        proxies['http'] = f.readline().replace('http=', '').rstrip('\n')
        proxies['https'] = f.readline().replace('https=', '').rstrip('\n')
        proxieUser = f.readline().replace('user=', '').rstrip('\n')
        proxiePass = f.readline().replace('pass=', '').rstrip('\n')

    #戻り値の初期化
    jvmDataList = []
    #リクエスト送信
    response = requests.get(url, proxies=proxies, auth=(proxieUser, proxiePass))
    response.encoding = response.apparent_encoding
    if response.status_code != 200:
        #エラーが発生した場合は-1を返す
        return -1

    #件数を取得
    bodyStart = response.text.find('<td class="pager_count_class">') + 30
    bodyEnd = response.text.find('件中1', bodyStart)

    if bodyEnd == -1:
        #get_jvn_infoの戻り値を返す
        return [0]
    
    #int型に変換
    num = int(response.text[bodyStart:bodyEnd])
    count = 0
    for i in range(num):
        #レスポンスの中身にある<td align="center" nowrap="nowrap"><a href="から</tr>までの文字列を取得
        blockStart = response.text.find('<td align="center" nowrap="nowrap"><a href="', bodyEnd)
        blockend = response.text.find('</tr>', blockStart)
        blockStr = response.text[blockStart:blockend]
        #次のループのためにbodyEndを更新
        bodyEnd = blockend
        tdStart = 0
        dataList = []
        for i in range(6):
            # <td>から</td>までの文字列を取得し、listに保存
            if i == 0:
                tdStart = blockStr.find('>JVNDB-', tdStart) + 1
                tdEnd = blockStr.find('</a>', tdStart)
            elif i == 1:
                tdStart = blockStr.find('<td>', tdStart) + 4
                tdEnd = blockStr.find('</td>', tdStart)
            else:
                tdStart = blockStr.find('<td align="center" nowrap="nowrap">', tdStart) + 35
                tdEnd = blockStr.find('</td>', tdStart)

            tdContent = blockStr[tdStart:tdEnd]
            dataList.append(tdContent)
            #次のループのためにblockStartを更新
            tdStart = tdEnd

        jvmDataList.append(dataList)
    #戻り値を返す
    return jvmDataList


