import json
import requests
from icalendar import Calendar

config = None

def load_config():
    config_l = None

    # read
    with open('config.json') as f:
        config_l = json.load(f)

    # void filters
    for course in config_l['courses']:
        course['filters'] = []
    return config_l

def download_calendar(link):
    req = requests.get(link)
    if req.status_code != 200:
        exit(100)
    return req.text

def load_calendar(ics_cal):
    return Calendar.from_ical(ics_cal)

def parse_ics(cal):
    return cal.to_ical()

def filter(course):
    global config
    def add_filter(func):
        # add to filters
        for conf_course in config['courses']:
            if conf_course['id'] == course:
                conf_course['filters'].append(func)
                break
        else:
            exit(101)
        return func
    return add_filter

def process_calendars(cals_id):
    global config

    # init
    config = load_config()
    load_filters()

    # load calendar
    ics = download_calendar(config['link'])
    cal = load_calendar(ics)
    new_cal = cal.copy()

    # filter
    for cal_id in cals_id:
        # get config
        course_config = None
        for course in config['courses']:
            if course['id'] == cal_id:
                course_config = course
                break
        else:
            exit(102)

        # filter events
        for event in cal.subcomponents:
            if event['summary'] == course_config['summary']:
                # apply filters
                new_event = event
                for filter in course_config['filters']:
                    new_event = filter(new_event)
                    if new_event is None:
                        break
                else:
                    new_cal.add_component(event)
    
    return parse_ics(new_cal)

### START FILTERS ###

def load_filters():
    
    @filter('1_GAL')
    def filter_september(event):
        # print(event['DTSTART'])
        return None

#####################

if __name__ == '__main__':
    out = process_calendars(['1_GAL']).decode('utf-8')
    print(out)
