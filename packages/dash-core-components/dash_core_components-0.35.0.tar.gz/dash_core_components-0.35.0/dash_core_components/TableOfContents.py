# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TableOfContents(Component):
    """A TableOfContents component.
Build a table of contents list with links to the headers tag.

Keyword arguments:
- id (string; optional)
- className (string; optional): className for the top ul component.
- content_selector (string; optional): Selector to search for building the toc.
- headings (list; optional): Headings tag name to search.
The table of contents will be leveled according to the order of
the headings prop.
- table_of_contents (list; optional): The table of content in object form.
- style (dict; optional): Style of the parent <ul>
- setProps (boolean | number | string | dict | list; optional)

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, content_selector=Component.UNDEFINED, headings=Component.UNDEFINED, table_of_contents=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'content_selector', 'headings', 'table_of_contents', 'style', 'setProps']
        self._type = 'TableOfContents'
        self._namespace = 'dash_core_components'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'className', 'content_selector', 'headings', 'table_of_contents', 'style', 'setProps']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TableOfContents, self).__init__(**args)

    def __repr__(self):
        if(any(getattr(self, c, None) is not None
               for c in self._prop_names
               if c is not self._prop_names[0])
           or any(getattr(self, c, None) is not None
                  for c in self.__dict__.keys()
                  if any(c.startswith(wc_attr)
                  for wc_attr in self._valid_wildcard_attributes))):
            props_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self._prop_names
                                      if getattr(self, c, None) is not None])
            wilds_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self.__dict__.keys()
                                      if any([c.startswith(wc_attr)
                                      for wc_attr in
                                      self._valid_wildcard_attributes])])
            return ('TableOfContents(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'TableOfContents(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
