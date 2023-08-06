
import ipywidgets as wg


class Util:
    """
    """

    @staticmethod
    def content_from_json(value, widget):
        """
        """
        from_json = wg.trait_types.bytes_serialization['from_json']
        return [from_json(e, None) for e in value]
