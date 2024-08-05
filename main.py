import getJvmData
import excelWriting
import csv
import tkinter.messagebox as mb
import tkinter.simpledialog as sd
import datetime

nowdate = datetime.datetime.now()
nowdate = nowdate.strftime('%Y%m%d')

date = sd.askstring('', '基準日付を入力してください。', initialvalue=nowdate)
if date == None:
    exit()

#キーワードリストを格納するリスト
keywordList = []

#csvモジュールを使ってCSVファイルから1行ずつ読み込む
with open('keywordList.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for keyword in reader:
        try:
            jvmDataList = getJvmData.get_jvn_info(keyword[1], date, keyword[2])
        except Exception as e:
            print(e + '接続エラーが発生しました。')
            mb.showinfo('通知', '接続エラーが発生しました。')
            exit()
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

mb.showinfo('通知', '処理が終了しました。')

