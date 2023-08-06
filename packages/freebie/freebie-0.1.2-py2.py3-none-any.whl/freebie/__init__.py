from pathlib import Path
from freebie.util import read_csv

__PROJECT_PATH = Path(__file__).parents[0]
__WEB_SOURCE_PATH = __PROJECT_PATH / 'websources.csv'
__RSS_FEEDS_PATH = __PROJECT_PATH / 'rss_feeds.csv'
__TWITTER_HANDLES_PATH = __PROJECT_PATH / 'twitter_handles.csv'


twitter_handles = read_csv(__TWITTER_HANDLES_PATH)
websources = read_csv(__WEB_SOURCE_PATH)
rss_feeds = read_csv(__RSS_FEEDS_PATH)
