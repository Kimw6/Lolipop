import pytest
import pandas
from clustering import filters
from import_data import import_table_from_string

@pytest.fixture
def genotypes()->pandas.DataFrame:
	genotype_table_string = """
		Genotype	0	17	25	44	66	75	90
		genotype-1	0	0	0.261	1	1	1	1
		genotype-2	0	0.38	0.432	0	0	0	0
		genotype-3	0	0	0	0	0	1	1
		genotype-4	0	0	0	0.525	0.454	0.911	0.91
		genotype-5	0	0	0	0.147	0.45	0.924	0.887
		genotype-6	0	0	0	0.273	0.781	1	1
		genotype-7	0	0	0	0.188	0.171	0.232	0.244
		genotype-8	0	0	0	0.403	0.489	0.057	0.08
		genotype-9	0	0	0.117	0	0	0	0.103
		genotype-10	0	0	0	0.138	0.295	0	0.081
		genotype-11	0	0	0	0	0.278	0.822	0.803
		genotype-12	0	0	0	0	0.2335	0.133	0.0375
		genotype-13	0	0	0.033	0.106	0.1065	0	0
		genotype-14	0	0	0	0	0	0.2675	0.326
		genotype-15	0	0	0	0.1145	0	0.1205	0.0615
	"""
	t = import_table_from_string(genotype_table_string, index = 'Genotype')
	t = t.astype(float)
	return t

def test_remove_single_point_series():
	table = pandas.DataFrame([
		[0,0,0,1,0,0],
		[1,3,2,0,1,1],
		[0.03, 1,0,0,0,0]
	])
	single_point_series = filters._remove_single_point_background(table, 0.03, 0.97)

	assert [0] == list(single_point_series)

	single_point_series = filters._remove_single_point_background(table, 0.04, 0.97)

	assert [0, 2] == list(single_point_series)

def test_get_first_timepoint_above_cutoff():
	series =pandas.Series([0, .03, .04, .1, .2, .3, .4, .5, .6, .7, .8])

	assert 2 == filters.get_first_timepoint_above_cutoff(series, 0.03)
	assert 4 == filters.get_first_timepoint_above_cutoff(series, 0.1)
	assert 1 == filters.get_first_timepoint_above_cutoff(series, 0)

def test_get_fuzzy_backgrounds(genotypes):
	cutoffs = [0.9]
	expected = """
		Genotype	0	17	25	44	66	75	90
		genotype-1	0	0	0.261	1	1	1	1
		genotype-4	0	0	0	0.525	0.454	0.911	0.91
		genotype-5	0	0	0	0.147	0.45	0.924	0.887
		genotype-6	0	0	0	0.273	0.781	1	1"""
	expected_table = import_table_from_string(expected, index = 'Genotype')
	backgrounds, (fuzzy_detected_cutoff, fuzzy_fixed_cutoff) = filters.get_fuzzy_backgrounds(genotypes, cutoffs)
	expected_table = expected_table.astype(float)
	assert pytest.approx(fuzzy_fixed_cutoff == 0.9)
	assert pytest.approx(fuzzy_detected_cutoff == 0.1)

	pandas.testing.assert_frame_equal(expected_table, backgrounds)

