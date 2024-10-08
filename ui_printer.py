import socket
import datetime
import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv


# 从环境变量中获取打印机的 IP 和端口
load_dotenv()
printer_ip_env = os.environ.get("PRINTER_IP", "")
printer_port_env = os.environ.get("PRINTER_PORT", "9100")  # 设置默认端口为 9100
qr_x = os.environ.get("QR_CODE_X", "") 
qr_y = os.environ.get("QR_CODE_Y", "")
width = os.environ.get("WIDTH", "310")
height = os.environ.get("HEIGH", "230") 
# 发送打印命令的函数
def send_print_command(printer_ip, printer_port, case_no, num_copies):
    try:
        # 构建 ZPL 指令
        zpl = f"""
        ^XA
        ^PQ{num_copies},0,1,Y,N
        ^PW{width}
        ^LL{height}
        ^LH0,0

        ^FO60,30^A0N,45,45^FD{datetime.datetime.now().strftime('%b-%d')}^FS

        ^FO{qr_x},{qr_y}^BQN,2,3^FDQA,{case_no}^FS

        ^FO0,175^A0N,50,35^FD{case_no[3:]}^FS
        ^XZ
        """
        
        # 发送打印命令
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((printer_ip, int(printer_port)))
            s.sendall(zpl.encode('utf-8'))
            messagebox.showinfo("Success", "Print command sent successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to the printer: {e}")

# 提交按钮的回调函数
def on_submit():
    printer_ip = ip_entry.get()
    printer_port = port_entry.get()
    case_no = case_no_entry.get()
    num_copies = num_copies_entry.get()

    # 验证输入
    if not case_no:
        messagebox.showerror("Error", "Case NO cannot be empty.")
        return

    try:
        num_copies = int(num_copies)
        if num_copies < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Number of copies must be a positive integer.")
        return

    # 发送打印命令
    send_print_command(printer_ip, printer_port, case_no, num_copies)

# 回车键绑定事件处理器
def case_no_enter(event):
    num_copies_entry.focus()  # 聚焦到副本数量输入框

# 输入数量后的回车键事件处理器
def num_copies_enter(event):
    on_submit()  # 调用提交函数

# 创建 GUI 窗口
root = tk.Tk()
root.title("Zebra Printer Interface")

# 创建标签和输入框
tk.Label(root, text="Printer IP:").grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)
ip_entry.insert(0, printer_ip_env)  # 从环境变量读取 IP 并作为默认值

tk.Label(root, text="Printer Port:").grid(row=1, column=0, padx=10, pady=10)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=10, pady=10)
port_entry.insert(0, printer_port_env)  # 从环境变量读取端口并作为默认值

tk.Label(root, text="Case NO:").grid(row=2, column=0, padx=10, pady=10)
case_no_entry = tk.Entry(root)
case_no_entry.grid(row=2, column=1, padx=10, pady=10)
case_no_entry.bind("<Return>", case_no_enter)  # 绑定回车事件

tk.Label(root, text="Number of Copies:").grid(row=3, column=0, padx=10, pady=10)
num_copies_entry = tk.Entry(root)
num_copies_entry.grid(row=3, column=1, padx=10, pady=10)
num_copies_entry.bind("<Return>", num_copies_enter)  # 绑定回车事件

# 创建提交按钮
submit_button = tk.Button(root, text="Print", command=on_submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# 运行 GUI 主循环
root.mainloop()
