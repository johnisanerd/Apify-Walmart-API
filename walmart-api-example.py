"""
Walmart API: A Quick Start Example
See more at: https://apify.com/johnvc/walmart-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/walmart-api/input-schema?fpr=9n7kx3

This script shows how to call the Walmart API on Apify from Python and
read its structured JSON output. The default run stays deliberately small so
your first call is inexpensive; the --example recipes mirror the API's main
use cases (see the README Recipes section).

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python walmart-api-example.py
  uv run python walmart-api-example.py --example seller_lookup
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/walmart-api"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short summary of dataset items."""
    print(f"Returned {len(items)} item(s).\n")
    for item in items:
        print(item.get('title'), item.get('price'), item.get('sellerName'))


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start. Inputs stay small on purpose."""
    run_input: dict[str, Any] = {
        "search_mode": "search",
        "query": "laptop",
        "max_results": 3,  # small on purpose to keep the first run inexpensive
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_seller_lookup(client: ApifyClient) -> None:
    """Every seller on one listing (mirrors the walmart-seller-lookup use case).

    The productId and store_id both come from any search-mode row.
    """
    run_input: dict[str, Any] = {
        "search_mode": "sellers",
        "item_id": "34X621REEQZQ",
        "store_id": "1932",
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_price_check(client: ApifyClient) -> None:
    """Price snapshot for a keyword; schedule it to build price history."""
    run_input: dict[str, Any] = {
        "search_mode": "search",
        "query": "coffee maker",
        "max_results": 3,  # small on purpose; raise once you know your budget
    }
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    for item in client.dataset(run.default_dataset_id).iterate_items():
        print(f"{item.get('title', '')[:60]:60} price={item.get('price')} was={item.get('wasPrice')}")


def main() -> None:
    """Dispatch a quick-start or use-case recipe."""
    parser = argparse.ArgumentParser(description="Walmart API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=['default', 'seller_lookup', 'price_check'],
        help="Which recipe to run (see README Recipes).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_API_TOKEN in .env or the environment.")

    client = ApifyClient(token)
    dispatch = {
        "default": run_default,
        "seller_lookup": run_seller_lookup,
        "price_check": run_price_check,
    }
    dispatch[args.example](client)


if __name__ == "__main__":
    main()
