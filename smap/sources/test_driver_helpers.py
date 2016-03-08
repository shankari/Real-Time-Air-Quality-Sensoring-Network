import aqiCalculator as aqicalc

class TestClass:
	"""
	Contains the tests for all the driver helper functions used in drivers
	"""
	def test_convert_particle_count_to_aqi_pm25(self):
		"""
		This test checks if convert particle count to aqi function works correctly for PM2.5
		"""
		assert aqicalc.convert_particle_count_to_aqi(3780,'pm2.5') == 19

	def test_convert_particle_count_to_aqi_pm10(self):
		"""
		This test checks if convert particle count to aqi function works correctly for PM10
		"""
		assert aqicalc.convert_particle_count_to_aqi(244,'pm10') == 102