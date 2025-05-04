import subprocess
import sys, os

IP_OUTPUT_FILE = "source.txt"  # Do not touch, or it might mess with brute.py


def scan_telnet(output: str) -> None:
    cmd = [
        "zmap",
        "-p23",
        "-B",
        "10M",
        "-o",
        output,
    ]  # Internet bandwitdh usage caped at 10Mbps, if remove it you might lose control of the vps (Zmap might use all the bandwidth)
    # Command may be adapted depending on vps capabilities
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nCTRL+C triggered.")


def main(argv: list) -> int:
    if len(argv) < 2:
        print(
            'Usage: %s %s <folder_name>\n\nThis utility script scan the internet until stopped for IPs that have the 23 port opened. \n"folder_name" is the folder where the ips will be put, and can be bruted afterward.'
            % (sys.executable, sys.argv[0])
        )
        return 1
    else:
        folder_name = argv[1]
        os.makedirs(folder_name, exist_ok=True)
        path = os.path.join(folder_name, IP_OUTPUT_FILE)

    print(f"Scanning IPs and saving to {path}")

    scan_telnet(path)

    print(
        f'Finished scanning, IPs were saved into {path},\nplease run "brute.py {folder_name}" to brute force them.'
    )

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
