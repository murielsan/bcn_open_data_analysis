# Get values for O3
def get_o3_val(value):
    if value > 240:
        return -2
    elif value > 180:
        return -1
    elif value > 110:
        return 0
    else: return 1   


# Get values for NO2
def get_no2_val(value):
    if value > 400:
        return -2
    elif value > 200:
        return -1
    elif value > 90:
        return 0
    else: return 1


# Get values for PM10
def get_pm10_val(value):
    if value > 75:
        return -2
    elif value > 50:
        return -1
    elif value > 35:
        return 0
    else: return 1


# Define a function to calculate ICQA element quality
def get_icqa(element, value):
    try:
        match element:
            case "O3":
                get_o3_val(value)
            case "NO2":
                get_no2_val(value)
            case "PM10":
                get_pm10_val(value)
    except TypeError:
        return 0


# Function to calculate air quality
def get_air_quality(o3,no2,pm10):
    # If None, put a value to return 1
    total = get_icqa("O3",float(0 if o3 is None else o3)) + get_icqa("NO2",float(0 if no2 is None else no2)) + get_icqa("PM10",float(0 if pm10 is None else pm10))
    if total == 3:
        return "Good"
    elif total > 0:
        return "Moderate"
    else: return "Poor"