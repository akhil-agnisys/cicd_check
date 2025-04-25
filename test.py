import subprocess
import sys
import os

# Function to run a subprocess command and return the result
def run_command(command):
    result = subprocess.run(command, shell=True,
                            stdout=subprocess.PIPE, 
                            
                    stderr=subprocess.PIPE)
    return result

# Run black in check mode
def check_black():
    print("Running black check...")
    result = run_command("black . --check")
    if result.returncode != 0:
        print("Black formatting issues found!")
        print(result.stdout.decode())
        sys.exit(1)
    else:
        print("Black formatting is correct.")

# Run pylint and check the score
def check_pylint():
    print("Running pylint...")
    result = run_command("pylint $(find . -name '*.py') --max-score=10 --output-format=text")
    
    # Parse the result to get the score
    output = result.stdout.decode()
    score = None
    for line in output.splitlines():
        if "Your code has been rated at" in line:
            score = float(line.split()[-2])
            break
    
    if score is not None:
        print(f"Pylint score: {score}")
        if score < 8.9:
            print("Pylint score is below 8.9. Please fix the issues.")
            sys.exit(1)
    else:
        print("Could not find pylint score in the output.")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure we are in the correct directory
    if not os.path.isdir("."):
        print("This script should be run from the root of the project.")
        sys.exit(1)

    check_black()
    check_pylint()
    print("Both black and pylint checks passed successfully!")
