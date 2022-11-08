class BodyMeasurements:
    def __init__(
        self,
        size: int,
        waist: float,
        bodyRise: float,
        hips: float,
        waistToFloor: float,
        waistToHip: float,
    ):
        if size == None:
            # TODO If to size is given, approximate from other measurements
            pass

        self.size = size
        self.waist = waist
        self.bodyRise = bodyRise
        self.hips = hips
        self.waistToFloor = waistToFloor
        self.waistToHip = waistToHip

    @property
    def hip(self):
        "Alias for self.hips"
        return self.hips


from src.geometry.XYGraph import x

size_to_bust = x * 4 + 52
size_to_waist = x * 4 + 36
size_to_low_waist = x * 4 + 46
size_to_hips = x * 4 + 60


exampleBodyMeasurements = BodyMeasurements(
    size=12,
    waist=680.0,
    bodyRise=280.0,
    hips=940.0,
    waistToFloor=1040.0,
    waistToHip=206.0,
)
