# 🛒 Walmart API: products, prices, reviews and sellers as JSON

Actor: [johnvc/walmart-api](https://apify.com/johnvc/walmart-api?fpr=9n7kx3) · [Input schema](https://apify.com/johnvc/walmart-api/input-schema?fpr=9n7kx3)

This repo shows two ways to use the [Walmart API](https://apify.com/johnvc/walmart-api?fpr=9n7kx3) on Apify: a Python quick start and MCP installs for five AI clients. Search products by keyword, look up full detail with UPC and variants, export customer reviews, and list every marketplace seller offering an item. If you were planning to scrape Walmart prices yourself, this returns the same rows without the blocking fight.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

The walmart api has four modes behind one search_mode input. Search returns products with price, wasPrice, rating, reviewCount, sellerName, a sponsored flag and both product ids. Sellers is the differentiator: every company offering an item with its own price, availabilityStatus, deliveryDate and returnPolicy, including the registered legal name behind the storefront. Reviews takes the numeric usItemId (search hands it to you) and detail adds upc, manufacturerNumber and variantCount. The seller_lookup recipe in this repo runs the whole chain, and the price fields make scheduled Walmart price history tracking a two-line loop.

## Quick Start

You need Python 3.11+ and a free Apify API key: sign up at [apify.com](https://apify.com?fpr=9n7kx3), then copy your token from Console Settings.

```bash
git clone https://github.com/johnisanerd/Apify-Walmart-API.git
cd Apify-Walmart-API
uv sync
cp .env.example .env   # then paste your APIFY_API_TOKEN
uv run python walmart-api-example.py
```

Run a specific recipe:

```bash
uv run python walmart-api-example.py --example seller_lookup
```

## Why use this API

- Four modes in one API: search, product detail, reviews, sellers
- Every seller on a listing with individual price, stock, delivery and return policy
- Registered legal seller names, which is what identifies a reseller
- price and wasPrice per store for price history tracking
- Both product ids on every search row, so the chain to any mode is self contained

## Recipes

The example script ships ready-made recipes that mirror this API's main use cases:

- **Every seller on a listing** (`--example seller_lookup`): Lists all sellers of one product with price, stock and delivery per offer.
- **Walmart price tracking** (`--example price_check`): Searches a keyword and prints price and wasPrice per product; schedule it for history.

**Schedule tip:** save any of these inputs as a task in the [Apify Console](https://apify.com/johnvc/walmart-api?fpr=9n7kx3) and attach a schedule. A daily or weekly run turns a one-off pull into a pipeline with zero manual work.

## Usage Examples

Basic input:

```json
{
  "search_mode": "search",
  "query": "laptop",
  "max_results": 10
}
```

Advanced input:

```json
{
  "search_mode": "sellers",
  "item_id": "34X621REEQZQ",
  "store_id": "1932"
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `search_mode` | string | yes | `"search"` | What to fetch. |
| `query` | string | no | none | Required when search mode is 'search'. |
| `item_id` | string | no | none | Required for product, reviews and sellers modes. |
| `store_id` | string | no | none | Optional, used by sellers mode only. |
| `max_results` | integer | no | `100` | How many rows to return before stopping. |

## Output Format

One row from a real run:

```json
{
  "resultType": "seller",
  "productId": "34X621REEQZQ",
  "title": "Nimo Gaming Laptop 17.3 inch",
  "sellerName": "Guangdong Cleamol Technology Company Limited",
  "sellerDisplayName": "Cleamol Co.,Ltd",
  "sellerType": "EXTERNAL",
  "availabilityStatus": "IN_STOCK",
  "price": 1099.59,
  "deliveryDate": "2026-08-06T21:59:00.000Z",
  "deliveryPrice": "$0.00",
  "returnPolicy": "Free 30-day returns"
}
```

## n8n integration

Available as an n8n community node, **[n8n-nodes-walmart-api](https://www.npmjs.com/package/n8n-nodes-walmart-api)**. In n8n: Settings, Community Nodes, install `n8n-nodes-walmart-api`, then use it in any workflow (it also works as an AI Agent tool).

## People also search for

### Is this a Walmart scraper?

Use it wherever you would use one, but it behaves like an API: structured JSON, documented ids, per-result billing, and no proxy or captcha handling on your side.

### How do I track a Walmart price over time?

Run the price_check recipe on a schedule and store price and wasPrice per run. Every row carries the storeId, so keep it fixed for a clean series.

### Which ID do reviews need?

The numeric usItemId. Product and sellers use the alphanumeric productId. Search rows return both, and the API rejects the wrong one before charging you.

### Can I find who sells a product besides Walmart?

That is the sellers mode: every marketplace offer with the storefront name and the registered legal entity behind it.

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Walmart API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings -> Connectors** (or **Settings -> Developer -> Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/walmart-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Walmart API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/walmart-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/walmart-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Walmart API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings -> Connectors -> Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/walmart-api`.
3. In any chat, open **+ -> Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/walmart-api`, using OAuth when prompted.
5. Ask Claude to run the Walmart API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/walmart-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/walmart-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor -> Settings -> MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Walmart API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/walmart-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp


---

Made with care by [johnvc on Apify](https://apify.com/johnvc?fpr=9n7kx3). This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.

Last Updated: 2026.08.09
