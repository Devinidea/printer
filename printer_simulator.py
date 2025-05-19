import socket
import threading
import datetime

class PrinterSimulator:
    def __init__(self, host='127.0.0.1', port=9100):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.is_running = True
            print(f"打印机模拟器已启动在 {self.host}:{self.port}")
            
            while self.is_running:
                client_socket, address = self.server_socket.accept()
                print(f"接收到来自 {address} 的连接")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_thread.start()
        except Exception as e:
            print(f"启动模拟器时发生错误: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def stop(self):
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        print("打印机模拟器已停止")

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if data:
                print("\n收到打印指令:")
                print("=" * 50)
                print(data)
                print("=" * 50)
                self.parse_zpl(data)
        except Exception as e:
            print(f"处理客户端请求时发生错误: {e}")
        finally:
            client_socket.close()

    def parse_zpl(self, zpl):
        """解析ZPL指令并显示关键信息"""
        print("\n解析ZPL指令:")
        print("-" * 50)
        
        # 解析打印份数
        if "^PQ" in zpl:
            copies = zpl[zpl.find("^PQ")+3:].split(',')[0].strip()
            print(f"打印份数: {copies}")
        
        # 解析QR码内容
        if "FDQA," in zpl:
            qr_content = zpl[zpl.find("FDQA,")+5:].split('^')[0].strip()
            print(f"QR码内容: {qr_content}")
        
        # 解析日期
        current_date = datetime.datetime.now().strftime('%b-%d')
        if current_date in zpl:
            print(f"打印日期: {current_date}")
        
        print("-" * 50)

if __name__ == "__main__":
    simulator = PrinterSimulator()
    try:
        simulator.start()
    except KeyboardInterrupt:
        simulator.stop()
        print("\n程序已退出")