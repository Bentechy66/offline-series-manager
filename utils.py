def log(severity, message):
    if severity == "success":
        print("[*] " + message)
    elif severity == "info":
        print("[-] " + message)
    elif severity == "warning":
        print("[!] " + message)
    elif severity == "error":
        print("[#] " + message)
    elif severity == "critical":
        print("[!!] " + message + ". Exiting.")
