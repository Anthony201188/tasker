from datetime import datetime

##untested filtering of .txt doc data

def parse_entry(entry):
    parts = entry.split("|")
    name = parts[0]
    content = parts[1].split(":")[1]
    status, date_str, time_str = parts[2].split(",")[1:]
    date_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M:%S")
    return {"name": name, "content": content, "status": status, "date_time": date_time}

def filter_by_name(data, name):
    return [entry for entry in data if parse_entry(entry)["name"] == name]

def filter_by_date(data, target_date):
    target_date = datetime.combine(target_date, datetime.min.time())
    return [entry for entry in data if parse_entry(entry)["date_time"].date() == target_date.date()]

def filter_by_date_range(data, start_date, end_date):
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.max.time())
    return [entry for entry in data if start_date <= parse_entry(entry)["date_time"] <= end_date]

# Example usage
data = [
    "habit1|content:\"habit1\"|S,28-11-2023,16:18:19|",
    "habit2|content:\"habit2\"|S,28-11-2023,16:18:19|",
    # ... other entries
]

filtered_by_name = filter_by_name(data, "habit1")
filtered_by_date = filter_by_date(data, datetime(2023, 11, 28))
filtered_by_date_range = filter_by_date_range(data, datetime(2023, 11, 28), datetime(2023, 11, 30))

####################################################################

def filter_by_name_and_status_and_date_range(data, name, status, start_date, end_date):
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.max.time())
    
    return [
        entry for entry in data
        if (
            parse_entry(entry)["name"] == name
            and parse_entry(entry)["status"] == status
            and start_date <= parse_entry(entry)["date_time"] <= end_date
        )
    ]

# Example usage
filtered_data = filter_by_name_and_status_and_date_range(
    data, name="habit1", status="S", start_date=datetime(2023, 11, 28), end_date=datetime(2023, 11, 30)
)
