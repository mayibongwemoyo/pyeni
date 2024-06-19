def vswr(output):
    # Define the line pattern to search for
    target_line = r"VSWR"  # Matches the specific line format for VSWR

    # Find the starting index of the section
    start_index = output.find(target_line)

    # Check if the target line was found
    if start_index == -1:
        print("No matching line found.")
        return

    # Find the second occurrence of the separator line
    first_occurrence = output.find("===(.*?)===")
    end_index = output.find("===(.*?)===", first_occurrence + 1)

    # Extract and print the desired section
    section = output[start_index:end_index]
    print(section.strip())  # Remove leading/trailing whitespace

def fiber_loss(output):
    # Define the line pattern to search for
    target_line = r"DlLoss"  # Matches the specific line format for fiberloss

    # Find the starting index of the section
    start_index = output.find(target_line)

    # Check if the target line was found
    if start_index == -1:
        print("No matching line found.")
        return

    # Find the second occurrence of the separator line
    first_occurrence = output.find("---(.*?)---")
    end_index = output.find("---(.*?)---", first_occurrence + 1)

    # Extract and print the desired section
    section = output[start_index:end_index]
    print(section.strip())  # Remove leading/trailing whitespace


with open('output.txt', 'r') as file:
    output = file.read()
vswr(output)
fiber_loss(output)
