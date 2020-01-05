from json import dumps
import os
from requests import get
import urllib.parse
import xmltodict
import yaml

with open(os.path.expanduser("~/.secrets/zillow.yml")) as f:
    cfg = yaml.safe_load(f)
    api_cfg = cfg["api"]

urls = {
    "search": "http://www.zillow.com/webservice/GetSearchResults.htm",
    "comps": "https://www.zillow.com/webservice/GetComps.htm",
}


def get_zpid(zws_id: int, address: str, citystatezip: str) -> str:
    resp = get(
        url=urls["search"],
        params={
            "zws-id": zws_id,
            "address": urllib.parse.quote(address),
            "citystatezip": urllib.parse.quote(citystatezip),
        },
    )
    return xmltodict.parse(resp.text, "utf8")


def get_comps(zws_id: int, zpid: int) -> dict:
    resp = get(url=urls["comps"], params={"zws-id": zws_id, "count": 1, "zpid": zpid})
    return xmltodict.parse(resp.text, "utf8")["Comps:comps"]["response"]["properties"][
        "comparables"
    ]


if __name__ == "__main__":
    zwsid = api_cfg["zwsid"]
    # print(dumps(get_comps(zwsid, 2082025403), indent=2))
    print(
        dumps(get_zpid(zwsid, "665 Ridgewood Rd APT 6", "Millburn, NJ 07041"), indent=2)
    )
