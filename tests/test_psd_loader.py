from facture_sfr import psd_loader


class DummyLayer:
    def __init__(self, name, bbox):
        self.name = name
        self.bbox = bbox


    @property
    def width(self):
        return self.bbox[2] - self.bbox[0]

    @property
    def height(self):
        return self.bbox[3] - self.bbox[1]


class DummyPSD:
    def __init__(self, layers):
        self._layers = layers

    def descendants(self):
        return self._layers


def test_get_layer_bbox_returns_tuple():
    psd = DummyPSD([DummyLayer("a", (1, 2, 3, 4))])
    assert psd_loader.get_layer_bbox(psd, "a") == (1, 2, 3, 4)


def test_get_layer_bbox_raises_when_missing():
    psd = DummyPSD([])
    try:
        psd_loader.get_layer_bbox(psd, "x")
    except psd_loader.LayerNotFoundError:
        assert True
    else:
        assert False


def test_find_layer_prefers_largest_bbox_when_duplicate():
    psd = DummyPSD(
        [
            DummyLayer("x", (0, 0, 10, 10)),
            DummyLayer("x", (0, 0, 20, 20)),
        ]
    )
    bbox = psd_loader.get_layer_bbox(psd, "x")
    assert bbox == (0, 0, 20, 20)


def test_find_layer_can_select_occurrence():
    psd = DummyPSD(
        [
            DummyLayer("x", (0, 0, 10, 10)),
            DummyLayer("x", (5, 5, 15, 15)),
        ]
    )
    bbox = psd_loader.get_layer_bbox(psd, "x", occurrence=0)
    assert bbox == (0, 0, 10, 10)
    bbox_second = psd_loader.get_layer_bbox(psd, "x", occurrence=1)
    assert bbox_second == (5, 5, 15, 15)
