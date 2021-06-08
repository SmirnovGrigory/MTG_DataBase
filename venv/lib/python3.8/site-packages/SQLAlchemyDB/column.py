from sqlalchemy import Column, ForeignKey, Sequence


class DBColumn:
    """ Specifies configuration for a SQLAlchemy Column. """

    def __init__(self, name, pg_type):
        self.name = name
        self.type_ = pg_type
        self.primary_key = False
        self.foreign_key = None
        self.nullable = False
        self.index = False
        self.unique = None

    def create(self, metadata=None, table_name=None):
        args = {'name': self.name, 'type_': self.type_, 'primary_key': self.primary_key,
                'nullable': self.nullable, 'index': self.index}
        if self.unique is not None:
            args['unique'] = self.unique

        extra_args = []
        if not (metadata is None or table_name is None):
            extra_args.append(Sequence(table_name + '_seq', metadata=metadata))
        if self.foreign_key is not None:
            extra_args.append(ForeignKey(self.foreign_key))

        return Column(**args) if len(extra_args) == 0 else Column(*extra_args, **args)

    def as_foreign_key(self, foreign_key):
        self.foreign_key = foreign_key
        return self

    def as_index(self):
        self.index = True
        return self

    def as_nullable(self):
        self.nullable = True
        return self

    def as_primary_key(self):
        self.primary_key = True
        return self

    def as_unique(self):
        self.unique = True
        return self
