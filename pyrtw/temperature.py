import rom
import time


class Temperature(rom.Model):
    city = rom.String(required=True, unique=True, suffix=True)
    temperature = rom.Float(default=time.time)
    created_at = rom.Float(default=time.time)


if __name__ == '__main__':
	temp = Temperature.get_by(city='Haifa')
	if temp:
		temp.temperature = 20
	else:
		temp = Temperature(city='Haifa', temperature=10)
	temp.save()