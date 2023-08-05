"""Utility classes for convenient access of table_rows within a Snapshot."""

class TableView(list):
    """A smart representation of a sampling of rows for a Snapshot."""

    def __init__(self, snapshot, table_rows=None):
        self.snapshot = snapshot
        if table_rows is not None:
            fields_by_name = {field.name: field for field in snapshot.fields}
            self.fields = FieldList(fields_by_name[name] for name in table_rows.fields)
            idx_by_name = {name: i for i, name in enumerate(table_rows.fields)}
            super().__init__(TableRow(row, table_rows.fields, idx_by_name)
                             for row in table_rows.rows)
            self.count = table_rows.count
        else:
            self.fields = FieldList(snapshot.fields)
            self.count = None

    def refresh(self, **kwargs):
        if 'row_limit' not in kwargs:
            kwargs['row_limit'] = 200
        return self.snapshot.refresh(**kwargs).table_rows

    def __repr__(self):
        return '<{} {} snapshot={}>'.format(
            type(self).__name__, hex(id(self)), self.snapshot.id)


class TableRow:
    """A smart representation of one row in a TableView."""

    def __init__(self, values, names, idx_by_name):
        # Arbitrary fields determine attributes, so try to minimize collisions.
        self._enigma_internal_data = (values, names, idx_by_name)

    def __getitem__(self, key):
        (values, _, idx_by_name) = self._enigma_internal_data
        if hasattr(key, 'name') and isinstance(key.name, str):
            key = key.name
        if isinstance(key, str):
            idx = idx_by_name.get(key)
            if idx is None:
                raise KeyError(key)
            key = idx
        if isinstance(key, (int, slice)):
            return values[key]
        msg = '{} indices must not be {}'.format(type(self).__name__, type(key).__name__)
        raise TypeError(msg)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            msg = "'{}' object has no attribute '{}'".format(type(self).__name__, name)
            raise AttributeError(msg)

    def __iter__(self):
        (values, _, _) = self._enigma_internal_data
        return iter(values)

    def __len__(self):
        (values, _, _) = self._enigma_internal_data
        return len(values)

    def __repr__(self):
        (values, names, _) = self._enigma_internal_data
        inside = ', '.join('{}: {!r}'.format(*item) for item in zip(names, values))
        return '[{}]'.format(inside)


class FieldList(list):
    """A list of Fields that prints with indices, and supports index() with field names."""

    def index(self, field, start=None, end=None):
        if isinstance(field, str):
            name = field
        elif hasattr(field, 'name'):
            name = field.name
        else:
            raise ValueError('{!r} is not in FieldList'.format(field))
        for idx in range(len(self))[slice(start, end)]:
            if self[idx].name == name:
                return idx
        raise ValueError('{!r} is not in FieldList'.format(field))

    def __contains__(self, field):
        try:
            self.index(field)
            return True
        except ValueError:
            return False

    def __repr__(self):
        inside = ', '.join('{!r}: {!r}'.format(*item) for item in enumerate(self))
        return '[{}]'.format(inside)
