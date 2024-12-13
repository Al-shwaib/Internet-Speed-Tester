# Internet Speed Tester 

A modern, beautiful, and accurate internet speed testing application built with Python.

## Features 

- **Modern UI**: Built with CustomTkinter for a sleek, modern look
- **Accurate Measurements**: 
  - Download Speed Testing
  - Upload Speed Testing
  - Ping Measurement
  - Real servers testing (Cloudflare, Hetzner, OVH)
- **Real-time Progress**: Visual feedback during testing
- **History Tracking**: Keep track of your previous speed tests
- **Dark Mode**: Modern dark theme for better visibility
- **Responsive Design**: Resizable window that adapts to your screen

## Requirements 

- Python 3.8 or higher
- Required packages:
  ```
  customtkinter==5.2.0
  pillow==10.0.0
  requests==2.31.0
  ```

## Installation 

1. Clone the repository:
```bash
   git clone https://github.com/Al-shwaib/Internet-Speed-Tester.git
   cd internet-speed-tester
```

2. Install requirements:
```bash
   pip install -r requirements.txt
   ```

## Usage 

Run the application:
```bash
python main.py
```

## How It Works 

1. **Download Speed**: Tests download speed using multiple servers for accuracy
2. **Upload Speed**: Measures upload speed using reliable test endpoints
3. **Ping**: Calculates response time to various servers
4. **History**: Automatically saves test results for future reference

## Screenshots 

[Add screenshots of your application here]

## Contributing 

Feel free to contribute to this project:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License 

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 

- CustomTkinter for the modern UI components
- Speed test servers (Cloudflare, Hetzner, OVH) for providing test endpoints
