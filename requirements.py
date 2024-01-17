import subprocess
import sys

def install_required_tools():
    try:
        # Install nmap
        subprocess.run(['sudo', 'apt', 'install', '-y', 'nmap'], check=True)

        # Install git for cloning repositories
        subprocess.run(['sudo', 'apt', 'install', '-y', 'git'], check=True)

        # Install whois
        subprocess.run(['sudo', 'apt', 'install', '-y', 'whois'], check=True)

        print("Required tools installed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error installing required tools: {e}")
        sys.exit(1)

def install_required_python_modules():
    try:
        # Install required Python packages
        subprocess.run(['pip3', 'install', 'whois', 'requests'], check=True)
        print("Required Python modules installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing required Python modules: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_required_tools()
    install_required_python_modules()
    print("All required tools and modules installed successfully!")
