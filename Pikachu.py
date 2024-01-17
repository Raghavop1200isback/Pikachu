import subprocess
import argparse

def run_nmap_vuln_scan(target):
    nmap_command = ["nmap", "-vv", "--script=vuln", target]
    
    try:
        result = subprocess.run(nmap_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Nmap Error: {e}")
        print(e.stderr)

def run_dirsearch_scan(target):
    dirsearch_command = ["dirsearch", "-u", target]
    
    try:
        result = subprocess.run(dirsearch_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Dirsearch Error: {e}")
        print(e.stderr)

def main():
    parser = argparse.ArgumentParser(description="Automate Nmap vulnerability scanning and dirsearch.")
    parser.add_argument("-d", "--domain", help="Specify the target domain")
    parser.add_argument("-ip", "--ip", help="Specify the target IP address")
    
    args = parser.parse_args()

    if args.domain:
        run_nmap_vuln_scan(args.domain)
        run_dirsearch_scan(args.domain)
    elif args.ip:
        run_nmap_vuln_scan(args.ip)
    else:
        print("Please specify a target domain or IP address using -d or -ip.")

if __name__ == "__main__":
    main()
      
