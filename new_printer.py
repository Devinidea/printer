import socket
import datetime
import os

# 从环境变量获取打印机的 IP 地址和端口号
# Zebra 打印机的 IP 地址和端口
default_ip = "10.192.1.183"
default_port = 9100

printer_ip = os.environ.get("PRINTER_IP", default_ip)  # "default_ip" 可以替换为默认值
printer_port = int(os.environ.get("PRINTER_PORT", default_port))  # 将端口转换为整数

def get_input(prompt, input_type=str):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            return 'exit'

        if input_type == int:
            # 验证是否为正整数
            try:
                user_input = int(user_input)
                if user_input < 1:
                    raise ValueError("Number of copies must be at least 1.")
                return user_input
            except ValueError:
                print("Invalid number, please try again.")
        else:
            # 对于 Case NO，不做验证，直接返回
            return user_input

while True:
    # 获取 Case NO 输入，不做验证
    qr_content = get_input("Please provide Case NO (or type 'exit' to quit): ", str)
    
    if qr_content == 'exit':
        print("Exiting the program.")
        break

    # 获取副本数量输入，验证为正整数
    num_copies = get_input("How many copies? ", int)

    # 构建 ZPL 指令
    zpl = f"""
    ^XA
    ^PQ{num_copies},0,1,Y,N
    ^PW300
    ^LL200
    ^LH0,0

    ^FO60,30^A0N,45,45^FD{datetime.datetime.now().strftime('%b-%d')}^FS

    ^FO90,40^BQN,2,3^FDQA,{qr_content}^FS

    ^FO0,175^A0N,50,35^FD{qr_content[3:]}^FS
    ^XZ
    """

    # 发送打印命令
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((printer_ip, printer_port))
            s.sendall(zpl.encode('utf-8'))
            print("Print command sent successfully.")
    except Exception as e:
        print(f"Failed to connect to the printer: {e}")
