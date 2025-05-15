import socket
import datetime
import tkinter as tk
from tkinter import messagebox, font, ttk
import os
from dotenv import load_dotenv

# 从环境变量中加载配置
load_dotenv()
printer_ip = os.environ.get("PRINTER_IP", "")
printer_port = int(os.environ.get("PRINTER_PORT", "9100"))

# 安全地获取整数环境变量，处理空字符串情况
def safe_get_int(key, default):
    value = os.environ.get(key, str(default))
    return int(value) if value.strip() else default

qr_x = safe_get_int("QR_CODE_X", 100)
qr_y = safe_get_int("QR_CODE_Y", 80)
width = safe_get_int("WIDTH", 310)
height = safe_get_int("HEIGHT", 230)

# 发送打印命令的函数
def send_print_command(case_no, num_copies):
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
            s.connect((printer_ip, printer_port))
            s.sendall(zpl.encode('utf-8'))
            messagebox.showinfo("Success", "Print command sent successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to the printer: {e}")

# 提交按钮的回调函数
def on_submit():
    # 获取输入并清除空格
    case_no = case_no_entry.get().strip()
    num_copies = num_copies_entry.get().strip()
    
    # 更新输入框显示（去除空格后的值）
    case_no_entry.delete(0, tk.END)
    case_no_entry.insert(0, case_no)
    
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

    # 按钮动画效果
    submit_button.config(state=tk.DISABLED)
    root.update()
    
    # 发送打印命令
    send_print_command(case_no, num_copies)
    
    # 恢复按钮
    submit_button.config(state=tk.NORMAL)
    
    # 清空和聚焦到Case NO输入框，为下一次打印准备
    case_no_entry.delete(0, tk.END)
    case_no_entry.focus()

# 实时去除输入的空格
def validate_case_no(event=None):
    current = case_no_entry.get()
    if " " in current:
        stripped = current.replace(" ", "")
        case_no_entry.delete(0, tk.END)
        case_no_entry.insert(0, stripped)
    return True

# 回车键事件处理
def case_no_enter(event):
    num_copies_entry.focus()

def num_copies_enter(event):
    on_submit()

# 窗口置顶状态切换
def toggle_topmost():
    is_top = root.attributes("-topmost")
    new_state = not is_top
    root.attributes("-topmost", new_state)
    
    # 更新订书钉按钮外观
    if new_state:
        pin_button.config(text="📌", style="Pinned.TButton")
    else:
        pin_button.config(text="📍", style="Unpinned.TButton")

# 创建精美现代的UI
def create_ui():
    global case_no_entry, num_copies_entry, root, pin_button, submit_button
    
    # 创建主窗口
    root = tk.Tk()
    root.title("QR Code Printer")
    
    # 设置窗口大小和居中
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 设置窗口最小尺寸
    root.minsize(350, 270)
    
    # 设置窗口内边距
    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 配置样式
    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 11))
    style.configure("TEntry", font=("Segoe UI", 11))
    style.configure("TButton", font=("Segoe UI", 11))
    
    # 订书钉按钮样式
    style.configure("Pinned.TButton", foreground="black", background="#ffcccc")
    style.configure("Unpinned.TButton", foreground="black", background="#f0f0f0")
    
    # 打印按钮样式
    style.configure("Print.TButton", font=("Segoe UI", 12, "bold"))
    
    # 标题样式
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
    
    # IP地址样式
    style.configure("IP.TLabel", font=("Segoe UI", 12, "bold"))
    
    # 作者信息样式
    style.configure("Author.TLabel", font=("Segoe UI", 9), foreground="#666666")
    
    # 创建标题和打印机信息框架
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 15))
    
    # 标题区域显示"Printer IP: [ip地址]"
    title_label = ttk.Label(header_frame, text="Printer IP:", 
                          style="Title.TLabel")
    title_label.pack(side=tk.LEFT)
    
    ip_label = ttk.Label(header_frame, text=printer_ip, 
                       style="IP.TLabel")
    ip_label.pack(side=tk.LEFT, padx=(5, 0))
    
    # 订书钉按钮放在右侧
    pin_button = ttk.Button(header_frame, text="📍", width=3,
                          style="Unpinned.TButton", command=toggle_topmost)
    pin_button.pack(side=tk.RIGHT)
    
    # 创建输入框架
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=5)
    
    # Case NO 输入
    case_no_label = ttk.Label(input_frame, text="Case NO:")
    case_no_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=8)
    
    case_no_entry = ttk.Entry(input_frame, width=25)
    case_no_entry.grid(row=0, column=1, sticky="ew", pady=8)
    case_no_entry.bind("<Return>", case_no_enter)
    case_no_entry.bind("<KeyRelease>", validate_case_no)
    
    # Number of Copies 输入
    copies_label = ttk.Label(input_frame, text="Copies:")
    copies_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
    
    num_copies_entry = ttk.Entry(input_frame, width=25)
    num_copies_entry.grid(row=1, column=1, sticky="ew", pady=8)
    num_copies_entry.insert(0, "1")
    num_copies_entry.bind("<Return>", num_copies_enter)
    
    # 列权重配置
    input_frame.columnconfigure(1, weight=1)
    
    # 打印按钮
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=15)
    
    submit_button = ttk.Button(button_frame, text="Print", 
                             style="Print.TButton", command=on_submit)
    submit_button.pack(pady=5, ipadx=10, ipady=5)
    
    # 底部状态栏
    status_frame = ttk.Frame(main_frame)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(15, 0))
    
    # 添加作者信息
    author_label = ttk.Label(status_frame, text="Created by Devin.Zhao",
                           style="Author.TLabel")
    author_label.pack(side=tk.LEFT)
    
    # 添加应用名称和版本信息
    app_version = ttk.Label(status_frame, text="QR Code Printer v1.1", 
                          style="Author.TLabel")
    app_version.pack(side=tk.RIGHT)
    
    # 设置初始焦点
    case_no_entry.focus()
    
    return root

# 主程序入口
if __name__ == "__main__":
    root = create_ui()
    root.mainloop()