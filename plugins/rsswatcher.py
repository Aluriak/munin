# -*- coding: utf-8 -*-
#########################
#       RSSWATCHER      #
#########################


#########################
# IMPORTS               #
#########################
from munin.plugin import Plugin
import concurrent.futures
import feedparser
import threading
import pickle
import time
import re



#########################
# PRE-DECLARATIONS      #
#########################



#########################
# RSSWATCHER            #
#########################
class RssWatcher(Plugin):
    """
    Advanced Plugin application.
    RSS feed observer. Unprotected use of threads for watch given 
    feeds, and report news on the chan.
    Need to be rewrite for take care of data racing, especially about 
    self.news list.
    """
    REGEX     = re.compile(r"\s*rss\s+add\s+([^ ]*)\s*")
    SAVE_FILE_PREFIX  = 'data/'
    SAVE_FILE_SUFFIX  = '.pkl'
    SAVE_FILE_DEFAULT = 'rssfeeds'


# CONSTRUCTOR #################################################################
    def __init__(self, bot, urls=None, savefile=SAVE_FILE_DEFAULT, temporization=10):
        """Optionnaly wait for a list of rss feed url and a filename."""
        super().__init__(bot)
        self.news = []
        self.savefile = (RssWatcher.SAVE_FILE_PREFIX
                         + savefile
                         + RssWatcher.SAVE_FILE_SUFFIX
                        )
        self.temporization = temporization
        self.terminated = False
        self.urls = self.default_persistant_data()
        # start check RSS feeds
        def checker_daemon(rsswatcher_instance):
            """Check all RSS feed for news regularly"""
            t = 0
            while not rsswatcher_instance.terminated:
                t += 1
                if t >= rsswatcher_instance.temporization:
                    rsswatcher_instance.__check_rss_feeds()
                    t = 0
                else:
                    time.sleep(1)
        self.check_rss_thread = threading.Thread(target=checker_daemon, args=[self])
        self.check_rss_thread.start()

    def __del__(self):
        """Save rss_feed in self.savefile file"""
        self.terminated = True
        self.check_rss_thread.join()


    def do_command(self, bot, message, matched_groups, sudo=False):
        """Execute command for bot (unused), according 
        to regex matchs (used) and sudo mode (used)"""
        return self.__add_rss_feed(matched_groups[0]) if sudo else ''

    def say_something(self):
        """Say something. Called only if self.want_speak() returned True"""
        text = '\n'.join((
            '[NEWS] ' + item.title + ': ' + item.link
            for item in self.news
        ))
        self.news = []
        return text


    def __add_rss_feed(self, url):
        """Add given url in RSS feed internal list. No doublons possible."""
        last = last_news(url)
        if last is not None:
            self.urls[url] = last.date
            self.save_rss_feeds()
            return 'Last item is ' + last.link
        else:
            return 'No RSS feed found…'

    def __check_rss_feeds(self):
        """Check all rss feeds for find something new"""
        with concurrent.futures.ProcessPoolExecutor() as executor:
            urls = self.urls.keys()
            for url, last_item in zip(urls,
                                      executor.map(last_news,
                                                   urls)
                                     ):
                # if last knowed date is different from current one
                # add last item to news list
                if last_item.date != self.urls[url]:
                    self.urls[url] = last_item.date
                    self.news.append(last_item)

    def want_speak(self):
        """True iff at least one news to notice."""
        return len(self.news) > 0

    @property
    def help(self):
        return ("RSSWATCHER: notice when something is new on some RSS feed."
                "Sudoers can add new feed with 'rss add <url>'.")

    @property
    def debug_data(self):
        return self.urls

    @property
    def persistent_data(self):
        return self.urls

    @persistent_data.setter
    def persistent_data(self, values):
        self.urls = values

    def default_persistant_data(self):
        """Return the default persistent data"""
        return {}


def last_news(url):
    """Parse given url, and return last entry, 
    or None if unable to access to feed."""
    try:
        feed = feedparser.parse(url)
        ret = sorted(feed.entries, key=lambda e: e.date_parsed)[-1] 
    except:
        ret = None
    finally:
        return ret
