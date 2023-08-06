from marshmallow import Schema


class BaseSchema(Schema):
    def load_row(self, columns, row):
        data = dict(zip(columns, row))
        return self.load(data)
