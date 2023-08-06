#!/usr/bin/env python3

from collections import namedtuple
import logging
import re
import time
import typing


import feedparser
import bs4
import packaging.version
import requests


RSSFeedItem = namedtuple("RSSFeedItem", ("version", "filename", "url", "time"))


class RSSFeed(object):
    BASE_URL = "https://sourceforge.net/projects/{project}/rss?path={url_path}"

    def __init__(self, project: str, url_path: typing.Union[str, None]=None):
        self._project = project
        self._url_path = url_path if url_path else "/"
        self._feedparser_res = None

    @property
    def url(self) -> str:
        return self.BASE_URL.format(project=self._project,
                                    url_path=self._url_path)

    @property
    def _feedparser(self) -> dict:
        if self._feedparser_res is None:
            url = self.url
            logging.debug("url is %s", url)
            feedparser_res = feedparser.parse(self.url)
            # FIXME: are assertion and exception ok here? Wrap them.
            if "bozo_exception" in feedparser_res:
                raise feedparser_res["bozo_exception"]
            assert "feed" in feedparser_res
            assert "entries" in feedparser_res
            self._feedparser_res = feedparser_res
        return self._feedparser_res

    def match_files(self, regex: typing.Union[typing.Pattern, str]) -> typing.List[RSSFeedItem]:
        if isinstance(regex, str):
            regex = re.compile(regex)
        matches = []
        for entry in self._feedparser["entries"]:
            _, filename = entry["title"].rsplit("/", 1)
            match = regex.match(filename)
            if match:
                if "version" in match.groupdict():
                    version = match.groupdict()["version"]
                elif len(match.groups()) >= 2:
                    version = match.group(2)
                elif len(match.groups()) >= 1:
                    version = match.group(1)
                else:
                    # FIXME: use wrapped errors
                    raise ValueError("Cannot determine version from match")

                time = entry["published_parsed"]
                url = entry["link"]
                match = RSSFeedItem(version=version, filename=filename, url=url, time=time)
                matches.append(match)
        return matches


class HtmlDirItem(namedtuple("HtmlDirItemParent", ("title", "path", "time"))):
    def is_directory(self) -> bool:
        if self.path:
            return self.path[-1] == "/"
        else:
            return False


class HtmlDirListing(object):
    BASE_URL = "https://sourceforge.net"
    FILES_PATH = "/projects/{project}/files/"

    def __init__(self, project: str, path: typing.Union[str, None]=None, absolutePath: bool=False):
        self._project = project
        self._html_text_res = None
        self._base_url = self.BASE_URL
        self._path = None
        self._path = self.FILES_PATH.format(project=project)
        if absolutePath:
            if isinstance(path, str):
                self._path = path
        else:
            if isinstance(path, str):
                self._path += path

    @property
    def _url(self) -> str:
        return self._base_url + self._path

    @property
    def _html_text(self) -> str:
        if self._html_text_res is None:
            url = self._url
            logging.debug("fetching %s", url)
            r = requests.get(url)  # FIXME: can raise
            assert(r.status_code == 200)  # FIXME: can raise
            self._html_text_res = r.text
        return self._html_text_res

    def __htmlrow2download(self, row: bs4.element.Tag) -> HtmlDirItem:
        title = row["title"]
        path = row.select("th > a")[0]["href"]  # FIXME: soup can fail
        try:
            rtime = time.strptime(row.select("[headers=files_date_h] > abbr")[0]["title"], "%Y-%m-%d %H:%M:%S %Z")  # FIXME: soup can fail
        except ValueError:
            raise ValueError("Cannot parse time")  # FIXME: wrap
        return HtmlDirItem(title=title, path=path, time=rtime)

    def list(self) -> typing.List[HtmlDirItem]:
        soup = bs4.BeautifulSoup(self._html_text, "lxml")  # FIXME: wrap
        htmlrows = soup.select('#files_list > tbody > tr')
        return list(map(self.__htmlrow2download, htmlrows))


def walkHtml(topHtmlDir: HtmlDirListing, sortKey: typing.Callable[[typing.Any], typing.Any]=None, sortReverse: bool=False, topDown: bool=True, maxDepth: int=None) -> typing.Tuple[HtmlDirListing, typing.List[HtmlDirItem], typing.List[HtmlDirItem]]:
    if maxDepth is not None:
        if maxDepth <= 0:
            return

    htmlDirList = sorted(topHtmlDir.list(), key=sortKey, reverse=sortReverse)
    htmlDirs = []
    htmlFiles = []
    for htmlDirItem in htmlDirList:
        if htmlDirItem.is_directory():
            htmlDirs.append(htmlDirItem)
        else:
            htmlFiles.append(htmlDirItem)
    if topDown:
        yield topHtmlDir, htmlDirs, htmlFiles
    for htmlDirItem in htmlDirs:
        htmlSubDir = HtmlDirListing(project=topHtmlDir._project, path=htmlDirItem.path, absolutePath=True)
        yield from walkHtml(htmlSubDir, sortKey=sortKey, sortReverse=sortReverse, topDown=topDown, maxDepth=maxDepth-1 if maxDepth is not None else None)
    if not topDown:
        yield htmlDirs, htmlFiles


def walkHtmlFilter(topHtmlDir: HtmlDirListing, filterFunc: typing.Callable[[HtmlDirItem], bool], sortKey: typing.Callable[[typing.Any], typing.Any]=None, sortReverse: bool=False, maxNbQueries: int=None, maxDepth: int=None):
    queryI = 0
    if maxNbQueries is not None:
        if queryI >= maxNbQueries:
            return
    for _, _, htmlFiles in walkHtml(topHtmlDir, sortKey=sortKey, sortReverse=sortReverse):
        for htmlFile in filter(filterFunc, htmlFiles):
            yield htmlFile
        if maxNbQueries is not None:
            if queryI >= maxNbQueries:
                return


def main() -> None:
    logging.getLogger().setLevel(0)

    if True:
        import pprint
        project_name = "tcl"
        feed = RSSFeed(project=project_name, url_path="/tcl")
        matches = feed.match_files(r"tcl(?P<version>[0-9\.a-zA-Z]+)-src.tar.gz")
        pprint.pprint(matches)
        matches = feed.match_files(r"tk(?P<version>[0-9\.a-zA-Z]+)-src.tar.gz")
        pprint.pprint(matches)

    tcl_dir = HtmlDirListing(project="tcl", path="Tcl")

    def sortKey(htmlDirItem: HtmlDirItem) -> typing.Any:
        return packaging.version.parse(htmlDirItem.title)

    def filterFunc(htmlDirItem: HtmlDirItem) -> bool:
        if htmlDirItem.is_directory():
            return True
        else:
            return re.match("tcl([A-Za-z0-9.]+)-src.tar.gz", htmlDirItem.title) is not None

    for htmldiritem in walkHtmlFilter(tcl_dir, filterFunc=filterFunc, sortKey=sortKey, sortReverse=True, maxNbQueries=10):
        print(htmldiritem)


if __name__ == "__main__":
    main()
