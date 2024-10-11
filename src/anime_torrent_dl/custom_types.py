from typing import TypedDict

AnilistQueryVariables = TypedDict(
    "AnilistQueryVariables", {"search": str, "isAdult": bool}
)

AnilistResultUserPreferred = TypedDict(
    "AnilistResultUserPreferred",
    {
        "userPreferred": str,
    },
)

AnilistResultCoverImage = TypedDict(
    "AnilistResultCoverImage",
    {
        "medium": str,
    },
)

AnilistResultStartDate = TypedDict(
    "AnilistResultStartDate",
    {
        "year": int,
    },
)

AnilistResult = TypedDict(
    "AnilistResult",
    {
        "id": int,
        "title": AnilistResultUserPreferred,
        "coverImage": AnilistResultCoverImage,
        "type": str,
        "format": str,
        "bannerImage": str,
        "isLicensed": bool,
        "popularity": float,
        "startDate": AnilistResultStartDate,
    },
)

DarkMahouResult = TypedDict(
    "DarkMahouResult",
    {
        "title": str,
        "url": str,
    },
)
