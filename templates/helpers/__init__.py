from datetime import datetime


def format_timestamp(timestamp):
    now = datetime.today()
    date = datetime.fromtimestamp(timestamp)
    if date.date() == now.date():
        return date.strftime('Today at %I:%M %p')
    else:
        return date.strftime('%b %d, %Y at %I:%M %p')
