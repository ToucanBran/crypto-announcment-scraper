import sys
from logger import logger
from services import BinanceScraper, CoinService, queue
from load_config import *
from services.rabbitmq_wrapper import RabbitMqWrapper

def main(configs):
    scraper = BinanceScraper(CoinService())
    last_article_id = 0
    new_coins = scraper.get_latest_coins(last_article_id)
    logger.debug(f"New coins: {', '.join(new_coins)}")
    
    with queue(configs["queue"]) as q:
        for coin in new_coins:
            logger.info(f"Pushing {coin} to queue")
            q.push(coin)


if __name__ == '__main__':
    configs = load_config("config.yml")
    rmq = RabbitMqWrapper(configs["queue"])
    channel = None
    try_count = 0
    while try_count < 3 and channel is None:
        try:
            channel = rmq.open_channel()
        except Exception as e:
            logger.debug(e)
            logger.info(f"Try {try_count + 1}: Unable to connect to the new coin queue")
            try_count = try_count + 1

    if not rmq.channel_connected():
        logger.info("Unable to connect to connect to the queue")
        sys.exit(1)

    rmq.close_connection()

    logger.info("Scanning announcements...")
    main(configs)