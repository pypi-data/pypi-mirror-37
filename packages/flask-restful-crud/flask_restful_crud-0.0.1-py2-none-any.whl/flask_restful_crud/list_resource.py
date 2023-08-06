import json
from sqlalchemy import desc, asc
from flask_restful import marshal, request, reqparse, Resource, fields


class ListResource(Resource):
    model: object
    db: object
    fields: dict
    parser = reqparse.RequestParser()
    page_count = 5

    def __init__(self):
        super().__init__()
        self.query = self.model.query
        self.init_parser()
        self.init_fields()

    def get(self):
        self.apply_filters()
        self.apply_sorting()
        response_data = self.apply_pagination(self.query, self.parser)
        return marshal(response_data, self.response_fields)

    def post(self):
        element = self.model(**request.json)

        self.db.session.add(element)
        self.db.session.commit()
        return marshal(element, self.fields)

    def apply_pagination(self, query, parser):
        pagination = json.loads(parser.parse_args().get('pagination'))

        return query.paginate(
            pagination.get('page', 1),
            pagination.get('count', self.page_count)
        )

    def init_parser(self):
        self.parser.add_argument('filters', type=str, default='[]')
        self.parser.add_argument(
            'pagination',
            type=str,
            default=f'{{"page": 1, "count": {self.page_count}}}'
        )
        self.parser.add_argument('sorting', type=str, default='{}')

    def init_fields(self):
        self.response_fields = {
            'items': fields.List(fields.Nested(self.fields)),
            'pages': fields.Integer,
            'page': fields.Integer
        }

    def apply_filters(self):
        filters = self.parser.parse_args().get('filters')
        print(filters)

        for filter in json.loads(filters):
            key = filter.get('key')
            value = filter.get('value')
            method = filter.get('operator')

            if not value:
                continue

            # start with helper
            if method == 'startWith':
                method = 'ilike'
                value = f'{value}%'

            # content helper
            if method == 'content':
                method = 'ilike'
                value = f'%{value}%'

            column = getattr(self.model, key, None)
            operator = getattr(column, method, None)

            if operator:
                self.query = self.query.filter(operator(value))

            if method == '==':
                self.query = self.query.filter(column == value)
            if method == '>=':
                self.query = self.query.filter(column >= value)
            if method == '>':
                self.query = self.query.filter(column > value)
            if method == '<=':
                self.query = self.query.filter(column <= value)
            if method == '<':
                self.query = self.query.filter(column < value)
            if method == '!=':
                self.query = self.query.filter(column != value)

    def apply_sorting(self):
        sorting = json.loads(self.parser.parse_args().get('sorting'))

        if sorting:
            key = sorting.get('key')
            order = {'desc': desc, 'asc': asc}.get(sorting.get('order'))
            column = getattr(self.model, key, None)

            self.query = self.query.order_by(order(column))
