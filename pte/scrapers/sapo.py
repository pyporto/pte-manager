import datetime
from urllib.parse import urljoin
from requests_html import HTMLSession
from dateutil.parser import parse
from slugify import slugify

from pte.events import MiscEvent
from pte.scrapers import core

session = HTMLSession()


pt_en_months = {
    'fev': 'feb',
    'mai': 'may',
    'abr': 'apr',
    'ago': 'aug',
    'set': 'sep',
    'out': 'oct',
    'dez': 'dec',
}


class FootballSpider:

    start_page = None
    event_id_prefix = None
    event_name_prefix = None

    def __init__(self):
        self.pages = {self.start_page}
        self.seen_pages = set()
        self.seen_objects = set()

    def scrape(self):
        now = datetime.datetime.utcnow()
        while self.pages:
            page = self.pages.pop()
            if page in self.seen_pages:
                continue
            for el in self.scrape_page(page):
                if el.id not in self.seen_objects:
                    if el.end_date >= now:
                        yield el
                    self.seen_objects.add(el.id)
            self.seen_pages.add(page)

    def scrape_page(self, page):
        r = session.get(page)
        for li in r.html.find('ul.match-list > li'):
            pt_date = li.find('div.match-date')[0].text
            for k, v in pt_en_months.items():
                pt_date = pt_date.replace(k, v)
            event_start = parse(pt_date)
            event_end = event_start + datetime.timedelta(minutes=120)

            team_names_el = li.find('.team-name-short')
            if not team_names_el:
                team_names_el = li.find('.team-name')

            team1 = team_names_el[0].text
            team2 = team_names_el[1].text
            event_name = f'{self.event_name_prefix}. {team1} x {team2}'
            event_id = slugify(f'{self.event_id_prefix}-{event_start:%Y%m%d}-'
                               f'{team1}-{team2}')
            url = list(li.absolute_links)[0]
            yield MiscEvent(
                id=event_id,
                url=url,
                name=event_name,
                description=[],
                start_date=event_start,
                end_date=event_end,
            )
        options = r.html.find('select')[1].find('option')
        for opt in options:
            url = urljoin(page, opt.attrs['value'])
            if url.startswith(self.start_page):
                self.pages.add(url)


class PremierLeagueSpider(FootballSpider):
    start_page = 'https://desporto.sapo.pt/futebol/competicao/primeira-liga-2/calendario'
    event_name_prefix = 'Primeira Liga'
    event_id_prefix = 'primeira-liga'


class PortugalCupSpider(FootballSpider):
    start_page = 'https://desporto.sapo.pt/futebol/competicao/taca-de-portugal-10/calendario'
    event_name_prefix = 'Taça de Portugal'
    event_id_prefix = 'taca-de-portugal'


class UEFAChampionLeagueSpider(FootballSpider):
    start_page = 'https://desporto.sapo.pt/futebol/competicao/uefa-champions-league-6/calendario'
    event_id_prefix = 'uefa-champions-league'
    event_name_prefix = 'UEFA Champions League'


class UEFAEuroLeagueSpider(FootballSpider):
    start_page = 'https://desporto.sapo.pt/futebol/competicao/liga-europa-7/calendario'
    event_id_prefix = 'liga-europa'
    event_name_prefix = 'Liga Europa'


core.register(PremierLeagueSpider().scrape)
core.register(PortugalCupSpider().scrape)
core.register(UEFAChampionLeagueSpider().scrape)
core.register(UEFAChampionLeagueSpider().scrape)
