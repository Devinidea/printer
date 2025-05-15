import socket
import datetime
import tkinter as tk
from tkinter import messagebox, font, ttk
import os
from dotenv import load_dotenv

<<<<<<< HEAD
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
=======
# 从环境变量中获取打印机的 IP 和端口
load_dotenv()
printer_ip_env = os.environ.get("PRINTER_IP", "")
printer_port_env = os.environ.get("PRINTER_PORT", "9100")  # 默认端口为 9100
qr_x = os.environ.get("QR_CODE_X", "50") 
qr_y = os.environ.get("QR_CODE_Y", "50")
width = os.environ.get("WIDTH", "310")
height = os.environ.get("HEIGHT", "230")

# 全局变量控制窗口置顶状态
is_always_on_top = False
>>>>>>> 243f71ec9538635b018bf5e6f4b6ac53cd97f5ea

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
<<<<<<< HEAD
            s.connect((printer_ip, printer_port))
            s.sendall(zpl.encode('utf-8'))
            messagebox.showinfo("Success", "Print command sent successfully.")
=======
            s.settimeout(5)  # 超时5秒
            s.connect((printer_ip, int(printer_port)))
            s.sendall(zpl.encode('ascii'))
            print("Print command sent successfully.")
            # messagebox.showinfo("Success", "Print command sent successfully.")
            clear_inputs()  # 打印成功后清空输入框
>>>>>>> 243f71ec9538635b018bf5e6f4b6ac53cd97f5ea
    except Exception as e:
        print(f"Error: {e}")
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

<<<<<<< HEAD
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
=======
# 切换窗口置顶状态的函数
def toggle_always_on_top():
    global is_always_on_top
    is_always_on_top = not is_always_on_top
    root.attributes('-topmost', is_always_on_top)
    always_on_top_button.config(text="Always on Top: ON" if is_always_on_top else "Always on Top: OFF")

# 清空输入框的函数
def clear_inputs():
    case_no_entry.delete(0, tk.END)
    num_copies_entry.delete(0, tk.END)
    case_no_entry.focus()  # 聚焦到 Case NO 输入框

# 创建 GUI 窗口
root = tk.Tk()
root.title("Zebra Printer Interface")
>>>>>>> 243f71ec9538635b018bf5e6f4b6ac53cd97f5ea

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

<<<<<<< HEAD
# 主程序入口
if __name__ == "__main__":
    root = create_ui()
    root.mainloop()
=======
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

# 创建置顶窗口按钮
always_on_top_button = tk.Button(root, text="Always on Top: OFF", command=toggle_always_on_top)
always_on_top_button.grid(row=5, column=0, columnspan=2, pady=10)

# 运行 GUI 主循环
root.mainloop()
>>>>>>> 243f71ec9538635b018bf5e6f4b6ac53cd97f5ea
