# File path to your JSON file
file_path = 'urls.json'

try:
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the specific string
    content = content.replace("fOMGkPKOPJaFMgcTthhFu","ptSsuTZFQxSUBFps0o4cE")

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

    print("Successfully replaced all instances of the specified string.")
except Exception as e:
    print(f"An error occurred: {e}")

