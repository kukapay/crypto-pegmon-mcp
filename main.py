from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import json

# Initialize MCP server with specified name and dependencies
mcp = FastMCP("Crypto-Pegmon-MCP", dependencies=["pycoingecko", "pandas"])

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

# Supported USD-pegged stablecoins with their CoinGecko API IDs and descriptions
STABLECOINS = {
    "usdt": {
        "id": "tether",
        "description": "Tether's USD-pegged stablecoin, centrally issued."
    },
    "usdc": {
        "id": "usd-coin",
        "description": "Circle's USD-backed stablecoin, widely used in DeFi."
    },
    "dai": {
        "id": "dai",
        "description": "Decentralized stablecoin by MakerDAO, collateralized by crypto."
    },
    "busd": {
        "id": "binance-usd",
        "description": "Binance's USD-pegged stablecoin, centrally managed."
    },
    "tusd": {
        "id": "true-usd",
        "description": "TrueUSD, a USD-backed stablecoin by TrustToken."
    },
    "frax": {
        "id": "frax",
        "description": "Fractional-algorithmic USD stablecoin by Frax Finance."
    },
    "usdd": {
        "id": "usdd",
        "description": "TRON's USD-pegged stablecoin, centrally issued."
    },
    "usds": {
        "id": "usds",
        "description": "USD-pegged stablecoin, focused on stability."
    },
    "susds": {
        "id": "susds",
        "description": "Staked USDS, yield-bearing stablecoin."
    },
    "eusde": {
        "id": "ethena-staked-usde",
        "description": "Ethena's staked USD stablecoin, yield-bearing."
    },
    "usdy": {
        "id": "ondo-us-dollar-yield",
        "description": "Ondo's USD yield stablecoin, designed for returns."
    },
    "pyusd": {
        "id": "paypal-usd",
        "description": "PayPal's USD-pegged stablecoin for payments."
    },
    "gusd": {
        "id": "gemini-dollar",
        "description": "Gemini Dollar, USD-backed by Gemini Trust."
    },
    "usdp": {
        "id": "paxos-standard",
        "description": "Paxos Standard, a regulated USD stablecoin."
    },
    "aave-usdc": {
        "id": "aave-usdc",
        "description": "Aave's USD-pegged stablecoin for lending."
    },
    "curve-usd": {
        "id": "curve-usd",
        "description": "Curve Finance's USD stablecoin for DeFi pools."
    },
    "mim": {
        "id": "magic-internet-money",
        "description": "Magic Internet Money, a decentralized USD stablecoin."
    }
}

# Tool to fetch the list of supported stablecoins with descriptions
@mcp.tool()
def get_supported_stablecoins() -> str:
    """
    Fetch the list of supported USD-pegged stablecoins with their symbols and descriptions.

    Returns:
        str: A Markdown-formatted table listing stablecoin symbols and their descriptions.
    """
    # Create DataFrame for stablecoins and descriptions
    df = pd.DataFrame([
        {"Symbol": coin.upper(), "Description": STABLECOINS[coin]["description"]}
        for coin in STABLECOINS.keys()
    ])
    
    # Convert to Markdown table
    markdown_table = df.to_markdown(index=False)
    return f"**Supported USD-Pegged Stablecoins**:\n\n{markdown_table}"

# Tool to fetch current price of a stablecoin
@mcp.tool()
def get_current_price(coin: str) -> str:
    """
    Fetch the current price of a USD-pegged stablecoin in USD and calculate peg deviation.

    Args:
        coin (str): The symbol of the stablecoin (e.g., 'usdt', 'usdc', 'dai').

    Returns:
        str: A string with the current price and peg deviation in Markdown format.
    """
    if coin.lower() not in STABLECOINS:
        return f"Error: Unsupported stablecoin. Choose from {list(STABLECOINS.keys())}"
    
    coin_id = STABLECOINS[coin.lower()]["id"]
    try:
        data = cg.get_price(ids=coin_id, vs_currencies="usd")
        price = data[coin_id]["usd"]
        deviation = (price - 1.0) * 100  # Calculate deviation as percentage
        return f"**{coin.upper()} Current Price**: ${price:.4f}, Peg Deviation: {deviation:.2f}%"
    except Exception as e:
        return f"Error fetching price for {coin}: {str(e)}"

# Tool to fetch historical price data for a stablecoin
@mcp.tool()
def get_historical_data(coin: str, days: int = 7) -> str:
    """
    Fetch historical price data for a USD-pegged stablecoin and return as a Markdown table.

    Args:
        coin (str): The symbol of the stablecoin (e.g., 'usdt', 'usdc', 'dai').
        days (int, optional): Number of days for historical data. Defaults to 7.

    Returns:
        str: A Markdown table with date, price, and deviation.
    """
    if coin.lower() not in STABLECOINS:
        return f"Error: Unsupported stablecoin. Choose from {list(STABLECOINS.keys())}"
    
    coin_id = STABLECOINS[coin.lower()]["id"]
    try:
        # Fetch historical data for the specified number of days
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency="usd", days=days)
        prices = [(datetime.fromtimestamp(item[0]/1000).strftime("%Y-%m-%d"), item[1]) 
                  for item in data["prices"]]
        
        # Create DataFrame for prices and deviations
        df = pd.DataFrame(prices, columns=["Date", "Price"])
        df["Deviation (%)"] = (df["Price"] - 1.0) * 100
        
        # Convert to Markdown table
        markdown_table = df.to_markdown(index=False, floatfmt=".4f")
        return f"**{coin.upper()} Historical Data (Last {days} Days)**:\n\n{markdown_table}"
    except Exception as e:
        return f"Error fetching historical data for {coin}: {str(e)}"

# Tool to analyze peg stability of a stablecoin
@mcp.tool()
def analyze_peg_stability(coin: str, days: int = 7) -> str:
    """
    Generate a peg stability analysis report for a USD-pegged stablecoin.

    Args:
        coin (str): The symbol of the stablecoin (e.g., 'usdt', 'usdc', 'dai').
        days (int, optional): Number of days for analysis. Defaults to 7.

    Returns:
        str: A Markdown-formatted report with historical data, current price, and stability analysis.
    """
    if coin.lower() not in STABLECOINS:
        return f"Error: Unsupported stablecoin. Choose from {list(STABLECOINS.keys())}"
    
    historical_data = get_historical_data(coin, days)
    current_price = get_current_price(coin)
    
    try:
        df = pd.read_json(json.dumps(cg.get_coin_market_chart_by_id(
            id=STABLECOINS[coin.lower()]["id"], vs_currency="usd", days=days)["prices"]))
        df.columns = ["Timestamp", "Price"]
        df["Deviation"] = (df["Price"] - 1.0) * 100
        max_deviation = df["Deviation"].abs().max()
        stability_note = "Stable" if max_deviation < 1.0 else "Unstable" if max_deviation > 3.0 else "Moderately Stable"
        
        return (
            f"**Peg Stability Analysis for {coin.upper()} (Last {days} Days)**:\n\n"
            f"{historical_data}\n\n"
            f"{current_price}\n\n"
            f"**Analysis**:\n"
            f"- Maximum Deviation: {max_deviation:.2f}%\n"
            f"- Stability Status: {stability_note}\n"
            f"- Note: Deviations > 3% indicate potential depegging risks."
        )
    except Exception as e:
        return f"Error in analysis for {coin}: {str(e)}"
        
# Run the MCP server
if __name__ == "__main__":
    mcp.run()
