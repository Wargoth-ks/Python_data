from datetime import datetime as _dtime, timedelta as _delta

def get_birthdays_per_week(users):

    today = _dtime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    prev_sat = (today - _delta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
    prev_sun = (today - _delta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    week_delta = (today + _delta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
    w_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    b_day_dict = {day: [] for day in w_days}

    for user in users:
        b_day = user['birthday'].replace(year=today.year)
        w_day = b_day.strftime('%A')

        # If birthdays were on Saturday and Sunday, then we add them to Monday
        if b_day == prev_sun or (b_day == prev_sat and today.weekday() == 0) \
                            or (b_day == (prev_sun + _delta(days=1))):
            w_day = "Monday"

        # Check if birthdays have been already passed in current year
        elif today.replace(year=today.year, month=1, day=1) <= b_day < today \
                            and (b_day.weekday() < 5):
            continue

        # We check if the birthday will occur more than a week from now 
        elif b_day >= week_delta or (b_day.weekday() >= 5 \
                    and b_day not in [prev_sat, prev_sun]):
            continue
        
        b_day_dict[w_day].append(user['name'])

    for day in w_days:
        if b_day_dict[day]:
            print(f"{day}: {', '.join(b_day_dict[day])}")
            
    

users = [{'name': 'Sauron', 'birthday': _dtime(6, 12, 22)},
        {'name': 'Aragorn', 'birthday': _dtime(596, 8, 23)},
        {'name': 'Gimle', 'birthday': _dtime(355, 4, 26)},
        {'name': 'Legolas', 'birthday': _dtime(133, 7, 15)}]


get_birthdays_per_week(users)