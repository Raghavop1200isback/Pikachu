import argparse
import whois
import requests
import subprocess
import os

def perform_whois_lookup(domain, output_file=None):
    try:
        whois_info = whois.whois(domain)
        print("\nWHOIS Information:")
        print(whois_info)

        if output_file:
            with open(output_file, 'a') as file:
                file.write("\nWHOIS Information:\n")
                file.write(str(whois_info) + "\n")
    except whois.parser.PywhoisError as e:
        print(f"WHOIS lookup failed: {e}")

def perform_social_media_analysis(username, output_file=None):
    # Example: Checking GitHub for the given username
    github_url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(github_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        github_data = response.json()

        print("\nGitHub Information:")
        print(f"Username: {github_data['login']}")
        print(f"Name: {github_data['name']}")
        print(f"Bio: {github_data['bio']}")

        if output_file:
            with open(output_file, 'a') as file:
                file.write("\nGitHub Information:\n")
                file.write(f"Username: {github_data['login']}\n")
                file.write(f"Name: {github_data['name']}\n")
                file.write(f"Bio: {github_data['bio']}\n")
    except requests.RequestException as e:
        print(f"GitHub analysis failed: {e}")

def perform_network_scan(target, output_file=None):
    try:
        nmap_command = ["nmap", "-Pn", "-sP", target]
        result = subprocess.run(nmap_command, capture_output=True, text=True, check=True)
        print("\nNetwork Scan Results:")
        print(result.stdout)

        if output_file:
            with open(output_file, 'a') as file:
                file.write("\nNetwork Scan Results:\n")
                file.write(result.stdout + "\n")
    except subprocess.CalledProcessError as e:
        print(f"Network scan failed: {e}")
        print(e.stderr)

def perform_network_recon(target, output_file=None):
    # Placeholder for network reconnaissance actions
    print("\nPerforming Network Reconnaissance:")
    print(f"Network Mapping: {target}")
    print(f"DNS Enumeration: {target}")
    print(f"SNMP Enumeration: {target}")

    # Modify this function based on your specific network reconnaissance actions
    if output_file:
        with open(output_file, 'a') as file:
            file.write("\nNetwork Reconnaissance Results:\n")
            file.write(f"Network Mapping: {target}\n")
            file.write(f"DNS Enumeration: {target}\n")
            file.write(f"SNMP Enumeration: {target}\n")

def perform_web_recon(target, output_file=None):
    # Placeholder for web reconnaissance actions
    print("\nPerforming Web Reconnaissance:")
    print(f"Web Scraping: {target}")
    print(f"Spidering: {target}")
    print(f"Directory and File Enumeration: {target}")

    # Modify this function based on your specific web reconnaissance actions
    if output_file:
        with open(output_file, 'a') as file:
            file.write("\nWeb Reconnaissance Results:\n")
            file.write(f"Web Scraping: {target}\n")
            file.write(f"Spidering: {target}\n")
            file.write(f"Directory and File Enumeration: {target}\n")

def perform_wireless_recon(interface, output_file=None):
    # Placeholder for wireless reconnaissance actions
    print("\nPerforming Wireless Reconnaissance:")
    print(f"Wardriving: {interface}")
    print(f"Wireless Network Scanning: {interface}")

    # Modify this function based on your specific wireless reconnaissance actions
    if output_file:
        with open(output_file, 'a') as file:
            file.write("\nWireless Reconnaissance Results:\n")
            file.write(f"Wardriving: {interface}\n")
            file.write(f"Wireless Network Scanning: {interface}\n")

def perform_vulnerability_scan(target, output_file=None):
    try:
        nmap_command = ["nmap", "-Pn", "--script=vuln", target]
        result = subprocess.run(nmap_command, capture_output=True, text=True, check=True)
        print("\nVulnerability Scan Results:")
        print(result.stdout)

        if output_file:
            with open(output_file, 'a') as file:
                file.write("\nVulnerability Scan Results:\n")
                file.write(result.stdout + "\n")
    except subprocess.CalledProcessError as e:
        print(f"Vulnerability scan failed: {e}")
        print(e.stderr)

def create_output_directory(output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def reconnaissance(args):
    output_file = args.output

    if args.domain:
        perform_whois_lookup(args.domain, output_file)
        if args.active:
            perform_network_scan(args.domain, output_file)
        if args.network:
            perform_network_recon(args.domain, output_file)
        if args.web:
            perform_web_recon(args.domain, output_file)
        if args.wireless:
            perform_wireless_recon(args.wireless, output_file)
        if args.vulnerability:
            perform_vulnerability_scan(args.domain, output_file)
    elif args.username:
        perform_social_media_analysis(args.username, output_file)
    else:
        print("Please specify a domain or username for reconnaissance.")

def main():
    parser = argparse.ArgumentParser(description="Reconnaissance script.")
    parser.add_argument("--domain", help="Perform WHOIS lookup for the specified domain.")
    parser.add_argument("--username", help="Perform social media analysis for the specified username.")
    parser.add_argument("--active", action="store_true", help="Perform active reconnaissance (network scan, etc.).")
    parser.add_argument("--network", action="store_true", help="Perform network reconnaissance (mapping, DNS enumeration, SNMP enumeration, etc.).")
    parser.add_argument("--web", action="store_true", help="Perform web reconnaissance (web scraping, spidering, directory and file enumeration, etc.).")
    parser.add_argument("--wireless", help="Perform wireless reconnaissance (wardriving, wireless network scanning, etc.).")
    parser.add_argument("--vulnerability", action="store_true", help="Perform vulnerability scanning, fingerprinting, banner grabbing, etc.")
    parser.add_argument("--output", help="Specify the output file or directory for saving results.")
    parser.add_argument("--help", action="help", help="Show this help message and exit.")

    args = parser.parse_args()

    if args.output and not os.path.isdir(args.output):
        # If the output is a file, create its parent directory
        create_output_directory(os.path.dirname(args.output))

    if args.domain or args.username:
        reconnaissance(args)
    else:
        print("Please specify either a domain or a username for reconnaissance.")

if __name__ == "__main__":
    main()
