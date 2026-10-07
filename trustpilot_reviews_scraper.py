#!/usr/bin/env python3
"""Business reviews, star ratings, and trust scores. Python, Node.js and cURL clients for the Trustpilot Reviews Scraper on Apify, pay per result.

Command-line client for the themineworks/trustpilot-reviews actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/trustpilot-reviews/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/trustpilot-reviews"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--company-domains", help="Comma-separated. Trustpilot company domains to scrape, for example ['amazon.com', 'booking.com']")
    ap.add_argument("--company-domain", help="Single company domain, for example 'amazon.com'")
    ap.add_argument("--max-results", type=int, help="Maximum reviews PER COMPANY (not per run), so 100 with three companies can return up to…")
    ap.add_argument("--stars-filter", help="Comma-separated. Only keep reviews with these star ratings (1-5)")
    ap.add_argument("--include-review-insights", action=argparse.BooleanOptionalAction, help="Adds one extra insights row PER COMPANY: a rating breakdown, the most common phrases in…")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.company_domains: run_input["companyDomains"] = [s.strip() for s in a.company_domains.split(",") if s.strip()]
    if a.company_domain is not None: run_input["companyDomain"] = a.company_domain
    if a.max_results is not None: run_input["maxResults"] = a.max_results
    if a.stars_filter: run_input["starsFilter"] = [s.strip() for s in a.stars_filter.split(",") if s.strip()]
    if a.include_review_insights is not None: run_input["includeReviewInsights"] = a.include_review_insights

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
