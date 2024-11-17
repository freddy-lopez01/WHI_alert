# Read the file, replace single quotes with double quotes, and save it back
file_path = 'urls.json'

try:
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace single quotes with double quotes
    content = content.replace("'", '"')

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

    print("Successfully replaced single quotes with double quotes.")
except Exception as e:
    print(f"An error occurred: {e}")

