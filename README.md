# Monero Merchant Index

An open dataset of businesses and services that accept Monero (XMR), published by
[XMRList](https://xmrlist.com) and updated every day by a GitHub Action.

Each listing has been reviewed by hand. The dataset records its category, KYC policy, Tor (.onion) address,
how long it has been operating, uptime, and an A–F grade computed with a
[published method](https://xmrlist.com/methodology). Daily summary snapshots make it possible to follow how the
Monero merchant economy changes over time.

- **Coverage:** about 1,800 listings in 20 categories and 100+ countries
- **Updated:** daily (snapshots start on 2026-11-04)
- **Formats:** CSV and JSON, no login or API key
- **Licence:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please credit "XMRList Monero Merchant Index" and link to https://xmrlist.com/stats

## Files

| File | Contents |
| --- | --- |
| `data/listings.csv` | One row per listing (fields below) |
| `data/listings.json` | The same listings as JSON, with export time and source |
| `data/stats.json` | Latest summary: totals, grades, KYC mix, Tor share, payment processors, categories, countries |
| `data/categories.csv` | Per category: listings, % no KYC, % with onion, % XMR confirmed, grade A or B |
| `data/countries.csv` | Listings per country (ISO 3166-1 alpha-2) |
| `data/history.csv` | One row per day: listings, verified, XMR confirmed, no KYC, onion, % online |
| `data/snapshots/YYYY-MM-DD.json` | Frozen copy of `stats.json` for each day |

## Listing fields

| Field | Description |
| --- | --- |
| `name`, `slug` | Listing name and identifier |
| `url` | Listing page on XMRList |
| `website`, `onion` | Official website and Tor address (empty if none) |
| `category`, `subcategory` | Directory category slugs |
| `status` | `verified` (reviewed, and the business links back to its listing), `admitted` (reviewed and listed), `questionable` (open reports or warning signs) |
| `grade` | A–F score from the [methodology](https://xmrlist.com/methodology) |
| `accepts_xmr` | `True` = Monero acceptance confirmed, `False` = reported as no longer accepting, empty = not yet confirmed |
| `xmr_discount` | Discount for paying in XMR, if published |
| `kyc` | `None` (no ID check required, or no KYC policy published), `Optional / sometimes`, `Required` |
| `operating_since` | Year the service started, if known |
| `country` | ISO 3166-1 alpha-2 country, if known |
| `last_checked` | Date the listing was last reviewed |
| `uptime_30d` | % of automatic checks in the last 30 days where the site responded |
| `rating`, `reviews` | Average user rating (1–5) and review count on XMRList |

## Sources and method

Listings come from submissions by businesses, community reports and XMRList's own research, and every one is checked
by hand before it is published. Websites and onion addresses are probed automatically for uptime. The scoring rules are
documented at https://xmrlist.com/methodology. The same data is available live from the free API at
https://xmrlist.com/api.

## Updating

`scripts/update.py` (Python standard library only) downloads the latest export from xmrlist.com and rewrites `data/`.
`.github/workflows/update.yml` runs it every day and commits any changes, so the git history is a full record of every
change.

## Citation

> XMRList (2026). Monero Merchant Index [Data set]. https://github.com/benwalton34533-cpu/monero-merchant-index. CC BY 4.0.
