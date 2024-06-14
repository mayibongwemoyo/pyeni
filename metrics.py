import re
import json

def vswr(output):
    # Define the line pattern to search for
    target_line = r"VSWR"  # Matches the specific line format for VSWR

    # Find the starting index of the section
    start_index = output.find(target_line)

    # Check if the target line was found
    if start_index == -1:
        print("No matching line found.")
        return {}  # Return an empty dictionary if not found

    # Find the second occurrence of the separator line
    first_occurrence = output.find("===(.*?)===")
    end_index = output.find("===(.*?)===", first_occurrence + 1)

    # Extract and print the desired section
    section = output[start_index:end_index]

    # Extract VSWR values using regex
    vswr_values = re.findall(r"VSWR\s+;\s+(.+?)\s+;", section)

    # Create a dictionary to store the VSWR values
    vswr_data = {"vswr_values": vswr_values}

    return json.dumps(vswr_data, indent=4)  # Return JSON output

def fiber_loss(output):
    # Define the line pattern to search for
    target_line = r"DlLoss"  # Matches the specific line format for fiberloss

    # Find the starting index of the section
    start_index = output.find(target_line)

    # Check if the target line was found
    if start_index == -1:
        print("No matching line found.")
        return {}  # Return an empty dictionary if not found

    # Find the second occurrence of the separator line
    first_occurrence = output.find("---(.*?)---")
    end_index = output.find("---(.*?)---", first_occurrence + 1)

    # Extract and print the desired section
    section = output[start_index:end_index]

    # Extract fiber loss values using regex
    fiber_loss_values = re.findall(r"DlLoss\s+;\s+(.+?)\s+;", section)

    # Create a dictionary to store the fiber loss values
    fiber_loss_data = {"fiber_loss_values": fiber_loss_values}

    return json.dumps(fiber_loss_data, indent=4)  # Return JSON output


