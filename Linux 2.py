# pip install psutil
import psutil

# به صورت پیش فرض نصبه
import os

def get_cpu_temperature():
    if os.name == 'posix': # بررسی اینکه سیستم عامل لینوکس است یا خیر
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read().strip()) / 1000.0 # تبدیل به درجه سانتیگراد
            return temp
    elif os.name == 'nt': # بررسی اینکه سیستم عامل ویندوز است یا خیر
        output = os.popen('wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature').read().strip()
        temp = int(output.split('\n')[1].strip()) / 10.0 - 273.15 # تبدیل به درجه سانتیگراد
        return temp
    else:
        return None

print("CPU Temperature: {}°C".format(get_cpu_temperature()))



# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

print("-----------------------------------------------------")

# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {svmem.total/(1024*1024):.2f} MB")
print(f"Available: {svmem.available/(1024*1024):.2f} MB")
print(f"Used: {svmem.used/(1024*1024):.2f} MB")
print(f"Percentage: {svmem.percent}%")

# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {swap.total/(1024*1024):.2f} MB")
print(f"Free: {swap.free/(1024*1024):.2f} MB")
print(f"Used: {swap.used/(1024*1024):.2f} MB")
print(f"Percentage: {swap.percent}%")

print("-----------------------------------------------------")

# Disk Information
print("Disk Information")
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"\t Device: {partition.device} \t")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {partition_usage.total/(1024*1024):.2f} MB")
    print(f"  Used: {partition_usage.used/(1024*1024):.2f} MB")
    print(f"  Free: {partition_usage.free/(1024*1024):.2f} MB")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {disk_io.read_bytes/(1024*1024):.2f} MB")
print(f"Total write: {disk_io.write_bytes/(1024*1024):.2f} MB")

print("-----------------------------------------------------------------")

# network monitoring
import socket

def get_network_stats():
    stats = psutil.net_io_counters()
    return (stats.bytes_sent, stats.bytes_recv)

def get_open_connections():
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            connections.append((conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port))
    return connections

def is_port_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

# بررسی اتصال به سرور گوگل
if is_port_open('google.com', 80):
    print("Connected to Google")
else:
    print("Could not connect to Google")

# نمایش آمار شبکه
bytes_sent, bytes_recv = get_network_stats()
print("Bytes sent: {}".format(bytes_sent))
print("Bytes received: {}".format(bytes_recv))

# نمایش اتصالات باز
connections = get_open_connections()
for conn in connections:
    print("{}:{} -> {}:{}".format(conn[0], conn[1], conn[2], conn[3]))
