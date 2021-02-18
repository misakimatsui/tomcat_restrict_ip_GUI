from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import PySimpleGUI as sg

xml_file = './web.xml'


def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    copymode(file_path, abs_path)
    remove(file_path)
    move(abs_path, file_path)


def call_gui():
    data = open(xml_file, "r")

    is_ip_line = False
    pattern = ''
    allow_ip = []
    for i, line in enumerate(data):
        line = line.rstrip()
        line = line.lstrip()
        if is_ip_line:
            pattern = line
            arr = line.split('|')
            for j in range(1, len(arr) - 1):
                allow_ip.append(arr[j])
            data.close()
            break
        if line == "<param-name>allow</param-name>":
            is_ip_line = True

    # ファイルをクローズする
    #  セクション1 - オプションの設定と標準レイアウト
    sg.theme('Dark Blue 3')

    layout = [[sg.Text('許可中のIP')]]
    for ip in allow_ip:
        layout.append([sg.Text('     ' + ip, size=(15, 1)), sg.Checkbox('削除', default=False)])
    layout.append([sg.Text('許可するIP追加', size=(15, 1)), sg.InputText('')])
    layout.append([sg.Submit(button_text='実行ボタン')])
    # セクション 2 - ウィンドウの生成
    window = sg.Window('許可するIPを入力', layout)

    # セクション 3 - イベントループ
    while True:
        event, values = window.read()

        if event is None:
            break

        if event == '実行ボタン':
            print(values)
            subst = '<param-value>|'
            idx = 0
            for ip in allow_ip:
                if not values[idx]:
                    subst += (ip + '|')
                idx = idx + 1
            if values[idx] != '':
                print('in')
                subst += (values[idx] + '|')
            subst += '</param-value>'
            replace(xml_file, pattern, subst)
            show_message = '書き込み完了\n'
            show_message += 'サーバーを再起動してください'

            # ポップアップ
            sg.popup(show_message)
            window.close()

    # セクション 4 - ウィンドウの破棄と終了
    window.close()


if __name__ == '__main__':
    call_gui()

