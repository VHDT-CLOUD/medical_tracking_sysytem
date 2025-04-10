import os
import subprocess

# Run the merge command
result = subprocess.run(
    ['python', 'manage.py', 'makemigrations', '--merge', '--no-input'],
    capture_output=True,
    text=True
)

# Print the output
print(result.stdout)
if result.stderr:
    print("Errors:")
    print(result.stderr)