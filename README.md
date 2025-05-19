# QR Code Printer Simulator for Zebra Printers

A Python-based simulator for Zebra label printers, supporting ZPL commands and QR code printing. Specifically designed for Zebra industrial label printers with full ZPL command compatibility.

[中文文档](README_zh.md)

## Features

- Simulates Zebra label printers (port 9100)
- Full ZPL command parsing support
- Modern GUI interface based on CustomTkinter
- QR code label printing functionality
- Real-time print preview
- Configurable printing parameters
- Compatible with Zebra printer network protocols

## System Requirements

- Python 3.6+
- Windows/Linux/MacOS
- Network printing support

## Dependencies

```bash
customtkinter>=5.2.0
python-dotenv>=1.0.0
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd printer-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env-default` to `.env`
   - Modify parameters as needed

## Configuration

Configure the following parameters in the `.env` file:

- `PRINTER_IP`: Printer IP address (default: 127.0.0.1)
- `PRINTER_PORT`: Printer port (default: 9100, standard Zebra printer port)
- `QR_CODE_X`: QR code X coordinate position (default: 100)
- `QR_CODE_Y`: QR code Y coordinate position (default: 80)
- `WIDTH`: Label width in dots (default: 320, equivalent to 40mm at 203 DPI)
- `HEIGHT`: Label height in dots (default: 240, equivalent to 30mm at 203 DPI)

Note: This simulator is specifically designed for testing labels with dimensions of 40mm × 30mm.

### DPI to Dots Conversion

For label dimensions of 40mm × 30mm, use the following conversion table:

| Printer DPI | Width (40mm)              | Height (30mm)              |
|------------|---------------------------|---------------------------|
| 203 DPI    | 40 × 8 = **~320 dots**   | 30 × 8 = **~240 dots**   |
| 300 DPI    | 40 × 11.81 = **~472 dots** | 30 × 11.81 = **~354 dots** |
| 600 DPI    | 40 × 23.62 = **~945 dots** | 30 × 23.62 = **~709 dots** |

Conversion formula:
- For 203 DPI: millimeters × 8
- For 300 DPI: millimeters × 11.81
- For 600 DPI: millimeters × 23.62

The default configuration uses 203 DPI (8 dots/mm), which is common in standard Zebra printers.

## Usage

1. Start the printer simulator:
```bash
python printer_simulator.py
```

2. Launch the GUI interface:
```bash
python customtk_ui.py
```

3. In the GUI interface:
   - Enter Case Number
   - Set number of copies
   - Click the Print button

## Key Features

- Real-time ZPL command parsing
- Multi-threaded print request handling
- Modern GUI design
- Window pin functionality
- Error handling and user feedback
- Configurable printing parameters
- Full compatibility with Zebra printer ZPL command set

## Supported Zebra Printer Models

This simulator supports all Zebra printers that use ZPL commands, including but not limited to:
- ZT Series (ZT230, ZT410, ZT420, etc.)
- ZM Series (ZM400, ZM600, etc.)
- GX Series (GX420d, GX430t, etc.)
- Other Zebra printer models supporting ZPL

## Developer Information

- Author: Devin.Zhao
- Version: v2.0

## License

This project uses a custom license with the following main terms:
- Free use, copying, modification, and distribution for personal or non-commercial purposes
- Commercial use allowed with written permission from the author
- Commercial use requires a separate commercial license agreement
See [LICENSE](LICENSE) file for details.