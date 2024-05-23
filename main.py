import getJvmData
import excelWriting
import csv
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
import datetime

#現在日付をYYYYMMDDで取得してStr型に変換
nowdate = datetime.datetime.now()
nowdate = nowdate.strftime('%Y%m%d')

# ポップアップウィンドウで日付を入力するがキャンセルボタンが押された場合終了する
date = sd.askstring('', '基準日付を入力してください。', initialvalue=nowdate)
if date == None:
    exit()

# Rest of your code...
#キーワードリストを格納するリスト
keywordList = []

#csvモジュールを使ってCSVファイルから1行ずつ読み込む
with open('keywordList.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for keyword in reader:
        jvmDataList = getJvmData.get_jvn_info(keyword[1], date, keyword[2])
        if jvmDataList == -1:
            print('HTTPエラーが発生しました。')
            mb.showinfo('通知', 'HTTPエラーが発生しました。')
            break
        keywords = [[keyword[0]], [keyword[1]], [jvmDataList]]
        keywordList.append(keywords)

try:
    excelWriting.doExcelWriting(keywordList,date)
except Exception as e:
    print(e + 'エラーが発生しました。')
    mb.showinfo('通知', 'エラーが発生しました。')
    exit()

#ポップアップメッセージを表示
mb.showinfo('通知', '処理が終了しました。')

