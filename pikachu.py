import subprocess
import argparse

def run_nmap_vuln_scan(target, output_file=None):
    nmap_command = ["nmap", "-vv", "--script=vuln", target]
    if output_file:
        nmap_command.extend(["-oN", output_file])

    try:
        result = subprocess.run(nmap_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Nmap Error: {e}")
        print(e.stderr)

def run_dirsearch_scan(target, output_file=None):
    dirsearch_command = ["dirsearch", "-u", target]
    if output_file:
        dirsearch_command.extend(["--output", output_file])

    try:
        result = subprocess.run(dirsearch_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Dirsearch Error: {e}")
        print(e.stderr)

def run_subfinder_scan(target, output_file=None):
    subfinder_command = ["subfinder", "-d", target]
    if output_file:
        subfinder_command.extend(["-o", output_file])

    try:
        result = subprocess.run(subfinder_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Subfinder Error: {e}")
        print(e.stderr)

def run_assetfinder_scan(target, output_file=None):
    assetfinder_command = ["assetfinder", target]
    if output_file:
        assetfinder_command.extend(["-o", output_file])

    try:
        result = subprocess.run(assetfinder_command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Assetfinder Error: {e}")
        print(e.stderr)

def main():
    parser = argparse.ArgumentParser(description="Automate Nmap vulnerability scanning and directory/subdomain searches.")
    parser.add_argument("-d", "--domain", help="Specify the target domain")
    parser.add_argument("-ip", "--ip", help="Specify the target IP address")
    parser.add_argument("-o", "--output", help="Specify the output file")
    
    args = parser.parse_args()

    if args.domain:
        run_nmap_vuln_scan(args.domain, args.output)
        run_dirsearch_scan(args.domain, args.output)
        run_subfinder_scan(args.domain, args.output)
        run_assetfinder_scan(args.domain, args.output)
    elif args.ip:
        run_nmap_vuln_scan(args.ip, args.output)
    else:
        print("Please specify a target domain or IP address using -d or -ip.")

if __name__ == "__main__":
    main()
  
