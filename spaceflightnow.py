import requests
from bs4 import BeautifulSoup

SPACE_FLIGHT_NOW_LAUNCH_SCHEDULE_URL = 'https://spaceflightnow.com/launch-schedule/'


def missions_payload(missions, mission_data):
    payload = []
    for index, mission in enumerate(missions):
        launch_date = mission.find('span', attrs={'class': 'launchdate'}).text.strip()
        mission_summary = mission.find('span', attrs={'class': 'mission'}).text.strip().split('•')
        mission_details = mission_data[index].contents

        payload.append({
            'launch_date': launch_date,
            'rocket': mission_summary[0],
            'mission': mission_summary[1],
            'launch_time': mission_details[1].strip(),
            'launch_site': mission_details[3].strip()
        })

    return payload


def scrape_space_flight_now():
    launch_page_request = requests.get(SPACE_FLIGHT_NOW_LAUNCH_SCHEDULE_URL)

    if (launch_page_request.status_code != 200):
        print('Error with status {status} encountered while retrieving latest launch data'.format(
            status=launch_page_request.status_code))
        return []

    launch_page = BeautifulSoup(launch_page_request.content, 'html.parser')
    launch_page_details_section = launch_page.find('div', attrs={'class': 'entry-content clearfix'})
    missions = launch_page_details_section.find_all('div', attrs={'class': 'datename'})
    mission_data = launch_page_details_section.find_all('div', attrs={'class': 'missiondata'})

    return missions_payload(missions, mission_data)