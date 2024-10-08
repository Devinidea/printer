import socket
import datetime

# Zebra 打印机的 IP 地址和端口
printer_ip = "10.192.1.183"
printer_port = 9100

while True:
    try:
        # 获取当前日期
        current_date = datetime.datetime.now().strftime('%b-%d')

        # 用户输入二维码内容
        qr_content = input("Please provide Case NO (or type 'exit' to quit): ")
        
        if qr_content.lower() == 'exit':
            print("Exiting the program.")
            break

        num_copies = input("How many copies? ")

        # 输入验证
        try:
            num_copies = int(num_copies)
            if num_copies < 1:
                raise ValueError("Number of copies must be at least 1.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue  # 回到循环开头

        # ZPL 命令
        zpl = f"""
        ^XA
        ^PQ{num_copies},0,1,Y,N
        ^PW300
        ^LL200 ; 
        ^LH0,0  ; 设置标签的左上角

        ; 当前日期的位置和大小（调整为更大的字体）
        ^FO60,30^A0N,45,45^FD{current_date}^FS  ; 打印当前日期，字体大小调整

        ; 二维码的位置和大小（调整缩放因子）
        ^FO90,40^BQN,2,3^FDQA,{qr_content}^FS  ; 打印二维码，缩放因子调整为 3

        ; 明文的位置和大小
        ^FO0,175^A0N,50,35^FD{qr_content[3:]}^FS  ; 打印二维码内容，保持原字体大小
        ^XZ
        """

        # 创建 socket 连接并发送 ZPL 命令
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((printer_ip, printer_port))
                s.sendall(zpl.encode('utf-8'))
                print("Print command sent successfully.")
        except Exception as e:
            print(f"Failed to connect to the printer: {e}")

    except KeyboardInterrupt:
        print("\nExiting the program.")
        break
