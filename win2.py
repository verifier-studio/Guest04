from ttkbootstrap import *
from ttkbootstrap.toast import ToastNotification
from tkinter import filedialog

import subprocess
import pyautogui

import json
import pyperclip

server_infos = []

app = Window(themename="pulse", position=(700, 200))
app.title('Guest04 v0.6.15 Turbo探索版')
# app.geometry('610x400')
app.resizable(False, False)

frm = Frame(app, padding=10)
frm.grid()

Label(frm, text='服务器IP').grid(row=0, column=0)
server_addr = Entry(frm)
server_addr.grid(row=1, column=0, padx=5)

Label(frm, text='SSH端口').grid(row=0, column=1)
server_port = Entry(frm)
server_port.grid(row=1, column=1, padx=5)

Label(frm, text='ROOT密码').grid(row=2, column=0)
root_pwd = Entry(frm)
root_pwd.grid(row=3, column=0, padx=5)

Label(frm, text='转发远程').grid(row=4, column=0)
remote_port = Entry(frm)
remote_port.grid(row=5, column=0, padx=5)

Label(frm, text='转发本地').grid(row=4, column=1)
local_port = Entry(frm)
local_port.grid(row=5, column=1, padx=5)

remote_port.insert(0, 3306)
local_port.insert(0, 6603)

def crtl(root_pwd_val):
    pyautogui.sleep(1)
    pyautogui.hotkey('win', 'up')
    pyperclip.copy(root_pwd_val)
    pyautogui.rightClick()
    pyautogui.press('enter')

def open_server():
    server_addr_val = server_addr.get()
    server_port_val = server_port.get()
    root_pwd_val = root_pwd.get()

    if server_addr_val =='' or server_port_val == '' or root_pwd_val == '':
        show_alert('前三空，填！')
        return

    command = 'ssh root@' + server_addr_val + ' -p ' + server_port_val
    # command = 'ps'
    tt = subprocess.Popen(["powershell", "-NoExit", "-Command", command], creationflags=subprocess.CREATE_NEW_CONSOLE)

    crtl(root_pwd_val)
Button(frm, text='打开终端', bootstyle=SUCCESS, command=open_server).grid(row=6, column=0, pady=10)

def connect_server():
    server_addr_val = server_addr.get()
    server_port_val = server_port.get()
    root_pwd_val = root_pwd.get()
    remote_port_val = remote_port.get()
    local_port_val = local_port.get()

    if server_addr_val =='' or server_port_val == '' or root_pwd_val == '' or remote_port_val == '' or local_port_val == '':
        show_alert('前五空，填！')
        return

    command = 'ssh -N -L ' + local_port_val + ':localhost:' + remote_port_val + ' root@' + server_addr_val + ' -p ' + server_port_val
    subprocess.Popen(["powershell", "-NoExit", "-Command", command], creationflags=subprocess.CREATE_NEW_CONSOLE)

    crtl(root_pwd_val)
Button(frm, text='建立通道', bootstyle=INFO, command=connect_server).grid(row=6, column=1, pady=10)

upload = LabelFrame(frm, text='文件上传', bootstyle=PRIMARY, width=200, height=100, padding=(80, 20))
upload.grid(row=7, column=0, columnspan=2, rowspan=2, pady=8)

# 文件上传
def upload_file():
    server_addr_val = server_addr.get()
    server_port_val = server_port.get()
    root_pwd_val = root_pwd.get()

    if server_addr_val =='' or server_port_val == '' or root_pwd_val == '':
        show_alert('前三空，填！')
        return

    selectFile = filedialog.askopenfilename()
    print(selectFile)
    if selectFile != None and selectFile != "":
        command = 'scp -P ' + server_port_val + ' ' + selectFile + ' root@' + server_addr_val + ':/root'
        subprocess.Popen(["powershell", "-Command", command], creationflags=subprocess.CREATE_NEW_CONSOLE)

        crtl(root_pwd_val)
Button(upload, text='选择文件', bootstyle=LIGHT, command=upload_file).grid()

def show_alert(msg):
    toast = ToastNotification(
        title="来自Guest04的提示",
        message=msg,
        duration=3000,
    )
    toast.show_toast()

def save_info():
    msg = '删除失败'

    server_addr_val = server_addr.get()
    server_port_val = server_port.get()
    root_pwd_val = root_pwd.get()
    remote_port_val = remote_port.get()
    local_port_val = local_port.get()
    server_remark_val = server_remark.get()

    if server_addr_val =='' or server_port_val == '' or root_pwd_val == '' or server_remark_val == '':
        show_alert('前三空 + 备注，填！')
        return

    new_server = {
        'ip': server_addr_val,
        'port': server_port_val,
        'passwd': root_pwd_val,
        'remote_port': remote_port_val,
        'local_port': local_port_val,
        'remark': server_remark_val
    }

    global server_infos
    print(server_infos)

    del_flag = server_remark_val[-3:]
    server_remark_val = server_remark_val.replace('-rf', '')
    print(del_flag)
    # return

    if len(server_infos) > 0: # 列表有数据，检查备注是否存在
        have = True
        for index, info in enumerate(server_infos):
            if info['remark'] == server_remark_val: # 已经存在
                if '-rf' == del_flag: # 删除
                    del server_infos[index]
                    msg = '删除成功'
                else: # 修改
                    server_infos[index]['ip'] = server_addr_val
                    server_infos[index]['port'] = server_port_val
                    server_infos[index]['passwd'] = root_pwd_val
                    server_infos[index]['remote_port'] = remote_port_val
                    server_infos[index]['local_port'] = local_port_val
                    server_infos[index]['remark'] = server_remark_val

                    msg = '更新成功'
                have = False
        if have and '-rf' != del_flag: # 新增
            msg = '保存成功'
            server_infos.append(new_server)                
    else: # 列表第一次保存
        if '-rf' != del_flag:
            msg = '保存成功'
            server_infos = [new_server]

    data = {
        'title': 'Guest04 Server Info',
        'server_infos': server_infos
    }
    with open('guest04.json', 'w') as f:
        json.dump(data, f)
        show_alert(msg)
    update_table()
Label(frm, text='备注').grid(row=15, column=0)
server_remark = Entry(frm)
server_remark.grid(row=16, column=0)
Button(frm, text='保存当前服务器信息', command=save_info).grid(row=16, column=1)

columns = ['ip_port', 'remark', 'ip', 'port', 'passwd', 'remote_port', 'local_port']
table = Treeview(frm, height=16, columns=columns, bootstyle=PRIMARY, show='headings', displaycolumns=('ip_port', 'remark'))
table.grid(row=0, column=2, padx=30, rowspan=15)

table.heading('ip_port', text='IP:PORT')
table.heading('remark', text='备注')

table.column('ip_port', width=140, minwidth=120)
table.column('remark', width=90, minwidth=80)

def update_table():
    table.delete(*table.get_children())

    try:
        with open("guest04.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # print(data['server_infos'])
            global server_infos
            server_infos = data['server_infos']

            for _, info in enumerate(server_infos):
                row = [info['ip'] + ':' + info['port'], info['remark'], info['ip'], info['port'], info['passwd'], info['remote_port'], info['local_port']]
                table.insert('', END, values=row)
    except:
        pass
update_table()

def get_row():
    foc = table.focus()

    if foc == '':
        show_alert('选！')
        return

    val = table.set(foc)

    server_addr.delete(0, END)
    server_addr.insert(0, val['ip'])
    server_port.delete(0, END)
    server_port.insert(0, val['port'])
    root_pwd.delete(0, END)
    root_pwd.insert(0, val['passwd'])
    remote_port.delete(0, END)
    remote_port.insert(0, val['remote_port'])
    local_port.delete(0, END)
    local_port.insert(0, val['local_port'])
    server_remark.delete(0, END)
    server_remark.insert(0, val['remark'])
Button(frm, text='加载/切换', bootstyle=DARK, command=get_row).grid(row=15, column=2)

Label(frm, text='Power By 海超人与大洋游侠®工作室！', bootstyle=SECONDARY).grid(row=16, column=2)

app.mainloop()