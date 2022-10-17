from dvrip import DVRIPCam

cams = ('192.168.0.14', '192.168.0.133', '192.168.0.15', '192.168.0.222')

try:

    for IP in cams:

        cam = DVRIPCam(IP, user='admin', password='St4nburyRd!')

        print("\nConnecting to {}...".format(IP))

        try:
            if cam.login():
                print("Connected")
            else:
                print("Failed to connect")
                continue
        except Exception as e:
            print("Connection failed with exception: {}".format(e))
            continue

        print("Current camera time:", cam.get_time())

        cam.set_time()

        print("New camera time:", cam.get_time())

except KeyboardInterrupt:
    exit()
