from flask_restful import fields


class SearchIdField(fields.Raw):
    def output(self, key, obj):
        return obj.search_id or obj.id


song_list_marshal = {
    'title': fields.String,
    'artist': fields.String,
    'album': fields.String,
    'duration': fields.String,
    'available': fields.Boolean,
}

song_search_marshal = {
    'search_id': SearchIdField,
    'search_key': fields.String,
    'title': fields.String,
    'duration': fields.String,
    'available': fields.Boolean,
    'source': fields.String
}

playlist_detail_marshal = {
    'id': fields.String,
    'name': fields.String,
    'is_playing': fields.Boolean,
    'is_default': fields.Boolean,
    'songs_count': fields.Integer,
}

user_detail_marshal = {
    'id': fields.String,
    'username': fields.String,
    'is_superuser': fields.Boolean,
}
