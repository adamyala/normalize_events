class Food(object):
    def __init__(self):
            self.categories = [
                'BBQ',
                'Beer',
                'Cheese',
                'Chocolate',
                'Cocktail',
                'Coffee',
                'Dinner',
                'Education',
                'Food',
                'Liquor',
                'Lunch', 
                'Spirits',
                'Whiskey',
                'Wine',
                'Vegetarian'
            ]

    def get_categories_for_insert(self, event_string):
        result = []
        for category in self.categories:
            if category.lower() in event_string.lower():
                result.append(category)
        if not result:
            return ['Other']
        return result
