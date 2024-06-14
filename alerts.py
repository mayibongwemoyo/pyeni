import re
import json

def extract_alarms_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            output = file.read()
            return extract_alarms(output)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return "File not found"
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def extract_alarms(output):
    alarms = []
    alarm_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ([Mm]) (.+?)  +(.+)"  # Refined regex
    matches = re.findall(alarm_pattern, output)

    for match in matches:
        date_time, severity, problem, cause_info = match
        alarm = {
            "date_time": date_time,
            "severity": severity.upper(),
            "problem": problem.strip(),
            "cause_info": cause_info.strip()
        }
        alarms.append(alarm)

    return json.dumps(alarms, indent=4)

# Example usage:
file_path = 'output.txt'
alarms_json = extract_alarms_from_file(file_path)
print("Extracted Alarms (JSON):")
print(alarms_json)