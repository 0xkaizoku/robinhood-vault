#!/usr/bin/env python3
"""Extract GreenTown app API paths and backend fingerprints from page chunks."""

import re
import ssl
import urllib.request

ctx = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0"}
BASE = "https://greentown.social"
API = "https://api.greentown.social"


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read().decode("utf-8", errors="replace")


def main():
    pages = [
        "/home",
        "/launch",
        "/greenswap",
        "/houses",
        "/wallet",
        "/leaderboard",
        "/search",
        "/settings",
    ]
    all_chunks = set()
    for p in pages:
        st, _, html = fetch(BASE + p)
        print(p, st)
        for c in re.findall(r"/_next/static/[^\"']+\.js", html):
            all_chunks.add(c)

    blob_parts = []
    for c in sorted(all_chunks):
        st, _, body = fetch(BASE + c)
        if st == 200:
            blob_parts.append(body)
    blob = "\n".join(blob_parts)
    print("total blob", len(blob))

    # Find api.greentown usages and nearby path strings
    print("\n=== api.greentown.social CONTEXT ===")
    for m in re.finditer(r"api\.greentown\.social", blob):
        print(blob[max(0, m.start() - 80) : m.end() + 120].replace("\n", " "))
        print("---")

    # SWR keys and fetchers
    print("\n=== SWR / FETCH KEYS ===")
    for pat in [
        r'["\']global-activity["\']',
        r'["\']leaderboard["\']',
        r'["\']trending[^"\']*["\']',
        r'["\']hive[^"\']*["\']',
        r'["\']keys[^"\']*["\']',
        r'["\']/v1/[^"\']+["\']',
        r'["\']v1/[^"\']+["\']',
        r'fetch\(["\'][^"\']+["\']',
        r'ofetch\(["\'][^"\']+["\']',
        r'baseURL[:"\'=\s]+[^,}\s]+',
        r'BASE_URL[:"\'=\s]+[^,}\s]+',
        r'NEXT_PUBLIC_[A-Z0-9_]+',
        r'process\.env\.[A-Z0-9_]+',
    ]:
        found = sorted(set(re.findall(pat, blob)))[:40]
        if found:
            print(pat)
            for f in found:
                print(" ", f)

    # Look for express/helmet/cors style is backend; check OPTIONS
    print("\n=== API OPTIONS / METHODS ===")
    for path in ["/", "/health", "/activity", "/leaderboard", "/v1/activity", "/v1/leaderboard"]:
        st, h, body = fetch(API + path)
        print(path, st, body[:100])

    # Try common REST shapes
    print("\n=== REST PROBES ===")
    candidates = []
    # extract quoted path-like strings that look like backend routes
    for s in set(re.findall(r'["\'](/[a-z][a-z0-9_/-]{2,60})["\']', blob)):
        if any(
            k in s
            for k in (
                "activity",
                "leader",
                "user",
                "key",
                "trade",
                "house",
                "swap",
                "launch",
                "referral",
                "notif",
                "feed",
                "hive",
                "point",
                "creator",
                "profile",
                "search",
                "price",
                "token",
                "market",
                "chart",
            )
        ):
            candidates.append(s)
    for s in sorted(candidates):
        print(" candidate route string:", s)

    # Probe some of these on api host
    print("\n=== PROBE CANDIDATES ON API HOST ===")
    for s in sorted(candidates)[:50]:
        st, h, body = fetch(API + s)
        if st != 404:
            print(s, st, body[:150].replace("\n", " "))

    # Also try without leading assumptions
    for s in [
        "/activity",
        "/global-activity",
        "/leaderboard",
        "/users",
        "/creators",
        "/keys",
        "/trades",
        "/houses",
        "/feed",
        "/hive",
        "/search",
        "/v1/activity",
        "/v1/leaderboard",
        "/v1/users",
        "/v1/keys",
        "/v1/trades",
        "/v1/houses",
        "/v1/feed",
        "/v1/hive",
        "/v1/search",
        "/v1/trending",
        "/v1/notifications",
        "/v1/referrals",
        "/v1/tokens",
        "/v1/launch",
        "/v1/swap",
        "/v1/stats",
        "/v1/markets",
        "/v1/prices",
        "/v1/me",
        "/me",
        "/stats",
    ]:
        st, h, body = fetch(API + s)
        if st != 404:
            print("hit", s, st, body[:180].replace("\n", " "))

    # Privy app id confirmation context
    print("\n=== PRIVY APP ID CONTEXT ===")
    idx = blob.find("cmrg3tc55005q0cl78wtlpxl7")
    if idx >= 0:
        print(blob[idx - 100 : idx + 150].replace("\n", " "))

    # Twitter linking
    print("\n=== TWITTER / SOCIAL LINK ===")
    for term in ["twitter.com", "api.twitter", "x.com/i/oauth", "oauth/twitter", "linkTwitter"]:
        if term in blob:
            i = blob.find(term)
            print(term, blob[i - 60 : i + 80].replace("\n", " ")[:160])

    # ofetch / SWR imports evidence
    print("\n=== DATA CLIENT ===")
    for term in ["ofetch", "ky(", "$fetch", "axios", "useSWR", "mutate(", "refreshInterval", "dedupingInterval"]:
        print(term, blob.count(term))
        if term in blob:
            i = blob.find(term)
            print(" ", blob[i - 40 : i + 80].replace("\n", " ")[:140])


if __name__ == "__main__":
    main()
