

class Params:
    """
    Validating input parameters and building jsons for chart init

    -----
    Attributes:

    obj: a Chart object whose attributes will be checked and built by BuilderParams.
    """

    def __init__(self,
                 obj):
        """
        """
        self.obj = obj

    def valid(self):
        """
        Checks if the values for the given entries are valid.
        """
        msg = 'width must be an int (number of pixels) or a string'
        assert (isinstance(self.obj.width_in, int)
                or isinstance(self.obj.width_in, str)), msg

        msg = 'height must be an int (number of pixels)'
        assert isinstance(self.obj.height_in, int), msg

        li_theme = ['dark-unica',
                    'grid-light',
                    'sand-signika',
                    '']
        # Empty string is a valid theme
        msg = 'theme must be one of {}'.format(li_theme)
        assert self.obj.theme in li_theme, msg

    def build(self):
        """
        Builds parameters of the chart
        """

        # Convert width to string
        if isinstance(self.obj.width_in, int):
            self.obj.width = str(self.obj.width_in) + 'px'
        else:
            self.obj.width = self.obj.width_in

        # Height
        if self.obj.height_in == 0:
            self.obj.height_in = 350
        self.obj.height = str(self.obj.height_in) + 'px'
