

# import ipywidgets as wg
# from traitlets import observe

# from .widget_upload import FileUpload


# class FileUploadBox(wg.HBox):
#     """
#     Box widget including FilUpload and HTML to report
#     """

#     def __init__(self,
#                  accept=None,
#                  multiple=False,
#                  disabled=False,
#                  style_button=False,
#                  layout_box={},
#                  ):
#         """
#         """
#         if accept is None:
#             accept = ''

#         self.accept = accept
#         self.disabled = disabled
#         self.multiple = multiple
#         self.style_button = style_button
#         self.layout_box = layout_box

#         self.output = self.build_widget_output()
#         self.value = {}

#         self.fu = FileUpload(
#             accept=self.accept,
#             disabled=self.disabled,
#             multiple=self.multiple,
#             style_button=self.style_button,
#             output=self.output,
#             box=self,
#         )

#         super().__init__(children=[self.fu, self.output],
#                          layout=wg.Layout(**self.layout_box))

#     def build_widget_output(self):
#         """
#         """
#         widget = wg.HTML(
#             layout=wg.Layout(
#                 width='100px',
#                 margin='1px 5px 1px 5px')
#         )
#         return widget

#     @observe('accept')
#     def on_change_accept(self, change):
#         """
#         """
#         new = change['new']
#         self.fu.accept = new
