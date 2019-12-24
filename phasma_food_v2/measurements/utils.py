import pandas as pd


_foods = {
    "Maize flour": "Mais",
    "Wheat": "Wheat",
    "Almond": "Almond",
    "Peanuts": "Peanuts",
    "Ready-to-eat rocket": "Rocket",
    "Ready-to-eat pineapple": "Pineapple",
    "Ready-to-eat baby spinach": "Baby spinach",
    "Ready to eat rocket salad": "Rocket",
    "Ready to eat pineapple": "Pineapple",
    "Ready to eat baby spinach": "Baby spinach",
    "Minced pork": "Minced Pork AIR",
    "Fish": "Fish",
    "Edible oils": "Edible oils",
    "Minced raw meat": "Minced raw meat",
    "Skimmed milk powder": "Skimmed milk powder",
    "Alcoholic beverages": "Alcoholic beverages"
}

_sensors = ["VIS", "FLUO", "NIR", "FUSION"]


def calculate_average(data: dict) -> dict:
    """Calculate average values for raw values.

    Parameter:
        data (dict): Measurement that is used to
        calculate average values

    Returns:
        data (dict): Measurement with additional
        data (average values)
    """
    valids = "vis", "fluo"
    keys = "rawData", "rawWhite", "rawDark"
    for valid in valids:
        for key in keys:
            if data.get(valid):
                if key in data.get(valid):
                    process = data[valid][key]
                    if process:
                        df_data = pd.DataFrame()
                        avg = []
                        for i in range(len(process)):
                            df = pd.DataFrame(process[i])
                            df_data = pd.concat([df_data, df])

                        df_data["measurement"] = pd.to_numeric(df_data["measurement"], errors="coerce")
                        result_data = df_data.groupby(["wave"]).median().to_dict("dict")
                        for k, v in result_data["measurement"].items():
                            avg.append({"wave": k, "measurement": v})
                        data[valid].update({key.replace("raw", "avg"): avg})
            else:
                continue

    return data
