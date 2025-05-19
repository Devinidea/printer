import customtkinter as ctk
import socket
import datetime
import os
from dotenv import load_dotenv

# 从环境变量中加载配置
def load_config():
    load_dotenv()
    config = {
        "printer_ip": os.getenv("PRINTER_IP", "127.0.0.1").strip('"'),
        "printer_port": int(os.getenv("PRINTER_PORT", "9100")),
        "qr_x": int(os.getenv("QR_CODE_X", "100")),
        "qr_y": int(os.getenv("QR_CODE_Y", "80")),
        "width": int(os.getenv("WIDTH", "310")),
        "height": int(os.getenv("HEIGHT", "230"))
    }
    return config

config = load_config()
printer_ip = config["printer_ip"]
printer_port = config["printer_port"]
qr_x = config["qr_x"]
qr_y = config["qr_y"]
width = config["width"]
height = config["height"]

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
            s.settimeout(5)  # 超时5秒
            s.connect((printer_ip, printer_port))
            s.sendall(zpl.encode('utf-8'))
            return True, "Print command sent successfully"
    except Exception as e:
        print(f"Error: {e}")
        return False, f"Failed to connect to printer: {e}"

class QRCodePrinter:
    def __init__(self):
        # 设置主题和外观
        ctk.set_appearance_mode("light")  # 默认使用浅色主题
        ctk.set_default_color_theme("blue")

        # 创建主窗口
        self.window = ctk.CTk()
        self.window.title("QR Code Printer")
        self.window.geometry("400x500")
        self.window.minsize(350, 450)

        # 窗口居中
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 500) // 2
        self.window.geometry(f"400x500+{x}+{y}")

        # 创建主框架
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 创建标题卡片
        self.title_card = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.title_card.pack(fill="x", pady=(0, 20))

        # 打印机信息
        self.printer_info_frame = ctk.CTkFrame(self.title_card, fg_color="transparent")
        self.printer_info_frame.pack(side="left", padx=15, pady=10)

        self.printer_icon = ctk.CTkLabel(
            self.printer_info_frame,
            text="🖨️",
            font=("Segoe UI", 24)
        )
        self.printer_icon.pack(side="left", padx=(0, 10))

        self.printer_text_frame = ctk.CTkFrame(self.printer_info_frame, fg_color="transparent")
        self.printer_text_frame.pack(side="left")

        self.title_label = ctk.CTkLabel(
            self.printer_text_frame,
            text="Printer Address",
            font=("Segoe UI", 14)
        )
        self.title_label.pack(anchor="w")

        self.ip_label = ctk.CTkLabel(
            self.printer_text_frame,
            text=printer_ip,
            font=("Segoe UI", 16, "bold")
        )
        self.ip_label.pack(anchor="w")

        # 置顶按钮
        self.is_top = False
        self.pin_button = ctk.CTkButton(
            self.title_card,
            text="📌",
            width=40,
            height=40,
            font=("Segoe UI", 18),
            command=self.toggle_top,
            fg_color="#D0D0D0",
            hover_color="#B0B0B0",
            border_width=1,
            border_color="#A0A0A0",
            text_color="black"
        )
        self.pin_button.pack(side="right", padx=15, pady=10)

        # 输入卡片
        self.input_card = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.input_card.pack(fill="x", pady=(0, 20))

        # Case NO 输入框
        self.case_no_frame = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.case_no_frame.pack(fill="x", padx=15, pady=(15, 5))

        self.case_no_label = ctk.CTkLabel(
            self.case_no_frame,
            text="Case Number",
            font=("Segoe UI", 14)
        )
        self.case_no_label.pack(anchor="w")

        self.case_no_entry = ctk.CTkEntry(
            self.case_no_frame,
            placeholder_text="Enter Case Number",
            font=("Segoe UI", 16),
            height=40
        )
        self.case_no_entry.pack(fill="x", pady=(5, 0))
        self.case_no_entry.bind("<Return>", lambda e: self.copies_entry.focus())
        self.case_no_entry.bind("<KeyRelease>", self.validate_case_no)

        # 打印份数输入框
        self.copies_frame = ctk.CTkFrame(self.input_card, fg_color="transparent")
        self.copies_frame.pack(fill="x", padx=15, pady=(5, 15))

        self.copies_label = ctk.CTkLabel(
            self.copies_frame,
            text="Copies",
            font=("Segoe UI", 14)
        )
        self.copies_label.pack(anchor="w")

        self.copies_entry = ctk.CTkEntry(
            self.copies_frame,
            placeholder_text="Enter number of copies",
            font=("Segoe UI", 16),
            height=40
        )
        self.copies_entry.pack(fill="x", pady=(5, 0))
        self.copies_entry.bind("<Return>", lambda e: self.print_clicked())

        # 打印按钮
        self.print_button = ctk.CTkButton(
            self.main_frame,
            text="🖨️ Print",
            font=("Segoe UI", 18, "bold"),
            height=50,
            command=self.print_clicked,
            fg_color="#3B8ED0",
            hover_color="#36719F"
        )
        self.print_button.pack(fill="x", pady=(0, 20))

        # 状态栏
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", side="bottom", pady=(20, 0))

        self.author_label = ctk.CTkLabel(
            self.status_frame,
            text="Created by Devin.Zhao",
            font=("Segoe UI", 12)
        )
        self.author_label.pack(side="left")

        self.version_label = ctk.CTkLabel(
            self.status_frame,
            text="QR Code Printer v2.0",
            font=("Segoe UI", 12)
        )
        self.version_label.pack(side="right")

    def validate_case_no(self, event=None):
        current = self.case_no_entry.get()
        if " " in current:
            stripped = current.replace(" ", "")
            self.case_no_entry.delete(0, "end")
            self.case_no_entry.insert(0, stripped)

    def toggle_top(self):
        self.is_top = not self.is_top
        self.window.attributes("-topmost", self.is_top)
        self.pin_button.configure(
            fg_color=("#3B8ED0" if self.is_top else "#D0D0D0"),
            text_color=("white" if self.is_top else "black"),
            hover_color=("#36719F" if self.is_top else "#B0B0B0"),
            border_color=("#36719F" if self.is_top else "#A0A0A0")
        )

    def show_message(self, message, is_error=False):
        message_frame = ctk.CTkFrame(
            self.window,
            fg_color=("#FF6B6B" if is_error else "#6BCB77")
        )
        message_frame.place(relx=0.5, rely=0.9, anchor="center")

        message_label = ctk.CTkLabel(
            message_frame,
            text=message,
            text_color="white",
            font=("Segoe UI", 14)
        )
        message_label.pack(padx=20, pady=10)

        # 2秒后自动消失
        self.window.after(2000, message_frame.destroy)

    def print_clicked(self):
        case_no = self.case_no_entry.get().strip()
        num_copies = self.copies_entry.get().strip()

        if not case_no:
            self.show_message("Case Number cannot be empty", True)
            self.case_no_entry.focus()
            return

        try:
            num_copies = int(num_copies)
            if num_copies < 1:
                raise ValueError
        except ValueError:
            self.show_message("Copies must be a positive integer", True)
            self.copies_entry.focus()
            return

        # 禁用打印按钮
        self.print_button.configure(state="disabled")

        # 发送打印命令
        success, message = send_print_command(case_no, num_copies)

        # 显示结果
        self.show_message(message, not success)

        # 恢复打印按钮
        self.print_button.configure(state="normal")

        if success:
            # 清空所有输入并聚焦到Case NO
            self.case_no_entry.delete(0, "end")
            self.copies_entry.delete(0, "end")
            self.case_no_entry.focus()

    def run(self):
        self.window.mainloop()

def main():
    app = QRCodePrinter()
    app.run()

if __name__ == "__main__":
    main()
