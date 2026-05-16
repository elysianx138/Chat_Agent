import subprocess
import json
WSL_PATH = os.getenv("")

def get_system_info():
    result = subprocess.run(
        ["wsl",WSL_PATH],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()

    try:
        data = json.loads(output)
        return data
    except:
        return None


if __name__ == "__main__":
    data = get_system_info()
    if data:
        
        print("内存占用率:",data["cpu_usage"])