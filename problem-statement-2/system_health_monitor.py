#!/usr/bin/env python3
"""
System Health Monitoring Script
Author: [Your Name]
Description: Monitors CPU usage, memory usage, disk space, and running processes.
             Sends alerts when metrics exceed predefined thresholds.
"""

import psutil
import datetime
import time
import os
import sys

# ======================= CONFIGURATION =======================
# Define thresholds
CPU_THRESHOLD = 80          # CPU usage percentage
MEMORY_THRESHOLD = 80       # Memory usage percentage
DISK_THRESHOLD = 80         # Disk usage percentage
PROCESS_COUNT_THRESHOLD = 300  # Number of running processes

# Log file configuration
LOG_FILE = "system_health_monitor.log"
ALERT_LOG_FILE = "system_health_alerts.log"

# Monitoring interval (seconds)
MONITORING_INTERVAL = 5

# ======================= UTILITY FUNCTIONS =======================

def get_timestamp():
    """Return current timestamp in readable format"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_to_log(message, log_file=LOG_FILE):
    """Write message to log file with timestamp"""
    timestamp = get_timestamp()
    log_message = f"[{timestamp}] {message}\n"
    
    try:
        with open(log_file, 'a') as f:
            f.write(log_message)
    except Exception as e:
        print(f"Error writing to log: {e}")

def print_and_log(message, is_alert=False):
    """Print message to console and write to log file"""
    print(message)
    if is_alert:
        write_to_log(message, ALERT_LOG_FILE)
    write_to_log(message)

def send_alert(alert_type, current_value, threshold):
    """Send alert when threshold is exceeded"""
    alert_message = f"⚠️  ALERT: {alert_type} exceeded threshold! Current: {current_value}% | Threshold: {threshold}%"
    print_and_log(alert_message, is_alert=True)

# ======================= MONITORING FUNCTIONS =======================

def check_cpu_usage():
    """Monitor CPU usage"""
    try:
        # Get CPU usage percentage (interval=1 for accurate reading)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        status = "✓ NORMAL" if cpu_percent < CPU_THRESHOLD else "✗ CRITICAL"
        message = f"CPU Usage: {cpu_percent}% [{status}]"
        print_and_log(message)
        
        # Send alert if threshold exceeded
        if cpu_percent > CPU_THRESHOLD:
            send_alert("CPU Usage", cpu_percent, CPU_THRESHOLD)
            
        return cpu_percent
    except Exception as e:
        error_msg = f"Error checking CPU usage: {e}"
        print_and_log(error_msg, is_alert=True)
        return None

def check_memory_usage():
    """Monitor memory usage"""
    try:
        # Get virtual memory statistics
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Get memory details
        total_gb = memory.total / (1024 ** 3)
        used_gb = memory.used / (1024 ** 3)
        available_gb = memory.available / (1024 ** 3)
        
        status = "✓ NORMAL" if memory_percent < MEMORY_THRESHOLD else "✗ CRITICAL"
        message = f"Memory Usage: {memory_percent}% (Used: {used_gb:.2f}GB / Total: {total_gb:.2f}GB) [{status}]"
        print_and_log(message)
        
        # Send alert if threshold exceeded
        if memory_percent > MEMORY_THRESHOLD:
            send_alert("Memory Usage", memory_percent, MEMORY_THRESHOLD)
            
        return memory_percent
    except Exception as e:
        error_msg = f"Error checking memory usage: {e}"
        print_and_log(error_msg, is_alert=True)
        return None

def check_disk_usage():
    """Monitor disk space usage"""
    try:
        # Get disk usage for root partition
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # Get disk details
        total_gb = disk.total / (1024 ** 3)
        used_gb = disk.used / (1024 ** 3)
        free_gb = disk.free / (1024 ** 3)
        
        status = "✓ NORMAL" if disk_percent < DISK_THRESHOLD else "✗ CRITICAL"
        message = f"Disk Usage: {disk_percent}% (Used: {used_gb:.2f}GB / Total: {total_gb:.2f}GB / Free: {free_gb:.2f}GB) [{status}]"
        print_and_log(message)
        
        # Send alert if threshold exceeded
        if disk_percent > DISK_THRESHOLD:
            send_alert("Disk Usage", disk_percent, DISK_THRESHOLD)
            
        return disk_percent
    except Exception as e:
        error_msg = f"Error checking disk usage: {e}"
        print_and_log(error_msg, is_alert=True)
        return None

def check_running_processes():
    """Monitor running processes"""
    try:
        # Get list of all running processes
        process_count = len(psutil.pids())
        
        status = "✓ NORMAL" if process_count < PROCESS_COUNT_THRESHOLD else "✗ HIGH"
        message = f"Running Processes: {process_count} [{status}]"
        print_and_log(message)
        
        # Send alert if threshold exceeded
        if process_count > PROCESS_COUNT_THRESHOLD:
            alert_message = f"⚠️  ALERT: Process count exceeded threshold! Current: {process_count} | Threshold: {PROCESS_COUNT_THRESHOLD}"
            print_and_log(alert_message, is_alert=True)
        
        # Get top 5 CPU-consuming processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        top_processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:5]
        
        if top_processes:
            print_and_log("\nTop 5 CPU-consuming processes:")
            for idx, proc in enumerate(top_processes, 1):
                proc_msg = f"  {idx}. PID: {proc['pid']} | Name: {proc['name']} | CPU: {proc['cpu_percent']}%"
                print_and_log(proc_msg)
        
        return process_count
    except Exception as e:
        error_msg = f"Error checking running processes: {e}"
        print_and_log(error_msg, is_alert=True)
        return None

def get_system_info():
    """Get basic system information"""
    try:
        # Get system information
        system_info = {
            'Platform': sys.platform,
            'CPU Cores': psutil.cpu_count(logical=False),
            'CPU Threads': psutil.cpu_count(logical=True),
            'Boot Time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return system_info
    except Exception as e:
        print_and_log(f"Error getting system info: {e}", is_alert=True)
        return None

def print_header():
    """Print monitoring header"""
    header = f"""
{'='*80}
          SYSTEM HEALTH MONITORING - AccuKnox Assessment
{'='*80}
Thresholds: CPU: {CPU_THRESHOLD}% | Memory: {MEMORY_THRESHOLD}% | Disk: {DISK_THRESHOLD}% | Processes: {PROCESS_COUNT_THRESHOLD}
Monitoring started at: {get_timestamp()}
Log files: {LOG_FILE}, {ALERT_LOG_FILE}
{'='*80}
    """
    print(header)
    write_to_log(header)

def monitor_system_once():
    """Perform one complete system health check"""
    print_and_log("\n" + "="*80)
    print_and_log(f"System Health Check - {get_timestamp()}")
    print_and_log("="*80)
    
    # Check all metrics
    cpu = check_cpu_usage()
    memory = check_memory_usage()
    disk = check_disk_usage()
    processes = check_running_processes()
    
    # Generate summary
    print_and_log("\n" + "-"*80)
    print_and_log("SUMMARY:")
    
    all_normal = True
    if cpu and cpu > CPU_THRESHOLD:
        all_normal = False
    if memory and memory > MEMORY_THRESHOLD:
        all_normal = False
    if disk and disk > DISK_THRESHOLD:
        all_normal = False
    if processes and processes > PROCESS_COUNT_THRESHOLD:
        all_normal = False
    
    if all_normal:
        print_and_log("✓ All systems operating normally")
    else:
        print_and_log("✗ Some systems require attention - check alerts above")
    
    print_and_log("-"*80 + "\n")

def monitor_system_continuous():
    """Monitor system continuously"""
    print_header()
    
    # Display system information once
    system_info = get_system_info()
    if system_info:
        print_and_log("\nSystem Information:")
        for key, value in system_info.items():
            print_and_log(f"  {key}: {value}")
    
    print_and_log(f"\nMonitoring interval: {MONITORING_INTERVAL} seconds")
    print_and_log("Press Ctrl+C to stop monitoring\n")
    
    try:
        iteration = 0
        while True:
            iteration += 1
            print_and_log(f"\n{'#'*80}")
            print_and_log(f"Monitoring Iteration #{iteration}")
            print_and_log(f"{'#'*80}")
            
            monitor_system_once()
            
            # Wait before next check
            print_and_log(f"Waiting {MONITORING_INTERVAL} seconds before next check...\n")
            time.sleep(MONITORING_INTERVAL)
            
    except KeyboardInterrupt:
        print_and_log("\n\nMonitoring stopped by user")
        print_and_log(f"Total monitoring iterations: {iteration}")
        print_and_log(f"Logs saved to: {LOG_FILE}")
        print_and_log(f"Alerts saved to: {ALERT_LOG_FILE}")

# ======================= MAIN FUNCTION =======================

def main():
    """Main function"""
    print("\nSystem Health Monitoring Script")
    print("Choose monitoring mode:")
    print("1. Single Check (run once)")
    print("2. Continuous Monitoring (run continuously)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == '1':
        print("\n" + "="*80)
        print("Running single system health check...")
        print("="*80)
        monitor_system_once()
        print("\nCheck complete! Logs saved to:", LOG_FILE)
        
    elif choice == '2':
        monitor_system_continuous()
        
    elif choice == '3':
        print("Exiting...")
        sys.exit(0)
        
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()