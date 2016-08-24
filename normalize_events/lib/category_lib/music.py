import genres


class Music(object):
    @staticmethod
    def get_categories_for_insert(event_string):
        result = genres.find(event_string)
        if not result:
            return ['Other']
        return result
