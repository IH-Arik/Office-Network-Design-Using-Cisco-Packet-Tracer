#!/usr/bin/env python3
"""
Packet Tracer Configuration Extractor
This script helps extract network configurations from Packet Tracer files
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class PacketTracerExtractor:
    def __init__(self, pkt_file_path):
        self.pkt_file = pkt_file_path
        self.output_dir = Path("extracted_configs")
        self.output_dir.mkdir(exist_ok=True)
    
    def extract_device_configs(self):
        """
        Extract device configurations from Packet Tracer file
        Note: This requires Packet Tracer to be installed and accessible
        """
        print(f"Extracting configurations from: {self.pkt_file}")
        
        # Check if Packet Tracer is installed
        pt_path = self.find_packet_tracer()
        if not pt_path:
            print("Packet Tracer not found. Please install Packet Tracer first.")
            return False
        
        print(f"Found Packet Tracer at: {pt_path}")
        
        # Method 1: Try to use Packet Tracer CLI (if available)
        try:
            self.extract_via_cli(pt_path)
        except Exception as e:
            print(f"CLI extraction failed: {e}")
            print("Please use manual extraction method.")
            self.show_manual_instructions()
    
    def find_packet_tracer(self):
        """Find Packet Tracer installation"""
        common_paths = [
            "C:/Program Files/Cisco Packet Tracer/bin/PacketTracer.exe",
            "C:/Program Files (x86)/Cisco Packet Tracer/bin/PacketTracer.exe",
            "C:/Cisco Packet Tracer/bin/PacketTracer.exe"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        return None
    
    def extract_via_cli(self, pt_path):
        """Extract using Packet Tracer command line"""
        # Note: Packet Tracer CLI support may be limited
        cmd = [
            pt_path,
            "-open", self.pkt_file,
            "-export", str(self.output_dir)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("Successfully exported configurations")
                return True
            else:
                print(f"Export failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"CLI extraction error: {e}")
            return False
    
    def show_manual_instructions(self):
        """Show manual extraction instructions"""
        print("\n" + "="*60)
        print("MANUAL EXTRACTION INSTRUCTIONS")
        print("="*60)
        print("\n1. Open Packet Tracer")
        print("2. Open your .pkt file")
        print("3. For each device:")
        print("   - Click on the device")
        print("   - Go to CLI tab")
        print("   - Type 'enable'")
        print("   - Type 'show running-config'")
        print("   - Copy the configuration")
        print("   - Save to a text file")
        print("\n4. Save all configurations in the 'extracted_configs' folder")
        print("\n5. Run this script again to organize the configurations")
        print("="*60)
    
    def organize_configs(self):
        """Organize extracted configurations"""
        config_dir = Path("extracted_configs")
        if not config_dir.exists():
            print("No extracted_configs directory found.")
            return
        
        # Create organized structure
        dirs = ["routers", "switches", "servers", "wireless"]
        for dir_name in dirs:
            (config_dir / dir_name).mkdir(exist_ok=True)
        
        print("Configuration organization complete!")
        print(f"Check the '{config_dir}' directory for organized configs.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract-config.py <path_to_pkt_file>")
        sys.exit(1)
    
    pkt_file = sys.argv[1]
    if not os.path.exists(pkt_file):
        print(f"File not found: {pkt_file}")
        sys.exit(1)
    
    extractor = PacketTracerExtractor(pkt_file)
    extractor.extract_device_configs()
    
    # Try to organize if configs already exist
    if Path("extracted_configs").exists():
        extractor.organize_configs()

if __name__ == "__main__":
    main()
