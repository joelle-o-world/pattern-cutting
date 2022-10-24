class BodyMeasurements:
    def __init__(self, size: int, waist: float, bodyRise: float, hips: float, waistToFloor: float, waistToHip: float):
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


exampleBodyMeasurements = BodyMeasurements(
    size = 12,
    waist = 680.0,
    bodyRise = 280.0,
    hips = 940.0,
    waistToFloor = 1040.0,
    waistToHip = 206.0
)
