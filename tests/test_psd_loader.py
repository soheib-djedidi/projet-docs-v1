from facture_sfr import psd_loader


class DummyLayer:
    def __init__(self, name, bbox):
        self.name = name
        self.bbox = bbox


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
