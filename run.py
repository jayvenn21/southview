#!/usr/bin/env python3
"""
run.py — One-command launcher for the app.
1. Runs the CSV processing script
2. Starts a local HTTP server
3. Opens the app in your browser

Usage: python run.py
"""

import subprocess
import sys
import os
import time
import webbrowser
import http.server
import socketserver
import threading


CSV_SCRIPT   = "convert.py"
SERVER_PORT  = 3000
OPEN_PATH    = "/"


def print_step(msg):
    print(f"\n{'─'*50}")
    print(f"  {msg}")
    print(f"{'─'*50}")

def setup_mapbox_token():
    config_file = "config.js"
    if os.path.exists(config_file):
        print("  config.js already exists, skipping.")
        return

    print_step("Step 0: Mapbox Token Setup")
    print("  A Mapbox token is required to run this app.")
    print("  Copy this link into your browser to find your token at https://account.mapbox.com/\n")

    token = input("  Paste your Mapbox token here and press Enter: ").strip()

    if not token:
        print("\n  No token entered. Exiting.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    with open(config_file, "w") as f:
        f.write(f"var MAPBOX_ACCESS_TOKEN = '{token}';\n")

    print(f"\n config.js created successfully.")

def run_csv_script():
    print_step(f"Step 1: Running CSV script ({CSV_SCRIPT})...")

    if not os.path.exists(CSV_SCRIPT):
        print(f"\n  ERROR: Could not find '{CSV_SCRIPT}'")
        print(     "     Make sure run.py is in the same folder as your project.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, CSV_SCRIPT],
        capture_output=False   # let output stream live to the terminal
    )

    if result.returncode != 0:
        print(f"\n  CSV script exited with an error (code {result.returncode}).")
        input("\nPress Enter to exit...")
        sys.exit(result.returncode)

    print("\n  CSV script finished successfully.")


def start_server():
    print_step(f"Step 2: Starting local server on port {SERVER_PORT}...")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # serve from this folder

    handler = http.server.SimpleHTTPRequestHandler

    # Suppress default request logging to keep output clean
    handler.log_message = lambda *args: None

    httpd = socketserver.TCPServer(("", SERVER_PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    print(f"  Server running at http://localhost:{SERVER_PORT}")
    return httpd


def open_browser():
    url = f"http://localhost:{SERVER_PORT}{OPEN_PATH}"
    print_step(f"Step 3: Opening browser at {url}")
    time.sleep(1)  # brief pause so the server is ready
    webbrowser.open(url)


def wait_for_exit(httpd):
    print("\n  App is running! Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n  Shutting down server... Goodbye!")
        httpd.shutdown()


if __name__ == "__main__":
    setup_mapbox_token()
    run_csv_script()
    httpd = start_server()
    open_browser()
    wait_for_exit(httpd)