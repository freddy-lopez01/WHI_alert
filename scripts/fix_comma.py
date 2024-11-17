def add_commas_before_curly_braces(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        modified_content = []
        for i, line in enumerate(lines):
            line = line.strip()
            # If the line contains a starting curly brace, add a comma before it unless it's the first one
            if line.startswith("{") and i != 0:
                modified_content.append(",")
            modified_content.append(line)

        # Write the modified content to the output file
        with open(output_file, 'w') as outfile:
            outfile.write("\n".join(modified_content))

        print(f"File processed successfully, saved as {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file = 'information.json'  # Replace with the path to your input file
output_file = 'output.json'  # Replace with the path to your output file
add_commas_before_curly_braces(input_file, output_file)

