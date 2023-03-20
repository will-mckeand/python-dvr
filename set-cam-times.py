from dvrip import DVRIPCam, SomethingIsWrongWithCamera

cams = ("192.168.0.14", "192.168.0.133", "192.168.0.222", "192.168.0.15")

try:
    for IP in cams:
        print("\n" + IP)
        cam = DVRIPCam(IP, user="admin", password="St4nburyRd!")

        try:
            if cam.login():
                print("Connected")
            else:
                print("Failed to connect")
                continue
        except SomethingIsWrongWithCamera as e:
            print("Connection failed:", e)
            continue

        print("Orig:\t", cam.get_time())
        cam.set_time()
        print("New:\t", cam.get_time())
        cam.close()

except KeyboardInterrupt:
    exit()
