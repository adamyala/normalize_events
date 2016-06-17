
DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'database': 'events'
    }

# Food, Music
CATEGORY = ''

CLIENT_EB = {
    'token': '',
    'url': 'https://www.eventbriteapi.com/v3',
    'location_address': 'Chicago,IL',
    'location_within': '25mi',
    'categories': {
        'Business': '101',
        'Music': '103',
        'Film': '104',
        'Arts': '105',
        'Fashion': '106',
        'Sports': '108',
        'Health': '107',
        'Science': '102',
        'Outdoor': '109',
        'Food': '110',
        'Charity': '111',
        'Government': '112',
        'Community': '113',
        'Spirituality': '114',
        'Education': '115',
        'Holiday': '116',
        'Lifestyle': '117',
        'Auto': '118',
        'Hobbies': '119',
        'Other': '199',
    },
}
CLIENT_BPT = {
    'token': '',
    'url': 'https://www.brownpapertickets.com',
    'state': 'IL',
    'country': 'United States',
    'category_id': {
        'Arts': '100001',
        'Comedy': '100009',
        'Education': '100012',
        'Film': '100002',
        'Food': '100010',
        'Music': '100003',
        'Social': '200109',
        'Sports': '100004',
        'Other': '100006',
    },
}
CLIENT_MU = {
    'token': '',
    'url': 'https://api.meetup.com',
    'state': 'IL',
    'category': {
        'Arts': '1',
        'Business': '2',
        'Auto': '3',
        'Community': '4',
        'Dancing': '5',
        'Education': '6',
        'Fashion': '7',
        'Fitness': '8',
        'Food': '9',
        'Games': '10',
        'Movements': '11',
        'Health': '12',
        'Crafts': '13',
        'Languages': '14',
        'LGBT': '15',
        'Lifestyle': '16',
        'Literature': '17',
        'Films': '18',
        'Music': '21',
        'Spirituality': '20',
    },
}
CLIENT_EF = {
    'token': '',
    'url': 'http://api.eventful.com/json/events/search',
    'location': 'Chicago',
    'category': {
        'Music': 'music',
        'Comedy': 'comedy',
        'Learning Education': 'learning_education',
        'Family Fun Kids': 'family_fun_kids',
        'Festivals Parades': 'festivals_parades',
        'Movies Film': 'movies_film',
        'Food': 'food',
        'Fundraisers': 'fundraisers',
        'Art': 'art',
        'Support': 'support',
        'Holiday': 'holiday',
        'Books': 'books',
        'Attractions': 'attractions',
        'Community': 'community',
        'Business': 'business',
        'Singles Social': 'singles_social',
        'Schools Alumni': 'schools_alumni',
        'Clubs Associations': 'clubs_associations',
        'Outdoors Recreation': 'outdoors_recreation',
        'Performing Arts': 'performing_arts',
        'Animals': 'animals',
        'Politics Activism': 'politics_activism',
        'Sales': 'sales',
        'Science': 'science',
        'Religion Spirituality': 'religion_spirituality',
        'Sports': 'sports',
        'Technology': 'technology',
        'Other': 'other',
    },
}
CLIENT_GM = {
    'token': '',
    'url': 'https://maps.googleapis.com/',
    'on': False,
}

USERS = [
    {
        'USER_NAME': 'ADD USER HERE',
        'PASSWORD': 'ADD SECRET KEY'
    }
]
