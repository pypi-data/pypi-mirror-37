
class ProbaTable(object):
    def __init__(self, events, values):
        super(ProbaTable, self).__init__()
        assert values.ndim == 2, \
            "\"values\" must be a 2D array!"
        assert len(events) == values.shape[1], \
            "Number of events must be equal number of columns in the values"

        self.events = events
        self.values = values

        if values.dtype.kind in ["b", "f"]:
            self.values = values
        elif values.dtype.kind == "i":
            self.values = values.astype(bool)
        else:
            raise ValueError("Unknown values type: \"{}\"".format(values.dtype))

        self.event_index = {event: i for i, event in enumerate(events)}

    def __call__(self, event):
        return event(self).mean()
