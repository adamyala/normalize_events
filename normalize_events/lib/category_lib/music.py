import genres


class Music(object):
    def get_categories_for_insert(self, event_string):
        result = genres.find(event_string)
        if result == []:
            return ['Other']
        return result
