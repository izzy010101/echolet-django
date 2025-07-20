import psutil
import time
import os

def get_processes_by_name(name):
    return [p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] and name.lower() in p.info['name'].lower()]

while True:
    os.system('cls')
    django_procs = get_processes_by_name("python")
    vue_procs = get_processes_by_name("node")

    print("="*40)
    print("Django (python.exe) usage:")
    if django_procs:
        for p in django_procs:
            try:
                cpu = p.cpu_percent(interval=0.1)
                mem = p.memory_info().rss / 1024 / 1024
                print(f"PID {p.pid}: CPU {cpu:.2f}%, Memory {mem:.2f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    else:
        print("No python.exe process found (Django).")

    print("\nVue.js (node.exe) usage:")
    if vue_procs:
        for p in vue_procs:
            try:
                cpu = p.cpu_percent(interval=0.1)
                mem = p.memory_info().rss / 1024 / 1024
                print(f"PID {p.pid}: CPU {cpu:.2f}%, Memory {mem:.2f} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    else:
        print("No node.exe process found (Vue).")

    time.sleep(2)