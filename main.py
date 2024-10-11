import asyncio

from src.anime_torrent_dl import Anilist, DarkMahou, Downloader
from src.anime_torrent_dl.utils import similarity


async def main():
    s = await DarkMahou.search("jujutsu", 1)
    await Downloader.start_torrent(list(s.values())[0], ".")
    # print(similarity("kamuri", "muri"))
    # dl = Downloader()
    # await dl.search("My Hero")
    # d = await Anilist.search("my hero")
    # for x in d:
    #     print(x["title"]["userPreferred"])
    # popular = Anilist.get_most_popular(d)
    # print(popular)


if __name__ == "__main__":
    asyncio.run(main())
