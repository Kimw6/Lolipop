import pytest
from muller.graphics.generate_muller_plot import *
def test_relocate_point_simple():

	point = (.1, .613)
	locations = [(.1, .626), (5, .35)]

	expected_point = (.6, .513)
	result_point = relocate_point(point, locations)
	assert pytest.approx(expected_point, result_point)

def test_relocate_point_complex():
	point = (0.1, 0.426)
	locations = [
		(1.0, 0.154),
		(6.0, 0.0821442859047873),
		(0.1, 0.3475000000000004),
		(1.0, 0.26),
		(1.0, 0.4985),
		(4.5, 0.8981050818260126),
		(0.1, 0.6129285714285719)
	]
	expected_point = (.6, .726)
	result_point = relocate_point(point, locations)

	assert pytest.approx(expected_point, result_point)

def test_get_font_properties():

	expected_result = {
		'size': 9,
		'color': '#333333'
	}

	assert get_font_properties("#99d8c9") == expected_result

	assert get_font_properties("#00441b")['color'] == '#FFFFFF'

def test_find_closest_point():
	point = (10, 15)

	points = [(0,1), (10,10), (11,11), (12,12)]
	assert find_closest_point(point, points) == (12,12)
def test_unique_everseen():
	assert list(unique_everseen("AABBCCCADAACCFD")) == "A B C D F".split()
