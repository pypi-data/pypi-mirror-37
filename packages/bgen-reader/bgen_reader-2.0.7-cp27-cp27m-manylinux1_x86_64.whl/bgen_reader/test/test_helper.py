from bgen_reader._helper import genotypes_to_allele_counts, get_genotypes
from numpy.testing import assert_array_equal


def test_helper_genotypes():
    e = [
        [1, 1, 1],
        [1, 1, 2],
        [1, 2, 2],
        [2, 2, 2],
        [1, 1, 3],
        [1, 2, 3],
        [2, 2, 3],
        [1, 3, 3],
        [2, 3, 3],
        [3, 3, 3],
    ]
    assert_array_equal(get_genotypes(3, 3), e)

    e = [[1, 1], [1, 2], [2, 2], [1, 3], [2, 3], [3, 3]]
    assert_array_equal(get_genotypes(2, 3), e)


def test_helper_genotypes_to_allele_counts():
    e = [
        [3, 0, 0],
        [2, 1, 0],
        [1, 2, 0],
        [0, 3, 0],
        [2, 0, 1],
        [1, 1, 1],
        [0, 2, 1],
        [1, 0, 2],
        [0, 1, 2],
        [0, 0, 3],
    ]
    g = get_genotypes(3, 3)
    assert_array_equal(genotypes_to_allele_counts(g), e)

    g = get_genotypes(2, 3)
    e = [[2, 0, 0], [1, 1, 0], [0, 2, 0], [1, 0, 1], [0, 1, 1], [0, 0, 2]]
    assert_array_equal(genotypes_to_allele_counts(g), e)
