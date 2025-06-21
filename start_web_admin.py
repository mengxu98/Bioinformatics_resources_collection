#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bioinformatics Resources Collection - Web Admin Interface Startup Script
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if Python dependencies are installed"""
    try:
        import flask
        import yaml
        import requests
        import bs4
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run the following command to install dependencies:")
        print("pip install -r requirements-web.txt")
        return False

def check_config_files():
    """Check if configuration files exist"""
    config_files = [
        'config/articles.yaml',
        'config/methods.yaml', 
        'config/books.yaml',
        'config/blogs.yaml',
        'config/databases.yaml',
        'config/labs.yaml'
    ]
    
    missing_files = []
    for file_path in config_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("✗ Missing configuration files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        print("\nPlease make sure you are running this script from the correct project root directory")
        return False
    else:
        print("✓ All configuration files exist")
        return True

def main():
    print("Bioinformatics Resources Web Admin Interface Startup Script")
    print("=" * 50)
    
    # Check dependencies
    if not check_requirements():
        sys.exit(1)
    
    # Check configuration files
    if not check_config_files():
        sys.exit(1)
    
    # Check templates directory
    if not os.path.exists('templates'):
        print("✗ Missing templates directory")
        sys.exit(1)
    else:
        print("✓ Templates directory exists")
    
    print("\n" + "=" * 50)
    print("Starting Web Admin Interface...")
    print("Access URL: http://localhost:5001")
    print("Press Ctrl+C to stop the service")
    print("=" * 50 + "\n")
    
    # Start Flask application
    try:
        from web_admin import app
        app.run(debug=True, host='0.0.0.0', port=5001)
    except ImportError:
        print("✗ Cannot import web_admin module, please ensure web_admin.py file exists")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nService stopped")
        sys.exit(0)

if __name__ == '__main__':
    main() 