from scipy.interpolate import interp1d

from .women_size_table import women_size_table

size_to_measurement = {
    key: interp1d(range(6, 26, 2), women_size_table[key], bounds_error=False)
    for key in women_size_table
}

measurement_to_size = {
    key: interp1d(women_size_table[key], range(6, 26, 2), bounds_error=False)
    for key in women_size_table
}
