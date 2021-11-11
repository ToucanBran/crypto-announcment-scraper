import time, requests, re
from services import CoinService
from services import get_logger

class BinanceScraper():

    def __init__(self, coin_service: CoinService):
        self.coin_service = coin_service
        self.logger = get_logger("scraper")

    def get_latest_coins(self, last_article_id: int) -> list[str]:
        self.logger.debug("Pulling announcement page")
        latest_announcement = requests.get("https://www.binance.com/bapi/composite/v1/public/cms/article/catalog/list/query?catalogId=48&pageNo=1&pageSize=15&rnd=" + str(time.time()))
        latest_announcement = latest_announcement.json()
        self.logger.debug("Finished pulling announcement page")
        # TODO only pull articles where id > last_article_id 
        latest_coins = self.parse_new_coins_from_announcements([article['title'] for article in latest_announcement['data']['articles'] if article['id'] > last_article_id])
        self.logger.info(f"Found {len(latest_coins)} new coins")
        return latest_coins
       
    def parse_new_coins_from_announcements(self, article_titles) -> list[str]:
        new_coin_announcements = list(filter(lambda article_title: 'will list' in article_title.lower(), article_titles))
        coins = (re.findall('\(([^)]+)', coin) for coin in new_coin_announcements)
        new_coins = [new_coin[0] for new_coin in coins if len(new_coin) > 0 and not self.coin_service.exists(new_coin[0])]
        return new_coins

            