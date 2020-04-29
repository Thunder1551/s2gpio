import Python_BMP.BMP085 as BMP085

# If bmp180 sensor is stardard attached to i2c, default address is 0x77


def read_sensor():
    sensor = BMP085.BMP085()
    return sensor.read_pressure(), sensor.read_altitude()
