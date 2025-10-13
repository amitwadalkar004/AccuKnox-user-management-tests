#!/usr/bin/env python3
"""
Application Health Checker Script
Author: [Your Name]
Description: Checks the uptime and health of applications by monitoring HTTP status codes.
             Determines if applications are 'up' (functioning) or 'down' (unavailable).
"""

import requests
import datetime
import time
import json
import sys
from urllib.parse import urlparse

# ======================= CONFIGURATION =======================

# Log file configuration
LOG_FILE = "app_health_checker.log"
REPORT_FILE = "app_health_report.json"

# Request timeout (seconds)
REQUEST_TIMEOUT = 10

# Monitoring interval for continuous mode (seconds)
CHECK_INTERVAL = 30

# ======================= UTILITY FUNCTIONS =======================

def get_timestamp():
    """Return current timestamp in readable format"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_to_log(message):
    """Write message to log file with timestamp"""
    timestamp = get_timestamp()
    log_message = f"[{timestamp}] {message}\n"
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:  # ← Fixed!
            f.write(log_message)
    except Exception as e:
        print(f"Error writing to log: {e}")

def print_and_log(message):
    """Print message to console and write to log file"""
    print(message)
    write_to_log(message)

def validate_url(url):
    """Validate if URL is properly formatted"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# ======================= HEALTH CHECK FUNCTIONS =======================

def check_application_health(url, app_name=None):
    """
    Check the health of an application by making HTTP request
    Returns: dict with health check results
    """
    if not app_name:
        app_name = urlparse(url).netloc
    
    health_data = {
        'application': app_name,
        'url': url,
        'timestamp': get_timestamp(),
        'status': 'unknown',
        'status_code': None,
        'response_time_ms': None,
        'is_up': False,
        'message': '',
        'error': None
    }
    
    print_and_log(f"\nChecking health of: {app_name} ({url})")
    
    try:
        # Make HTTP request
        start_time = time.time()
        response = requests.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        end_time = time.time()
        
        # Calculate response time
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Get status code
        status_code = response.status_code
        
        # Update health data
        health_data['status_code'] = status_code
        health_data['response_time_ms'] = round(response_time, 2)
        
        # Determine if application is UP or DOWN based on status code
        if 200 <= status_code < 300:
            # 2xx - Success
            health_data['is_up'] = True
            health_data['status'] = 'success'
            health_data['message'] = "✓ Application is UP and functioning correctly"
            print_and_log(f"Status: ✓ UP")
            print_and_log(f"HTTP Status Code: {status_code} (Success)")
            print_and_log(f"Response Time: {response_time:.2f}ms")
            print_and_log(f"✓ Application is functioning correctly")
            
        elif 300 <= status_code < 400:
            # 3xx - Redirection
            health_data['is_up'] = True
            health_data['status'] = 'redirect'
            health_data['message'] = f"↗ Application is UP (redirected to {response.url})"
            print_and_log(f"Status: ↗ UP (with redirect)")
            print_and_log(f"HTTP Status Code: {status_code} (Redirect)")
            print_and_log(f"Redirected to: {response.url}")
            print_and_log(f"Response Time: {response_time:.2f}ms")
            
        elif 400 <= status_code < 500:
            # 4xx - Client Error
            health_data['is_up'] = False
            health_data['status'] = 'client_error'
            health_data['message'] = "⚠ Application is DOWN (Client Error)"
            print_and_log(f"Status: ⚠ DOWN")
            print_and_log(f"HTTP Status Code: {status_code} (Client Error)")
            print_and_log(f"Response Time: {response_time:.2f}ms")
            print_and_log(f"✗ Client error - Application may be inaccessible")
            
        else:  # 5xx Server Error
            health_data['is_up'] = False
            health_data['status'] = 'server_error'
            health_data['message'] = "✗ Application is DOWN (Server Error)"
            print_and_log(f"Status: ✗ DOWN")
            print_and_log(f"HTTP Status Code: {status_code} (Server Error)")
            print_and_log(f"Response Time: {response_time:.2f}ms")
            print_and_log(f"✗ Server error - Application is not functioning")
        
    except requests.exceptions.Timeout:
        health_data['error'] = 'Request timeout'
        health_data['message'] = "✗ Application is DOWN (Timeout)"
        print_and_log(f"Status: ✗ DOWN")
        print_and_log(f"Error: Request timeout after {REQUEST_TIMEOUT} seconds")
        print_and_log(f"✗ Application is not responding")
        
    except requests.exceptions.ConnectionError:
        health_data['error'] = 'Connection error'
        health_data['message'] = "✗ Application is DOWN (Connection Failed)"
        print_and_log(f"Status: ✗ DOWN")
        print_and_log(f"Error: Unable to establish connection")
        print_and_log(f"✗ Application is unavailable or not responding")
        
    except requests.exceptions.RequestException as e:
        health_data['error'] = str(e)
        health_data['message'] = "✗ Application is DOWN (Request Error)"
        print_and_log(f"Status: ✗ DOWN")
        print_and_log(f"Error: {str(e)}")
        print_and_log(f"✗ Application health check failed")
        
    except Exception as e:
        health_data['error'] = str(e)
        health_data['message'] = "✗ Application is DOWN (Unknown Error)"
        print_and_log(f"Status: ✗ DOWN")
        print_and_log(f"Unexpected error: {str(e)}")
        print_and_log(f"✗ Health check encountered an error")
    
    return health_data

def check_multiple_applications(app_list):
    """
    Check health of multiple applications
    app_list: list of dicts with 'name' and 'url' keys
    """
    print_and_log("\n" + "="*80)
    print_and_log("MULTIPLE APPLICATION HEALTH CHECK")
    print_and_log("="*80)
    
    results = []
    up_count = 0
    down_count = 0
    
    for idx, app in enumerate(app_list, 1):
        print_and_log(f"\n[{idx}/{len(app_list)}] Checking: {app['name']}")
        print_and_log("-" * 80)
        
        result = check_application_health(app['url'], app['name'])
        results.append(result)
        
        if result['is_up']:
            up_count += 1
        else:
            down_count += 1
    
    # Print summary
    print_and_log("\n" + "="*80)
    print_and_log("HEALTH CHECK SUMMARY")
    print_and_log("="*80)
    print_and_log(f"Total Applications Checked: {len(app_list)}")
    print_and_log(f"✓ UP: {up_count}")
    print_and_log(f"✗ DOWN: {down_count}")
    print_and_log("="*80)
    
    # Detailed results
    print_and_log("\nDETAILED RESULTS:")
    print_and_log("-" * 80)
    
    for result in results:
        status_symbol = "✓" if result['is_up'] else "✗"
        print_and_log(f"\n{status_symbol} {result['application']}")
        print_and_log(f"   URL: {result['url']}")
        print_and_log(f"   Status: {result['message']}")
        if result['status_code']:
            print_and_log(f"   HTTP Code: {result['status_code']}")
        if result['response_time_ms']:
            print_and_log(f"   Response Time: {result['response_time_ms']}ms")
        if result['error']:
            print_and_log(f"   Error: {result['error']}")
    
    # Save report to JSON file
    save_report(results)
    
    return results

def save_report(results):
    """Save health check results to JSON file"""
    try:
        report = {
            'timestamp': get_timestamp(),
            'total_checked': len(results),
            'up_count': sum(1 for r in results if r['is_up']),
            'down_count': sum(1 for r in results if not r['is_up']),
            'applications': results
        }
        
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:  # ← Add encoding
            json.dump(report, f, indent=2, ensure_ascii=False)  # ← Add ensure_ascii=False
        
        print_and_log(f"\n✓ Report saved to: {REPORT_FILE}")
        
    except Exception as e:
        print_and_log(f"Error saving report: {e}")

def monitor_application_continuous(url, app_name=None, interval=CHECK_INTERVAL):
    """Monitor application continuously"""
    if not app_name:
        app_name = urlparse(url).netloc
    
    print_and_log("\n" + "="*80)
    print_and_log(f"CONTINUOUS MONITORING: {app_name}")
    print_and_log("="*80)
    print_and_log(f"URL: {url}")
    print_and_log(f"Check Interval: {interval} seconds")
    print_and_log(f"Started at: {get_timestamp()}")
    print_and_log("Press Ctrl+C to stop monitoring")
    print_and_log("="*80)
    
    iteration = 0
    uptime_count = 0
    downtime_count = 0
    
    try:
        while True:
            iteration += 1
            print_and_log(f"\n{'#'*80}")
            print_and_log(f"Check #{iteration} - {get_timestamp()}")
            print_and_log(f"{'#'*80}")
            
            result = check_application_health(url, app_name)
            
            if result['is_up']:
                uptime_count += 1
            else:
                downtime_count += 1
            
            # Calculate uptime percentage
            uptime_percentage = (uptime_count / iteration) * 100
            
            print_and_log(f"\nMonitoring Statistics:")
            print_and_log(f"  Total Checks: {iteration}")
            print_and_log(f"  Up: {uptime_count} times")
            print_and_log(f"  Down: {downtime_count} times")
            print_and_log(f"  Uptime: {uptime_percentage:.2f}%")
            
            print_and_log(f"\nNext check in {interval} seconds...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print_and_log("\n\n" + "="*80)
        print_and_log("MONITORING STOPPED")
        print_and_log("="*80)
        print_and_log(f"Total monitoring duration: {iteration * interval} seconds")
        print_and_log(f"Total checks performed: {iteration}")
        print_and_log(f"Uptime: {uptime_count} times ({uptime_percentage:.2f}%)")
        print_and_log(f"Downtime: {downtime_count} times ({(100-uptime_percentage):.2f}%)")
        print_and_log(f"Logs saved to: {LOG_FILE}")

# ======================= PREDEFINED APPLICATIONS =======================

SAMPLE_APPLICATIONS = [
    {'name': 'Google', 'url': 'https://www.google.com'},
    {'name': 'GitHub', 'url': 'https://github.com'},
    {'name': 'OrangeHRM Demo', 'url': 'https://opensource-demo.orangehrmlive.com'},
    {'name': 'Invalid URL (Test)', 'url': 'https://this-url-does-not-exist-12345.com'},
]

# ======================= MAIN FUNCTION =======================

def main():
    """Main function"""
    print("\n" + "="*80)
    print("APPLICATION HEALTH CHECKER - AccuKnox Assessment")
    print("="*80)
    print("\nChoose an option:")
    print("1. Check single application")
    print("2. Check multiple applications (predefined list)")
    print("3. Check multiple applications (custom URLs)")
    print("4. Continuous monitoring (single application)")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        url = input("\nEnter application URL (e.g., https://example.com): ").strip()
        if not validate_url(url):
            print("Invalid URL format. Please include http:// or https://")
            return
        
        app_name = input("Enter application name (optional, press Enter to skip): ").strip()
        if not app_name:
            app_name = None
        
        check_application_health(url, app_name)
        print_and_log(f"\n✓ Check complete! Log saved to: {LOG_FILE}")
        
    elif choice == '2':
        check_multiple_applications(SAMPLE_APPLICATIONS)
        
    elif choice == '3':
        print("\nEnter URLs to check (type 'done' when finished):")
        app_list = []
        idx = 1
        
        while True:
            url = input(f"  {idx}. URL: ").strip()
            if url.lower() == 'done':
                break
            
            if not validate_url(url):
                print("     Invalid URL format. Skipping...")
                continue
            
            name = input(f"     Name: ").strip()
            if not name:
                name = urlparse(url).netloc
            
            app_list.append({'name': name, 'url': url})
            idx += 1
        
        if app_list:
            check_multiple_applications(app_list)
        else:
            print("No applications added.")
        
    elif choice == '4':
        url = input("\nEnter application URL to monitor: ").strip()
        if not validate_url(url):
            print("Invalid URL format. Please include http:// or https://")
            return
        
        app_name = input("Enter application name (optional): ").strip()
        if not app_name:
            app_name = None
        
        interval_input = input(f"Enter check interval in seconds (default: {CHECK_INTERVAL}): ").strip()
        interval = int(interval_input) if interval_input.isdigit() else CHECK_INTERVAL
        
        monitor_application_continuous(url, app_name, interval)
        
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)
        
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()