import aiohttp
from bs4 import BeautifulSoup

from torrentp import TorrentDownloader
from anime_torrent_dl.utils import FIREFOX_HEADERS, similarity
from src.anime_torrent_dl.custom_types import *


class Anilist:
    endpoint = "https://graphql.anilist.co"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "schema": "default",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "DNT": "1",
        "TE": "trailers",
    }

    @staticmethod
    def build_query(variables: AnilistQueryVariables):
        return {
            "query": """query ($search: String, $isAdult: Boolean) {
                anime: Page(perPage: 10) {
                  pageInfo {
                    total
                  }
                  results: media(type: ANIME, isAdult: $isAdult, search: $search) {
                    id
                    title {
                      userPreferred
                    }
                    coverImage {
                      medium
                    }
                    type
                    format
                    bannerImage
                    isLicensed
                    popularity
                    startDate {
                      year
                    }
                  }
                }
              }""",
            "variables": variables,
        }

    @classmethod
    async def search(cls, term: str, is_adult: bool = False) -> list[AnilistResult]:
        async with aiohttp.ClientSession(headers=cls.headers) as s:
            async with s.post(
                cls.endpoint,
                json=cls.build_query({"search": term, "isAdult": is_adult}),
            ) as r:
                r.raise_for_status()
                return (await r.json()).get("data", {}).get("anime", {}).get("results")

    @staticmethod
    def get_most_popular(anilist_result: list[AnilistResult]):
        most_popular = anilist_result[0]
        for anime in anilist_result:
            if anime["popularity"] > most_popular["popularity"]:
                most_popular = anime
        return most_popular


class DarkMahou:
    baseurl = "https://darkmahou.org/"

    @staticmethod
    def parse_search_page(page_content: str) -> list[DarkMahouResult]:
        animes = []
        soup = BeautifulSoup(page_content, "html.parser")
        listupd = soup.find("div", {"class": "listupd"}).find_all("a", {"class": "tip"})  # type: ignore
        for item in listupd:
            if item.get("href") is None:
                continue
            animes.append({"title": item["title"], "url": item["href"]})
        return animes

    @staticmethod
    def get_most_similar(animes: list[DarkMahouResult], anilist_result: AnilistResult):
        most_similar = animes[0]
        most_similar_perf = 0
        for anime in animes:
            sim = similarity(anime["title"], anilist_result["title"]["userPreferred"])
            if sim > most_similar_perf:
                most_similar = anime
        return most_similar

    @staticmethod
    def parse_anime_page(page_content: str):
        soup = BeautifulSoup(page_content, "html.parser")
        anime_episodes = soup.find_all("div", {"class": "soraddl dlone"})
        episodes = []
        for episode in anime_episodes:
            url_data = {}
            urls = episode.find_all("a")
            for url in urls:
                if "magnet:" not in url["href"]: continue
                url_data[url.get_text()] = url["href"]
            episodes.append(url_data)
        return episodes

    @classmethod
    async def get_anime_url(cls, anime: DarkMahouResult, episode: int) -> dict[str, str]:
        async with aiohttp.ClientSession(headers=FIREFOX_HEADERS) as s:
            async with s.get(anime["url"]) as r:
                r.raise_for_status()
                page_content = cls.parse_anime_page(await r.text())
                return page_content[
                    (
                        (episode - 1)
                        if (episode - 1) > 0 and (episode - 1) < len(page_content)
                        else 0
                    )
                ]

    @classmethod
    async def search_anime(cls, title: str):
        async with aiohttp.ClientSession(headers=FIREFOX_HEADERS) as s:
            async with s.get(f"{cls.baseurl}?s={title}") as r:
                r.raise_for_status()
                return cls.parse_search_page(await r.text())

    @classmethod
    async def search(cls, title: str, episode: int, season: int = 0):
        anilist_anime = Anilist.get_most_popular(await Anilist.search(title))
        animes = await cls.search_anime(title)
        anime = cls.get_most_similar(animes, anilist_anime)
        return await cls.get_anime_url(anime, episode)


class Downloader:
    def __init__(self): ...

    @classmethod
    async def start_torrent(cls, torrent_url: str, target_folder: str):
        torrent_file = TorrentDownloader(torrent_url, target_folder)
        print(torrent_file._torrent_info)
        await torrent_file.start_download()
        
