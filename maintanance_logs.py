import datetime

class MaintenanceLog:
    """
    A class to store and manage maintenance logs for equipment.
    """

    def __init__(self):
        self.entries = []

    def add_entry(self, equipment_name, date, description, recommendations=""):
        """
        Adds a new maintenance entry to the log.

        Args:
            equipment_name (str): The name of the equipment.
            date (datetime.date): The date of the maintenance.
            description (str): A description of the maintenance performed.
            recommendations (str, optional): Recommendations for future maintenance. Defaults to "".
        """
        entry = {
            "equipment_name": equipment_name,
            "date": date,
            "description": description,
            "recommendations": recommendations
        }
        self.entries.append(entry)

    def get_entries(self, equipment_name=None, start_date=None, end_date=None):
        """
        Retrieves maintenance entries based on filters.

        Args:
            equipment_name (str, optional): The name of the equipment. Defaults to None.
            start_date (datetime.date, optional): The start date for the filter. Defaults to None.
            end_date (datetime.date, optional): The end date for the filter. Defaults to None.

        Returns:
            list: A list of maintenance entries matching the filters.
        """
        filtered_entries = self.entries
        if equipment_name:
            filtered_entries = [entry for entry in filtered_entries if entry["equipment_name"] == equipment_name]
        if start_date:
            filtered_entries = [entry for entry in filtered_entries if entry["date"] >= start_date]
        if end_date:
            filtered_entries = [entry for entry in filtered_entries if entry["date"] <= end_date]
        return filtered_entries

    def print_entries(self, entries):
        """
        Prints the maintenance entries in a formatted way.

        Args:
            entries (list): The list of maintenance entries to print.
        """
        for entry in entries:
            print(f"Equipment: {entry['equipment_name']}")
            print(f"Date: {entry['date'].strftime('%Y-%m-%d')}")
            print(f"Description: {entry['description']}")
            if entry['recommendations']:
                print(f"Recommendations: {entry['recommendations']}")
            print("-" * 20)

# Example usage:
maintenance_log = MaintenanceLog()

# Add some entries
maintenance_log.add_entry("Router 1", datetime.date(2023, 10, 26), "Replaced faulty power supply", "Check power supply regularly")
maintenance_log.add_entry("Switch 2", datetime.date(2023, 10, 27), "Upgraded firmware")

# Get all entries
all_entries = maintenance_log.get_entries()
maintenance_log.print_entries(all_entries)

# Get entries for a specific equipment
router_entries = maintenance_log.get_entries(equipment_name="Router 1")
maintenance_log.print_entries(router_entries)

# Get entries within a date range
entries_last_week = maintenance_log.get_entries(start_date=datetime.date(2023, 10, 20), end_date=datetime.date(2023, 10, 27))
maintenance_log.print_entries(entries_last_week)