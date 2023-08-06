# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TableInfo(Component):
    """A TableInfo component.
TableInfo is a component that digest metadata info and handle event of graph figure.

Keyword arguments:
- id (string; optional)
- graph (string; optional): The id of graph figure
- cell (string; optional): The target cell type
- clickData (dict; optional): Data from latest click event

Available events: """
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, graph=Component.UNDEFINED, cell=Component.UNDEFINED, clickData=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'graph', 'cell', 'clickData']
        self._type = 'TableInfo'
        self._namespace = 'dashx'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['id', 'graph', 'cell', 'clickData']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TableInfo, self).__init__(**args)

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
            return ('TableInfo(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'TableInfo(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')
