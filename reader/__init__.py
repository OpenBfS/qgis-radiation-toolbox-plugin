class ReaderBase:
    """Base reader class.
    """
    def __init__(self, filepath):
        self._filepath = filepath

        try:
            self._fd = open(self._filepath)
        except IOError as e:
            raise ReaderError("{}".format(e))

    def __del__(self):
        """Destructor, close input file.
        """
        if self._fd:
            self._fd.close()

    def count(self):
        """Count data items.
        """
        raise NotImplementedError()

    def _next_data_item(self):
        """Read next data item.
        """
        raise NotImplementedError()

    def _item2feat(self, item):
        """Create QgsFeature from data item.
        """
        raise NotImplementedError()

    def __iter__(self):
        """Loop through features.
        """
        self._reset()
        return self

    def __next__(self):
        """Return next QgsFeature.
        """
        item = self._next_data_item()
        if not item:
            raise StopIteration

        return self._item2feat(item)

    def _reset(self):
        """Reset reading.
        """
        self._fd.seek(0, 0)
