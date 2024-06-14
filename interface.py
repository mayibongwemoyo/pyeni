import re
import json

def extract_sfp_rates(file_path):
    try:
        with open(file_path, 'r') as file:
            output = file.read()
            return extract_sfp_rates_from_output(output)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return "File not found"
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def extract_sfp_rates_from_output(output):
    sfp_rates = []
    rate_pattern = r"([0-9.]+G)  ;   0 ;(.+?) ;.+? ;Fru=.+? Fru=(.+)"
    matches = re.findall(rate_pattern, output)

    for match in matches:
        rate, rru, band_sector = match
        sfp_rates.append({
            "rate": rate.strip(),
            "rru": rru.strip(),
            "band_sector": band_sector.strip()
        })

    return json.dumps(sfp_rates, indent=4)

# Example usage:
file_path = 'output.txt'
sfp_rates_json = extract_sfp_rates(file_path)
print("Extracted SFP Rates (JSON):")
print(sfp_rates_json)