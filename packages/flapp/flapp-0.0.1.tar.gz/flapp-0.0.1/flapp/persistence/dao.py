class AbstractDAO:
    __table_name__ = None
    __fields__ = None
    __mapper__ = None

    def __init__(self, cursor_factory):
        self.__cursor_factory = cursor_factory

    def add(self, entity):
        with self.with_cursor(True) as cur:
            cur.execute(
                'INSERT INTO "{}" ({}) VALUES ({})'.format(
                    self.__table_name__,
                    ', '.join( ('"{}"'.format(x) for x in self.__fields__) ),
                    ', '.join( ('%s', ) * len(self.__fields__) )
                ),
                self.__mapper__.map_to_db_values(entity)
            )

    def update(self, entity):
        with self.with_cursor(True) as cur:
            db_values = self.__mapper__.map_to_db_values(entity)
            db_values = db_values[1:] + (db_values[0], )

            cur.execute(
                'UPDATE "{}" SET {} WHERE "id" = %s'.format(
                    self.__table_name__,
                    ', '.join( ('"{}" = %s'.format(x) for x in self.__fields__) )
                ),
                db_values
            )

    def remove(self, entity_or_id):
        if type(entity_or_id) != int:
            entity_id = self.__mapper__.map_to_db_values(entity_or_id)[0]
        else:
            entity_id = entity_or_id

        with self.with_cursor(True) as cur:
            cur.execute(
                'DELETE FROM "{}" WHERE "id" = %s'.format(self.__table_name__),
                entity_id
            )

    def with_cursor(self, commit=False):
        return self.__cursor_factory(commit)

    def map(self, result):
        if result is None:
            return None
        elif type(result) == list:
            return [ self.__mapper__.map_to_object(x) for x in result ]
        else:
            return self.__mapper__.map_to_object(result)
