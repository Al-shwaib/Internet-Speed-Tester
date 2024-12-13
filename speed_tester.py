import socket
import time
import threading
from datetime import datetime
import json
import os
import requests
from urllib.parse import urlparse

class SpeedTester:
    def __init__(self):
        self.test_servers = [
            'https://speed.cloudflare.com/__down?bytes=25000000',  # 25MB test file
            'https://speed.hetzner.de/100MB.bin',                  # 100MB test file
            'https://proof.ovh.net/files/100Mb.dat'                # 100MB test file
        ]
        self.upload_servers = [
            'https://httpbin.org/post',
            'https://postman-echo.com/post'
        ]
        self.results = {
            'download': 0,
            'upload': 0,
            'ping': 0,
            'timestamp': None
        }
        self.history_file = 'speed_history.json'
        self.chunk_size = 8192
        self.test_duration = 10  # seconds

    def measure_ping(self, url):
        """Measure response time (ping) for a specific server"""
        try:
            domain = urlparse(url).netloc
            start_time = time.time()
            socket.gethostbyname(domain)
            end_time = time.time()
            return (end_time - start_time) * 1000
        except:
            return None

    def average_ping(self):
        """Calculate average response time"""
        pings = []
        for url in self.test_servers:
            ping_time = self.measure_ping(url)
            if ping_time is not None:
                pings.append(ping_time)
        return sum(pings) / len(pings) if pings else 0

    def measure_download_speed(self, url):
        """Measure download speed from a specific server"""
        try:
            start_time = time.time()
            downloaded = 0
            response = requests.get(url, stream=True, timeout=30)
            
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    downloaded += len(chunk)
                    current_time = time.time()
                    if current_time - start_time >= self.test_duration:
                        break

            duration = time.time() - start_time
            speed_bps = (downloaded * 8) / duration
            speed_mbps = speed_bps / (1024 * 1024)
            
            return speed_mbps
        except Exception as e:
            print(f"Error measuring download speed: {str(e)}")
            return 0

    def measure_upload_speed(self, url):
        """Measure upload speed to a specific server"""
        try:
            # Create data for upload (10MB)
            data = b'0' * (10 * 1024 * 1024)
            
            start_time = time.time()
            response = requests.post(url, data=data, timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                uploaded_bytes = len(data)
                speed_bps = (uploaded_bytes * 8) / duration
                speed_mbps = speed_bps / (1024 * 1024)
                return speed_mbps
            return 0
        except:
            return 0

    def run_speed_test(self, callback=None):
        """Run complete speed test"""
        try:
            # Measure response time
            ping = self.average_ping()
            if callback:
                callback('ping', ping)

            # Measure download speed
            download_speeds = []
            for url in self.test_servers:
                speed = self.measure_download_speed(url)
                if speed > 0:
                    download_speeds.append(speed)
                if callback:
                    callback('download_progress', speed)
            
            avg_download = max(download_speeds) if download_speeds else 0
            if callback:
                callback('download', avg_download)

            # Measure upload speed
            upload_speeds = []
            for url in self.upload_servers:
                speed = self.measure_upload_speed(url)
                if speed > 0:
                    upload_speeds.append(speed)
                if callback:
                    callback('upload_progress', speed)
            
            avg_upload = max(upload_speeds) if upload_speeds else 0
            if callback:
                callback('upload', avg_upload)

            # Save results
            self.results = {
                'download': avg_download,
                'upload': avg_upload,
                'ping': ping,
                'timestamp': datetime.now().isoformat()
            }
            
            self.save_results()
            return self.results
            
        except Exception as e:
            print(f"Error during speed test: {str(e)}")
            return None

    def save_results(self):
        """Save test results"""
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            except:
                history = []
        
        history.append(self.results)
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f)

    def get_history(self):
        """Retrieve test history"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def run_async(self, callback=None):
        """Run test asynchronously"""
        thread = threading.Thread(target=self.run_speed_test, args=(callback,))
        thread.daemon = True
        thread.start()
        return thread
