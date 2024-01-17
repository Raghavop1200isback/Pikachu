import subprocess

def install_dependencies():
    try:
        subprocess.run(["pip", "install", "argparse"])  # Add other dependencies if needed
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

if __name__ == "__main__":
    install_dependencies()
  
