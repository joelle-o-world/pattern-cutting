# All measurements here are in cm
# Source: Winnfred Owen page 13
women_size_table_cm = {
    "bust": [76, 80, 84, 88, 92, 96, 100, 104, 110, 116, 122],
    "waist": [60, 64, 68, 72, 76, 80, 84, 88, 94, 100, 106],
    "low_waist": [70, 74, 78, 82, 86, 90, 94, 98, 104, 110, 116],
    "hips": [84, 88, 92, 96, 100, 104, 108, 112, 117, 122, 127],
    "back_width": [31.4, 32.4, 33.4, 34.4, 35.4, 36.4, 37.4, 38.4, 39.8, 41.2, 42.6],
    "chest": [28.8, 30, 31.2, 32.4, 33.6, 34.8, 36, 37.2, 39, 40.8, 42.6],
    "shoulder": [11.5, 11.75, 12, 12.25, 12.5, 12.75, 13, 13.25, 13.6, 13.9, 14.2],
    "neck_size": [34, 35, 36, 37, 38, 39, 40, 41, 42.4, 43.8, 45.2],
    "dart": [5.2, 5.8, 6.4, 7, 7.6, 8.2, 8.8, 9.4, 10, 10.6, 11.2],
    "top_arm": [24.8, 26, 27.2, 28.4, 29.6, 30.8, 32, 33.2, 35.2, 37.2, 39.2],
    "wrist": [14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.7, 19.4, 20.1],
    "ankle": [22.5, 23, 23.5, 24, 24.5, 25, 25.5, 26, 26.7, 27.4, 28.1],
    "high_ankle": [19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.7, 24.4, 25.1],
    "nape_to_waist": [39.8, 40.2, 40.6, 41, 41.4, 41.8, 42.2, 42.6, 43, 43.4, 43.8],
    "front_shoulder_to_waist": [
        39.8,
        40.2,
        40.6,
        41,
        41.4,
        42.3,
        43.2,
        44.1,
        45,
        45.9,
        46.8,
    ],
    "armscye_depth": [19.8, 20.2, 20.6, 21, 21.4, 21.8, 22.2, 22.6, 23.2, 23.8, 24.4],
    "waist_to_knee": [57, 57.5, 58, 58.5, 59, 59.5, 60, 60.5, 61, 61.5, 62],
    "waist_to_hip": [19.7, 20, 20.3, 20.6, 20.9, 21.2, 21.5, 21.8, 22.1, 22.4, 22.7],
    "waist_to_floor": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
    "body_rise": [25.9, 26.6, 27.3, 28, 28.7, 29.4, 30.1, 30.8, 31.8, 32.8, 33.8],
    "sleeve_length": [57, 57.5, 58, 588.5, 59, 59.5, 60, 60.25, 60.5, 60.75, 61],
    "sleeve_length_jersey": [53, 53.5, 54, 54.5, 55, 55.5, 56, 56.25, 56.5, 56.75, 57],
    "cuff_size_shirts": [20.5, 21, 21, 21.5, 21.5, 22, 22.5, 23, 23.5, 24, 24.5],
    "cuff_size_two_piece_sleeve": [
        13,
        13.25,
        13.5,
        13.75,
        14,
        14.25,
        14.5,
        14.75,
        15,
        15.25,
        15.5,
    ],
    "trouser_bottom_width": [20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25, 25.5],
    "jeans_bottom_width": [18, 18.5, 18.5, 19, 19, 19.5, 19.5, 20, 20, 21, 21],
}

women_size_table = {
    key: [measurement * 10.0 for measurement in women_size_table_cm[key]]
    for key in women_size_table_cm
}

from scipy.interpolate import interp1d

size_to_measurement = {
    key: interp1d(
        range(6, 27, 2),
        women_size_table[key],
        bounds_error=False,
        fill_value="extrapolate",
    )
    for key in women_size_table
}

measurement_to_size = {
    key: interp1d(
        women_size_table[key],
        range(6, 27, 2),
        bounds_error=False,
        fill_value="extrapolate",
    )
    for key in women_size_table
}
