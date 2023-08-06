from flask_sqlalchemy import SQLAlchemy


class ForeignKey:
    def __init__(self, db, app=None):
        self.app = app
        self.db = db
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # app.config.setdefault('', '')
        # app.teardown_appcontext(self.teardown)
        pass

    def has_attr(self, table):
        def ref_table(cls, db=self.db):
            setattr(cls, table + 's',
                    db.relationship(table.capitalize(), back_populates=cls.__name__.lower()))
            return cls

        return ref_table

    def attr_to(self, table):
        def ref_table(cls, db=self.db):
            setattr(cls, '{0}_id'.format(table),
                    db.Column(db.String(50), db.ForeignKey('{0}.id'.format(table))))
            setattr(cls, table, db.relationship(table.capitalize(), back_populates=cls.__name__.lower() + 's'))
            return cls

        return ref_table

    def tag_to(self, table):
        def ref_table(cls, db=self.db):
            table_name_1 = table
            table_name_2 = cls.__name__.lower()

            if table_name_1 > table_name_2:
                association_table_name = "_%s_%s" % (table_name_1, table_name_2)
            else:
                association_table_name = "_%s_%s" % (table_name_2, table_name_1)

            association_table = db.Table(association_table_name, db.metadata,
                                         db.Column("%s_id" % table_name_1, db.String(50),
                                                   db.ForeignKey('%s.id' % table_name_1),
                                                   primary_key=True),
                                         db.Column("%s_id" % table_name_2, db.String(50),
                                                   db.ForeignKey('%s.id' % table_name_2),
                                                   primary_key=True),
                                         extend_existing=True
                                         )

            setattr(cls, table + 's', db.relationship(table.capitalize(),
                                                      secondary=association_table,
                                                      back_populates=cls.__name__.lower() + 's'))
            return cls

        return ref_table