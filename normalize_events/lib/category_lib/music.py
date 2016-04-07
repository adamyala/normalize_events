import genres


class Music(object):
    def get_categories_for_insert(self, event_string):
        result = genres.find(event_string)
        if not result:
            return ['Other']
        return result
