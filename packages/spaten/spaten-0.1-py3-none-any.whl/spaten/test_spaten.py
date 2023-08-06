from spaten import Feature, File


def test_parse():
    with File('spaten/testfiles/polygon.spaten') as f:
        for feature in f:
            assert isinstance(feature, Feature)

    with File('spaten/testfiles/two_blocks.spaten') as f:
        for feature in f:
            print(feature)
            assert isinstance(feature, Feature)
