import calendar

def calculate_age(date1, date2):
    return date2.year - date1.year - ((date2.month, date2.day) < (date1.month, date1.day))
    
def calculate_months_of_age(date1, date2):
    def is_last_day_of_the_month(date):
        days_in_month = calendar.monthrange(date.year, date.month)[1]
        return date.day == days_in_month
    imaginary_day_2 = 31 if is_last_day_of_the_month(date2) else date2.day
    monthdelta = ((date2.month - date1.month) + (date2.year - date1.year) * 12 +(-1 if date1.day > imaginary_day_2 else 0))
    return monthdelta

def calculate_days_of_age(date1, date2):
    return (date2 - date1).days

def calculate_bmi(weight, height):
    return round(weight / height ** 2, 1)
