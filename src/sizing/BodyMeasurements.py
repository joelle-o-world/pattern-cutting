from numpy import mean

from src.sizing.women_size import measurement_to_size, size_to_measurement


class BodyMeasurements:
    def __init__(self, size=None, **kwargs):
        if size == None:
            approximations = []
            for key in kwargs:
                if key in measurement_to_size:
                    approximations.append(measurement_to_size[key](kwargs[key]))

            size = mean(approximations)

        self.size = size

        self.all = {}
        self.known = {}
        for key in kwargs:
            self.all[key] = kwargs[key]
            self.known[key] = kwargs[key]

        # Add approximations
        self.approximations = {}
        for key in size_to_measurement:
            if not key in self.known:
                y = size_to_measurement[key](size)
                self.all[key] = y
                self.approximations[key] = y

    def __str__(self):
        str = "Size {}:".format(self.size)
        deviances = self.deviances()
        for key in self.all:
            str += "\n\t{}\t= {}mm".format(key, self.all[key])
            if key in deviances and deviances[key] != 0:
                str += "\t({:+.2f}mm)".format(deviances[key])
        return str

    def deviances(self):
        return {
            key: self.all[key] - size_to_measurement[key](self.size)
            for key in size_to_measurement
        }

    @property
    def hip(self):
        "Alias for self.hips"
        return self.all["hips"]

    @property
    def body_rise(self):
        return self.all["body_rise"]

    @property
    def waist_to_hip(self):
        return self.all["waist_to_hip"]

    @property
    def waist_to_floor(self):
        return self.all["waist_to_floor"]

    @property
    def waist(self):
        return self.all["waist"]


example_body_measurements = BodyMeasurements(
    size=12,
    waist=680.0,
    body_rise=280.0,
    hips=940.0,
    waist_to_floor=1040.0,
    waist_to_hip=206.0,
)
