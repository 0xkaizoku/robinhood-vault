#!/usr/bin/env python3
"""Fingerprint GreenTown tech stack from public assets."""

import json
import re
import ssl
import urllib.request
from collections import defaultdict

ctx = ssl.create_default_context()
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
BASE = "https://greentown.social"


def fetch(url: str) -> tuple[str, dict]:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace"), dict(r.headers)


def main():
    html, headers = fetch(f"{BASE}/home")
    print("=== HEADERS (key) ===")
    for k in sorted(headers):
        kl = k.lower()
        if any(
            x in kl
            for x in (
                "server",
                "powered",
                "railway",
                "next",
                "cf-",
                "cache",
                "vary",
                "x-",
            )
        ):
            print(f"{k}: {headers[k]}")

    chunks = sorted(set(re.findall(r"/_next/static/[^\"']+", html)))
    print(f"\nCHUNK COUNT: {len(chunks)}")

    # App Router evidence
    app_routes = [c for c in chunks if "/app/" in c]
    print("APP ROUTES:")
    for c in app_routes:
        print(" ", c)

    # manifest + other static
    for path in ["/manifest.json", "/robots.txt", "/sitemap.xml", "/favicon.ico"]:
        try:
            body, h = fetch(BASE + path)
            print(f"\n=== {path} ===")
            print(body[:500] if path.endswith((".json", ".txt", ".xml")) else f"ok bytes via headers {h.get('Content-Type')}")
        except Exception as e:
            print(f"\n=== {path} FAIL: {e}")

    search_terms = [
        "wagmi",
        "viem",
        "ethers",
        "RainbowKit",
        "rainbowkit",
        "@rainbow-me",
        "privy",
        "@privy-io",
        "dynamic.xyz",
        "@dynamic-labs",
        "web3modal",
        "WalletConnect",
        "walletconnect",
        "@reown",
        "reown",
        "connectkit",
        "thirdweb",
        "alchemy",
        "infura",
        "createPublicClient",
        "createConfig",
        "useAccount",
        "useWriteContract",
        "@tanstack/react-query",
        "react-query",
        "TanStack",
        "zustand",
        "jotai",
        "redux",
        "framer-motion",
        "motion.",
        "@radix-ui",
        "radix-ui",
        "chakra",
        "@mui",
        "styled-components",
        "@emotion",
        "socket.io",
        "pusher",
        "supabase",
        "firebase",
        "prisma",
        "trpc",
        "graphql",
        "apollo",
        "posthog",
        "sentry",
        "mixpanel",
        "segment",
        "Robinhood",
        "4663",
        "chainId",
        "bondingCurve",
        "bonding",
        "siwe",
        "Sign-In with Ethereum",
        "NextAuth",
        "next-auth",
        "clerk",
        "auth0",
        "lucide-react",
        "heroicons",
        "phosphor",
        "recharts",
        "chart.js",
        "lightweight-charts",
        "sonner",
        "react-hot-toast",
        "toast",
        "ipfs",
        "pinata",
        "cloudinary",
        "openai",
        "cloudflare",
        "railway",
        "vercel",
        "zerion",
        "1inch",
        "uniswap",
        "permit2",
        "ERC20",
        "encodeFunctionData",
        "parseEther",
        "formatEther",
        "getContract",
        "readContract",
        "writeContract",
        "switchChain",
        "injected",
        "metaMask",
        "coinbaseWallet",
        "safe.global",
        "account-abstraction",
        "permissionless",
        "pimlico",
        "biconomy",
        "zerodev",
        "next/font",
        "geist",
        "Inter",
        "class-variance-authority",
        "clsx",
        "tailwind-merge",
        "cva(",
        "shadcn",
        "cmdk",
        "vaul",
        "embla",
        "swiper",
        "react-hook-form",
        "zod",
        "superjson",
        "nuqs",
        "next-themes",
        "date-fns",
        "dayjs",
        "lodash",
        "axios",
        "ky(",
        "ofetch",
        "swr",
        "react-query",
        "graphql-request",
        "urql",
        "ws://",
        "wss://",
        "rpc.mainnet",
        "robinhood",
        "blockscout",
        "greentown",
        "GreenSwap",
        "creator key",
        "keys",
        "referral",
        "Twitter",
        "x.com",
        "oauth",
        "siwe",
    ]

    # Fetch most relevant chunks
    priority = [c for c in chunks if any(x in c for x in ("home", "layout", "app/", "main-app", "webpack"))]
    other = [c for c in chunks if c not in priority]
    to_fetch = priority + other
    # limit size somewhat but try to cover a lot
    to_fetch = to_fetch[:40]

    hits = defaultdict(list)
    samples = {}
    all_text = []

    print(f"\nFetching {len(to_fetch)} chunks for fingerprints...")
    for path in to_fetch:
        url = BASE + path
        try:
            body, _ = fetch(url)
        except Exception as e:
            print("fail", path, e)
            continue
        all_text.append(body)
        lower = body.lower()
        for term in search_terms:
            if term.lower() in lower:
                hits[term].append(path.split("/")[-1][:50])
                if term not in samples:
                    idx = lower.find(term.lower())
                    samples[term] = body[max(0, idx - 50) : idx + 90].replace("\n", " ")[:160]

    print("\n=== LIBRARY / STRING HITS ===")
    for k, v in sorted(hits.items(), key=lambda x: (-len(x[1]), x[0].lower())):
        print(f"{k}: files={len(v)} sample={samples.get(k, '')!r}")

    # Combined blob searches for contract / chain / api patterns
    blob = "\n".join(all_text)
    print("\n=== API / RPC URL PATTERNS ===")
    for pat in [
        r"https?://[a-zA-Z0-9._/-]+\.(?:alchemy|infura|quicknode|drpc|publicnode)[a-zA-Z0-9._/-]*",
        r"https?://rpc[a-zA-Z0-9._/-]*",
        r"https?://[a-zA-Z0-9.-]*robinhood[a-zA-Z0-9._/-]*",
        r"https?://api\.[a-zA-Z0-9._/-]+",
        r"wss?://[a-zA-Z0-9._/-]+",
        r"0x[a-fA-F0-9]{40}",
        r"chainId[\"' ]*[:=][\"' ]*\d+",
        r"id:\s*4663",
        r"/api/[a-zA-Z0-9_/-]+",
    ]:
        found = sorted(set(re.findall(pat, blob)))[:30]
        if found:
            print(f"\nPattern {pat}:")
            for f in found:
                print(" ", f)

    # CSS analysis
    css_paths = [c for c in chunks if c.endswith(".css")]
    print("\n=== CSS ===")
    for path in css_paths:
        body, _ = fetch(BASE + path)
        print("file", path, "len", len(body))
        for term in [
            "--tw-",
            "tailwind",
            "@radix",
            "framer",
            "chakra",
            "mui",
            "backdrop-filter",
            "oklch",
            "var(--",
        ]:
            c = body.count(term)
            if c:
                print(f"  {term}: {c}")
        # sample class-like patterns
        tw_like = len(re.findall(r"\.[a-z][a-z0-9_-]*(?:\\:[a-z0-9_-]+)?\{", body))
        print("  rule-ish count", tw_like)

    # Try common API routes
    print("\n=== PROBE COMMON ENDPOINTS ===")
    probes = [
        "/api/health",
        "/api/creators",
        "/api/leaderboard",
        "/api/activity",
        "/api/keys",
        "/api/user",
        "/api/auth",
        "/api/auth/session",
        "/api/trpc",
        "/home",
        "/leaderboard",
        "/search",
        "/swap",
        "/launch",
        "/profile",
    ]
    for path in probes:
        try:
            req = urllib.request.Request(BASE + path, headers=UA)
            with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
                body = r.read(300).decode("utf-8", errors="replace")
                print(path, r.status, r.headers.get("Content-Type"), body[:120].replace("\n", " "))
        except Exception as e:
            err = str(e)
            code = re.search(r"Error (\d+)", err)
            print(path, "ERR", code.group(1) if code else err[:80])

    # Look for __NEXT_DATA__ style flight data in home for more routes
    print("\n=== RSC / INLINE SCRIPT CLUES ===")
    for m in re.finditer(r"self\.__next_f\.push\((\[.*?\])\)", html):
        s = m.group(1)
        if any(x in s for x in ("api", "chain", "wagmi", "privy", "viem", "4663")):
            print(s[:300])

    # Extract more from full html bottom
    scripts_inline = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
    print(f"inline scripts: {len(scripts_inline)}")
    for s in scripts_inline[:5]:
        if len(s) > 20:
            print(s[:400].replace("\n", " "))

    # Also fetch a few more pages for route map
    print("\n=== ROUTE MAP FROM HTML NAV (home) ===")
    hrefs = sorted(set(re.findall(r'href=\"(/[a-zA-Z0-9_/?=&-]*)\"', html)))
    for h in hrefs:
        print(" ", h)

    # try to get home page JS specifically and extract readable strings
    home_js = [c for c in chunks if "home/page" in c]
    if home_js:
        body, _ = fetch(BASE + home_js[0])
        strings = re.findall(r'["\']([A-Za-z0-9_ ./:@#-]{6,80})["\']', body)
        interesting = [
            s
            for s in strings
            if any(
                k in s.lower()
                for k in (
                    "api",
                    "key",
                    "swap",
                    "leader",
                    "wallet",
                    "chain",
                    "error",
                    "buy",
                    "sell",
                    "create",
                    "referral",
                    "point",
                    "house",
                    "nft",
                    "launch",
                )
            )
        ]
        print("\n=== HOME PAGE INTERESTING STRINGS ===")
        for s in sorted(set(interesting))[:80]:
            print(" ", s)

    # package-like paths in webpack
    print("\n=== WEBPACK MODULE PATH HINTS ===")
    for path in to_fetch:
        if "webpack" not in path and "main-app" not in path and len(path) > 0:
            continue
        try:
            body, _ = fetch(BASE + path)
        except Exception:
            continue
        mods = set(re.findall(r"(?:node_modules/|../)((?:@[^/]+/)?[a-zA-Z0-9_.-]+)", body))
        # also look for package names in sourceMappingURL or comments
        pkgs = set(re.findall(r"@?[a-zA-Z0-9-]+/[a-zA-Z0-9_.-]+", body))
        # filter noise
        interesting_pkgs = [
            p
            for p in sorted(pkgs)
            if any(
                k in p.lower()
                for k in (
                    "wagmi",
                    "viem",
                    "privy",
                    "rainbow",
                    "wallet",
                    "tanstack",
                    "radix",
                    "framer",
                    "reown",
                    "web3",
                    "eth",
                    "react",
                    "next",
                    "zod",
                    "hook",
                    "query",
                )
            )
        ][:50]
        if interesting_pkgs:
            print(path.split("/")[-1], interesting_pkgs[:40])


if __name__ == "__main__":
    main()
