from __future__ import annotations

from enum import Enum


class CountMethod(str, Enum):
    exact = "exact"
    planned = "planned"
    estimated = "estimated"


class Filters(str, Enum):
    NOT = "not"
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IS = "is"
    LIKE = "like"
    ILIKE = "ilike"
    FTS = "fts"
    PLFTS = "plfts"
    PHFTS = "phfts"
    WFTS = "wfts"
    IN = "in"
    CS = "cs"
    CD = "cd"
    OV = "ov"
    SL = "sl"
    SR = "sr"
    NXL = "nxl"
    NXR = "nxr"
    ADJ = "adj"


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"


class ReturnMethod(str, Enum):
    minimal = "minimal"
    representation = "representation"
