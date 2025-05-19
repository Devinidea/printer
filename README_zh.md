# QR Code Printer Simulator for Zebra Printers

一个用于模拟 Zebra 标签打印机的 Python 应用程序，支持 ZPL 指令和 QR 码打印。专门针对 Zebra 工业标签打印机设计，完全兼容 ZPL 打印指令。

[English Documentation](README.md)

## 功能特点

- 模拟 Zebra 标签打印机（端口9100）
- 完整支持 ZPL 打印指令解析
- 现代化的 GUI 界面，基于 CustomTkinter
- QR 码标签打印功能
- 实时打印预览
- 可配置的打印参数
- 兼容 Zebra 打印机的标准网络协议

## 系统要求

- Python 3.6+
- Windows/Linux/MacOS
- 支持网络打印功能

## 依赖项

```bash
customtkinter>=5.2.0
python-dotenv>=1.0.0
```

## 安装

1. 克隆仓库：
```bash
git clone [repository-url]
cd printer-simulator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 复制 `.env-default` 为 `.env`
   - 根据需要修改配置参数

## 配置说明

在 `.env` 文件中可以配置以下参数：

- `PRINTER_IP`: 打印机 IP 地址（默认: 127.0.0.1）
- `PRINTER_PORT`: 打印机端口（默认: 9100，标准 Zebra 打印机端口）
- `QR_CODE_X`: QR 码 X 坐标位置（默认: 100）
- `QR_CODE_Y`: QR 码 Y 坐标位置（默认: 80）
- `WIDTH`: 标签宽度，单位点数（默认: 320，相当于 203 DPI 下的 40mm）
- `HEIGHT`: 标签高度，单位点数（默认: 240，相当于 203 DPI 下的 30mm）

注意：本模拟器专门用于测试 40mm × 30mm 规格的标签打印。

### DPI 与点数换算

对于 40mm × 30mm 的标签尺寸，使用以下换算表：

| 打印机 DPI | 宽度（40mm）              | 高度（30mm）              |
|----------|--------------------------|--------------------------|
| 203 DPI  | 40 × 8 = **~320 点**    | 30 × 8 = **~240 点**    |
| 300 DPI  | 40 × 11.81 = **~472 点** | 30 × 11.81 = **~354 点** |
| 600 DPI  | 40 × 23.62 = **~945 点** | 30 × 23.62 = **~709 点** |

换算公式：
- 203 DPI：毫米 × 8
- 300 DPI：毫米 × 11.81
- 600 DPI：毫米 × 23.62

默认配置使用 203 DPI（8 点/毫米），这是标准 Zebra 打印机常用的分辨率。

## 使用方法

1. 启动打印机模拟器：
```bash
python printer_simulator.py
```

2. 启动 GUI 界面：
```bash
python customtk_ui.py
```

3. 在 GUI 界面中：
   - 输入 Case Number
   - 设置打印份数
   - 点击打印按钮

## 主要特性

- 实时 ZPL 指令解析
- 多线程处理打印请求
- 现代化的 GUI 设计
- 支持窗口置顶功能
- 错误处理和用户反馈
- 可配置的打印参数
- 完全兼容 Zebra 打印机的 ZPL 指令集

## 支持的 Zebra 打印机型号

本模拟器支持所有使用 ZPL 指令的 Zebra 打印机，包括但不限于：
- ZT 系列（ZT230、ZT410、ZT420 等）
- ZM 系列（ZM400、ZM600 等）
- GX 系列（GX420d、GX430t 等）
- 其他支持 ZPL 的 Zebra 打印机型号

## 开发者信息

- 作者: Devin.Zhao
- 版本: v2.0

## 许可证

本项目采用自定义许可证，主要规定：
- 允许免费使用、复制、修改和分发用于个人或非商业目的
- 允许在获得作者书面同意后进行商业使用
- 商业使用将签订单独的商业许可协议
详见 [LICENSE](LICENSE) 文件。 