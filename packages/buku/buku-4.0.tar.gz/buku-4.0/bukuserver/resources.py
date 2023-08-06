from buku import BukuDb
from flask_restful import Resource


class TagList(Resource):

    def get(self):
        tags = BukuDb().get_tag_all()
        result = {'tags': tags[0]}
        return result
