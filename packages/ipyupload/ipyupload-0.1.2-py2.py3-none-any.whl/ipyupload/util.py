
import zlib
import ipywidgets as wg


class Util:
    """
    """

    @staticmethod
    def content_from_json(value, widget):
        """
        """
        from_json = wg.trait_types.bytes_serialization['from_json']
        output = [from_json(e, None) for e in value]

        if widget.compress_level > 0:
            output = [zlib.decompress(e) for e in output]

        return output
