from flask_restful import marshal, request, Resource, fields


class DetailResource(Resource):
    model: object
    db: object
    fields: dict
    associated = {}
    nested = []

    def __init__(self):
        super().__init__()

    def get(self, id):
        element = self.model.query.get(id)
        if not element:
            return {'message': 'Not found'}, 404

        return marshal(element, self.fields)

    def delete(self, id):
        element = self.model.query.get(id)
        self.db.session.delete(element)
        self.db.session.commit()
        return {
            'message': 'success',
            'id': id
        }, 200

    def put(self, id):
        self.query = self.model.query.filter_by(id=id)
        self.update_nested()
        self.update_associated()
        self.query.update(request.json)

        self.db.session.commit()
        return marshal(self.query.first(), self.fields)

    def update_associated(self):
        for field, model in self.associated.items():
            field_data = request.json.get(field)
            ids = [el.get('id') for el in field_data]
            item = self.query.first()
            values = model.query.filter(model.id.in_(ids)).all()
            setattr(item, field, values)
            del request.json[field]

    def update_nested(self):
        for field in self.nested:
            field_data = request.json.get(field)
            self.query.update({f'{field}_id': field_data.get('id') or None})
            del request.json[field]
