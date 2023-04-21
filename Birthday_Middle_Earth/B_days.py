from datetime import datetime as _dtime, timedelta as _delta

def get_birthdays_per_week(users):
    today = _dtime.now()
    next_week = today + _delta(days=7)
    w_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    b_day_dict = {day: [] for day in w_days}

    for user in users:
        b_day = user['birthday'].replace(year=today.year)
        if b_day < today:
            b_day = b_day.replace(year=today.year+1)
        elif b_day > next_week:
            b_day = b_day.replace(year=today.year-1)
        w_day = b_day.strftime('%A')
        if w_day in ['Saturday', 'Sunday']:
            w_day = 'Monday'
        b_day_dict[w_day].append(user['name'])

    for day in w_days:
        if b_day_dict[day]:
            print(f"{day}: {', '.join(b_day_dict[day])}")

            
    

users = [{'name': 'Sauron', 'birthday': _dtime(6, 12, 22)},
        {'name': 'Aragorn', 'birthday': _dtime(596, 8, 23)},
        {'name': 'Gimle', 'birthday': _dtime(355, 4, 26)},
        {'name': 'Legolas', 'birthday': _dtime(133, 7, 15)}]


get_birthdays_per_week(users)