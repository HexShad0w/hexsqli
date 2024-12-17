import os
import requests
import time
from colorama import Fore, Style, init

init(autoreset=True)

def clear():
    os.system("clear")

def banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + r"""
 _                         _ _
| |__   _____  _____  __ _| (_)
| '_ \ / _ \ \/ / __|/ _` | | |
| | | |  __/>  <\__ \ (_| | | |
|_| |_|\___/_/\_\___/\__, |_|_|
                        |_|

made by @hexsh1dow & @GirlsWhoCodeBot
""")
    print(Fore.CYAN + "=" * 50)


def detect_sqli(target_url, payload_file):

    print(Fore.BLUE + f"\n[+] Starting SQLi detection on: {target_url}")
    results = []
    timeout_threshold = 10

    try:
        with open(payload_file, "r") as file:
            payloads = [line.strip() for line in file.readlines()]
        if not payloads:
            print(Fore.RED + "[!] No payloads found in the file. Exiting.")
            return
        print(Fore.BLUE + f"[+] Loaded {len(payloads)} payloads for testing.\n")


        for i, payload in enumerate(payloads, 1):
            print(Fore.YELLOW + f"[*] Testing payload {i}/{len(payloads)}: {payload}")


            injection_url = target_url.replace("*", payload)
            start_time = time.time()

            try:
                response = requests.get(injection_url, timeout=timeout_threshold + 2)
            except requests.exceptions.Timeout:
                print(Fore.RED + f"[!!!] Timeout detected for payload: {payload}")
                print(Fore.GREEN + f"      [!] This is likely a vulnerability as it exceeds {timeout_threshold} seconds.")
                results.append(f"[!!!] Timeout detected with payload: {payload}")
                continue
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"[!] Error during request: {e}")
                results.append(f"[!] Error with payload: {payload}. Details: {e}")
                continue

            end_time = time.time()
            elapsed_time = end_time - start_time


            if elapsed_time > timeout_threshold:
                print(Fore.GREEN + f"[!!!] Potential SQLi vulnerability detected with payload: {payload}")
                print(Fore.GREEN + f"      Response time: {elapsed_time:.2f} seconds")
                results.append(f"[!!!] Vulnerable payload: {payload} | Response time: {elapsed_time:.2f} seconds")
            else:
                print(Fore.RED + f"[-] No vulnerability detected for payload: {payload}")
                results.append(f"[-] No vulnerability detected with payload: {payload}")

    except FileNotFoundError:
        print(Fore.RED + f"[!] Error: Payload file '{payload_file}' not found.")
    except Exception as e:
        print(Fore.RED + f"[!] An unexpected error occurred: {e}")
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting ...")
        exit()

def main():
    clear()
    banner()

    print(Fore.MAGENTA + "\n[!] Ensure the URL includes '*' where payloads will be tested")
    target = input(Fore.CYAN + "\nEnter the target URL: ")
    payload_file = input(Fore.CYAN + "Enter the path to the payloads file: ")
    detect_sqli(target, payload_file)



if __name__ == "__main__":
    main()
