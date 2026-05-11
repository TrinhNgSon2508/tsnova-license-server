import subprocess


def get_hwid():

    try:
        output = subprocess.check_output(
            "wmic csproduct get uuid",
            shell=True
        ).decode()

        hwid = output.split("\n")[1].strip()

        return hwid

    except:
        return "UNKNOWN"