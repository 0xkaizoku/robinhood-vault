#!/usr/bin/env python3
"""Deeper GreenTown stack: API, contracts, nav routes, privy/wagmi."""

import re
import ssl
import urllib.request
from collections import Counter

ctx = ssl.create_default_context()
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
BASE = "https://greentown.social"
API = "https://api.greentown.social"


def fetch(url: str, method="GET", data=None, headers=None) -> tuple[int, dict, str]:
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, dict(e.headers or {}), body


def main():
    # All app routes from home + a few known pages JS
    status, headers, html = fetch(f"{BASE}/home")
    chunks = sorted(set(re.findall(r"/_next/static/[^\"']+\.js", html)))

    # Collect all JS content for greentown-specific paths
    print("Downloading all JS chunks...")
    bodies = []
    for path in chunks:
        st, _, body = fetch(BASE + path)
        if st == 200:
            bodies.append((path, body))
            print(f"  {st} {path} {len(body)}")

    blob = "\n".join(b for _, b in bodies)

    # App nav routes
    print("\n=== NAV / ROUTES ===")
    routes = sorted(set(re.findall(r'["\'](/(?:home|leaderboard|search|launch|greenswap|houses|wallet|profile|u|settings|points|feed|hive|swap|create|key)[a-zA-Z0-9_/?=&-]*)["\']', blob)))
    for r in routes:
        print(" ", r)

    # greentown API paths
    print("\n=== GREENTown API PATHS IN BUNDLE ===")
    api_paths = sorted(set(re.findall(r'["\'](/api/v1/[a-zA-Z0-9_/-]+)["\']', blob)))
    for p in api_paths:
        print(" ", p)
    api_full = sorted(set(re.findall(r'https://api\.greentown\.social[a-zA-Z0-9_/?=&%-]*', blob)))
    print("full urls:", api_full[:40])

    # more endpoint-like strings
    print("\n=== /api/v1 STRINGS (broader) ===")
    for m in sorted(set(re.findall(r"/api/v1/[a-zA-Z0-9_/-]+", blob))):
        print(" ", m)

    # Privy app id
    print("\n=== PRIVY / AUTH CLUES ===")
    for pat in [
        r"cl[a-z0-9]{20,}",  # sometimes privy
        r"privy\.io[^\s\"']*",
        r"appId[\"']?\s*[:=]\s*[\"']([^\"']+)[\"']",
        r"PRIVY[A-Z0-9_]*",
        r"clientId[\"']?\s*[:=]\s*[\"']([^\"']+)[\"']",
    ]:
        found = set(re.findall(pat, blob))
        if found:
            print(pat, list(found)[:15])

    # Contract addresses that appear near greentown-ish context
    print("\n=== CONTRACT-LIKE NEAR KEYWORDS ===")
    for kw in ["keys", "Key", "factory", "swap", "router", "marketplace", "referral", "Hive", "House"]:
        for m in re.finditer(re.escape(kw), blob):
            window = blob[max(0, m.start() - 120) : m.end() + 120]
            addrs = re.findall(r"0x[a-fA-F0-9]{40}", window)
            if addrs:
                print(kw, addrs, window.replace("\n", " ")[:180])
                break

    # All unique 0x addresses that aren't zeros / known system
    addrs = Counter(re.findall(r"0x[a-fA-F0-9]{40}", blob))
    print("\n=== TOP NON-TRIVIAL ADDRESSES ===")
    skip_pref = ("0x000000", "0x420000", "0x01fff", "0x1fff")
    for a, c in addrs.most_common(80):
        if a.lower().startswith(skip_pref) or a == "0x0000000000000000000000000000000000000000":
            continue
        # filter common tokens
        print(f"  {a} x{c}")

    # wagmi vs viem usage
    print("\n=== WEB3 LIB COUNTS ===")
    for term in [
        "wagmi",
        "@wagmi",
        "createConfig",
        "useAccount",
        "useConnect",
        "viem@",
        "from \"viem",
        "ethers",
        "@privy-io/react-auth",
        "PrivyProvider",
        "usePrivy",
        "useWallets",
        "useSendTransaction",
        "SWRConfig",
        "useSWR",
        "socket.io-client",
        "io(",
        "framer-motion",
        "motion.create",
        "zustand",
        "createContext",
        "react-hot-toast",
        "sonner",
        "Toaster",
        "lucide",
        "clsx",
        "twMerge",
        "cva(",
        "class-variance-authority",
    ]:
        print(f"  {term}: {blob.count(term)}")

    # Probe api.greentown.social
    print("\n=== API.GREENTown.SOCIAL PROBES ===")
    for path in [
        "/",
        "/health",
        "/api/health",
        "/api/v1/health",
        "/api/v1/sessions",
        "/api/v1/siwe/init",
        "/api/v1/leaderboard",
        "/api/v1/activity",
        "/api/v1/creators",
        "/api/v1/users",
        "/api/v1/keys",
        "/api/v1/trades",
        "/api/v1/houses",
        "/docs",
        "/openapi.json",
        "/swagger",
        "/redoc",
    ]:
        st, h, body = fetch(API + path)
        ct = h.get("Content-Type", h.get("content-type", ""))
        powered = h.get("X-Powered-By") or h.get("x-powered-by") or h.get("Server") or h.get("server")
        print(f"{path}: {st} ct={ct[:40]} server={powered} body={body[:120].replace(chr(10),' ')}")

    # headers on API root
    st, h, body = fetch(API + "/")
    print("\n=== API ROOT HEADERS ===")
    for k, v in sorted(h.items()):
        print(f"  {k}: {v}")

    # Check more pages for additional chunks
    print("\n=== EXTRA PAGES ===")
    for path in ["/launch", "/greenswap", "/houses", "/wallet", "/leaderboard", "/search"]:
        st, _, page = fetch(BASE + path)
        print(path, st, "len", len(page))
        # extract any new chunk names
        more = set(re.findall(r"/_next/static/chunks/app/[^\"']+", page))
        for m in sorted(more):
            print("  chunk", m)

    # state store clues from sample earlier
    print("\n=== STATE KEYWORDS ===")
    for term in [
        "updateHiveFeed",
        "keysHeld",
        "referralEarnings",
        "trendingUsers",
        "global-activity",
        "dateHiveFeed",
        "Hive",
        "houses",
        "GreenSwap",
        "points",
        "bonding",
        "subject",
        "buyKey",
        "sellKey",
        "getBuyPrice",
        "getSellPrice",
    ]:
        if term in blob:
            idx = blob.find(term)
            print(term, "->", blob[max(0, idx - 60) : idx + 100].replace("\n", " ")[:180])


if __name__ == "__main__":
    main()
