from hashlib import sha1
from copy import deepcopy
from banal import ensure_list
from normality import stringify

from followthemoney.exc import InvalidData
from followthemoney.types import registry
from followthemoney.property import Property
from followthemoney.link import Link
from followthemoney.util import merge_data, key_bytes


class EntityProxy(object):
    """A wrapper object for an entity, with utility functions for the
    introspection and manipulation of its properties."""

    def __init__(self, schema, data, key_prefix=None):
        self.schema = schema
        data = deepcopy(data)
        self.id = stringify(data.pop('id', None))
        self._key_prefix = key_prefix
        self._properties = data.pop('properties', {})
        self._data = data

    def make_id(self, *parts):
        digest = sha1()
        if self._key_prefix:
            digest.update(key_bytes(self._key_prefix))
        base = digest.digest()
        for part in parts:
            digest.update(key_bytes(part))
        if digest.digest() == base:
            self.id = None
            return
        self.id = digest.hexdigest()
        return self.id

    def get(self, prop):
        if not isinstance(prop, Property):
            name = prop
            prop = self.schema.get(prop)
            if prop is None:
                msg = "Unknown property (%s): %s"
                raise InvalidData(msg % (self.schema, name))
        return ensure_list(self._properties.get(prop.name))

    def add(self, prop, value, cleaned=False):
        values = self.get(prop)
        if not isinstance(prop, Property):
            prop = self.schema.get(prop)
        for val in ensure_list(value):
            if not cleaned:
                val = prop.type.clean(val, countries=self.countries)
            if val is not None and val not in values:
                values.append(val)
        self._properties[prop.name] = values

    def iterprops(self):
        for prop in self.schema.properties.values():
            yield prop

    def itervalues(self):
        for key, value in self._properties.items():
            prop = self.schema.get(key)
            for value in self.get(prop):
                yield (prop, value)

    def get_type_values(self, type_, cleaned=True):
        values = []
        for prop, value in self.itervalues():
            if prop.type == type_:
                values.append(value)
        kwargs = {'cleaned': cleaned}
        if type_ != registry.country:
            kwargs['countries'] = self.countries
        return type_.normalize_set(values, **kwargs)

    @property
    def countries(self):
        return self.get_type_values(registry.country)

    @property
    def names(self):
        return self.get_type_values(registry.name)

    @property
    def caption(self):
        for prop in self.iterprops():
            if prop.caption:
                for value in self.get(prop):
                    return value

    def get_type_inverted(self, cleaned=True):
        """Invert the properties of an entity into their normalised form."""
        data = {}
        for group, type_ in registry.groups.items():
            values = self.get_type_values(type_, cleaned=cleaned)
            if len(values):
                data[group] = values
        return data

    @property
    def links(self):
        ref = registry.entity.ref(self.id)
        for prop, value in self.itervalues():
            yield Link(ref, prop, value)

    def to_dict(self, inverted_index=False):
        data = deepcopy(self._data)
        data['id'] = self.id
        data['schema'] = self.schema.name
        data['properties'] = self._properties
        if inverted_index:
            data.update(self.get_type_inverted())
        return data

    def merge(self, other):
        model = self.schema.model
        other = self.from_dict(model, other)
        schema = model.precise_schema(self.schema, other.schema)
        schema = model.get(schema)
        data = {
            'properties': merge_data(self._properties, other._properties)
        }
        return EntityProxy(schema, data)

    def __repr__(self):
        return '<EntityProxy(%r,%r)>' % (self.id, self.schema)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def from_dict(cls, model, data):
        if isinstance(data, cls):
            return data
        schema = model.get(data.get('schema'))
        if schema is None:
            raise InvalidData('No schema for entity proxy.')
        return cls(schema, data)
