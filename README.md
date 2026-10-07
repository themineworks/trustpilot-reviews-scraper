# Trustpilot Reviews Scraper: Ratings, Replies, No Login

Scrape Trustpilot business reviews by company domain: reviewer name, star rating, review title, review text, date, business reply, plus the overall trust score and total review count. No login required. Pay per review returned.

**Run it on Apify:** [apify.com/themineworks/trustpilot-reviews](https://apify.com/themineworks/trustpilot-reviews)
**Docs, FAQ and pricing:** [themineworks.com/actors/trustpilot-reviews](https://themineworks.com/actors/trustpilot-reviews/)

**Price:** From $0.45 per 1,000 reviews on Apify's higher plans ($0.65 on the free plan), plus a $0.0025 start fee per run. Failed and empty results are never charged.

## What it returns

* Reviewer name, rating, title, and review text
* Business reply and review date
* Overall trust score and total review count
* Search by company domain or Trustpilot URL
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/trustpilot-reviews").call(run_input={
    "companyDomains": [
        "amazon.com",
        "booking.com"
    ],
    "companyDomain": "amazon.com",
    "maxResults": 25,
    "starsFilter": [
        "1",
        "2"
    ]
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/trustpilot-reviews').call({
    "companyDomains": [
        "amazon.com",
        "booking.com"
    ],
    "companyDomain": "amazon.com",
    "maxResults": 25,
    "starsFilter": [
        "1",
        "2"
    ]
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~trustpilot-reviews/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companyDomains": ["amazon.com", "booking.com"], "companyDomain": "amazon.com", "maxResults": 25, "starsFilter": ["1", "2"]}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 trustpilot_reviews_scraper.py --token YOUR_APIFY_TOKEN --company-domains "amazon.com,booking.com" --company-domain "amazon.com" --max-results "25" --stars-filter "1,2"
node trustpilot_reviews_scraper.mjs --token YOUR_APIFY_TOKEN --company-domains "amazon.com,booking.com" --company-domain "amazon.com" --max-results "25" --stars-filter "1,2"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `companyDomains` | array |  | Trustpilot company domains to scrape, for example ["amazon.com", "booking.com"] |
| `companyDomain` | string |  | Single company domain, for example "amazon.com" |
| `maxResults` | integer | `100` | Maximum reviews PER COMPANY (not per run), so 100 with three companies can return up to 300 |
| `starsFilter` | array |  | Only keep reviews with these star ratings (1-5) |
| `includeReviewInsights` | boolean | `false` | Adds one extra insights row PER COMPANY: a rating breakdown, the most common phrases in negative reviews, the… |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `business_domain` | string | Company domain scraped (for example amazon.com) |
| `reviewer_name` | string | Display name of the reviewer |
| `rating` | number | Star rating (1-5) |
| `title` | string | Review headline / title |
| `text` | string | Full review body text |
| `review_date` | string | ISO-8601 publish date of the review |
| `reply_text` | string | Business reply text (if present) |
| `review_url` | string | Direct URL to the review |
| `review_id` | string | Trustpilot review ID |
| `scraped_at` | string | ISO-8601 timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/trustpilot-reviews
```

## FAQ

### Does Trustpilot have an official API?

Trustpilot has a Business API but it is only available to businesses managing their own profiles. Public review data for any company is not available via an official API, making scraping the only option.

### What fields does each review include?

Reviewer name, star rating (1-5), review title, full review text, date posted, date of experience, business reply text (if any), and whether the review is verified.

### Can I scrape reviews for any company?

Yes. Pass the company domain (like amazon.com or shopify.com) or the full Trustpilot URL. The scraper retrieves all public reviews visible on that company's Trustpilot profile.

### What are the main use cases?

Competitor sentiment analysis, brand reputation monitoring, customer feedback aggregation for product teams, training data for review classifiers, and due diligence research before partnerships.

### How many reviews can I pull per company?

Trustpilot paginates reviews with 20 per page. The scraper handles pagination automatically and can retrieve all available reviews for a company up to the limit you set.

### How much does the Trustpilot Reviews Scraper cost?

From $0.45 per 1,000 reviews on Apify's higher plans ($0.65 on the free plan), plus a $0.0025 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [B2B Leads Finder](https://themineworks.com/actors/b2b-leads-finder/): Business emails and LinkedIn profiles for target companies
* [LinkedIn Company Scraper](https://themineworks.com/actors/linkedin-company-details/): Company size, industry, website, and followers without login
* [Zillow Rental Listings Scraper](https://themineworks.com/actors/zillow-rental-listings/): Scrape Zillow for-rent listings by city or zip. $1 per 1,000 results

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
