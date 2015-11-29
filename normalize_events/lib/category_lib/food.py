class Food(object):
    def __init__(self):
            self.categories = [
                'Beer', 'Cheese', 'Chocolate', 'Cocktail', 'Coffee',
                'Dinner', 'Education', 'Food', 'Liquor', 'Other',
                'Spirits', 'Whiskey', 'Wine',
            ]

    def get_categories_for_insert(self, event_string):
        result = []
        for category in self.categories:
            if category.lower() in event_string.lower():
                result.append(category)
        if result == []:
            return ['Other']
        return result
