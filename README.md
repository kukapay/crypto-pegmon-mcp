# Crypto-Pegmon-MCP

An MCP server that tracks stablecoin peg integrity across multiple blockchains, helping AI agents detect depegging risks before they escalate.

<a href="https://glama.ai/mcp/servers/@kukapay/crypto-pegmon-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@kukapay/crypto-pegmon-mcp/badge" alt="crypto-pegmon-mcp MCP server" />
</a>

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Stability Reports**: Generate detailed reports assessing stablecoin peg stability, including maximum deviation and status (Stable, Moderately Stable, Unstable).
- **Real-Time Price Monitoring**: Fetch current prices and calculate peg deviation from $1 for USD-pegged stablecoins.
- **Historical Data Analysis**: Retrieve historical price data (up to 7 days by default) in Markdown table format.
- **Supported Stablecoins**: Monitor 17 USD-pegged stablecoins, such as Tether (USDT), USD Coin (USDC), Dai (DAI), and yield-bearing tokens like Ethena Staked USDe (eUSDe).
- **User-Friendly Output**: All data is presented in clean Markdown format for easy integration into reports or dashboards.

## Supported Stablecoins

The server supports the following USD-pegged stablecoins:

| Symbol     | Description                                            |
|------------|--------------------------------------------------------|
| USDT       | Tether's USD-pegged stablecoin, centrally issued.      |
| USDC       | Circle's USD-backed stablecoin, widely used in DeFi.   |
| DAI        | Decentralized stablecoin by MakerDAO, collateralized by crypto. |
| BUSD       | Binance's USD-pegged stablecoin, centrally managed.    |
| TUSD       | TrueUSD, a USD-backed stablecoin by TrustToken.        |
| FRAX       | Fractional-algorithmic USD stablecoin by Frax Finance. |
| USDD       | TRON's USD-pegged stablecoin, centrally issued.        |
| USDS       | USD-pegged stablecoin, focused on stability.           |
| SUSDS      | Staked USDS, yield-bearing stablecoin.                 |
| EUSDE      | Ethena's staked USD stablecoin, yield-bearing.         |
| USDY       | Ondo's USD yield stablecoin, designed for returns.     |
| PYUSD      | PayPal's USD-pegged stablecoin for payments.           |
| GUSD       | Gemini Dollar, USD-backed by Gemini Trust.             |
| USDP       | Paxos Standard, a regulated USD stablecoin.            |
| AAVE-USDC  | Aave's USD-pegged stablecoin for lending.              |
| CURVE-USD  | Curve Finance's USD stablecoin for DeFi pools.         |
| MIM        | Magic Internet Money, a decentralized USD stablecoin.  |

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management and running)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/crypto-pegmon-mcp.git
   cd crypto-pegmon-mcp
   ```

2. **Install Dependencies**:
   Using uv (recommended):
   ```bash
   uv sync
   ```

3. **Run the Server**:
   Using uv (recommended):
   ```bash
   uv run main.py
   ```

## Usage

The server provides four tools, accessible via the MCP interface. Below are examples for each tool and prompt.

### 1. List Supported Stablecoins
Retrieve a list of supported stablecoins with their descriptions.

- **Prompt**:
  ```plaintext
  List all supported stablecoins with their descriptions.
  ```
- **Output**:
  ```markdown
  **Supported USD-Pegged Stablecoins**:

  | Symbol     | Description                                            |
  |------------|--------------------------------------------------------|
  | USDT       | Tether's USD-pegged stablecoin, centrally issued.      |
  | USDC       | Circle's USD-backed stablecoin, widely used in DeFi.   |
  | ...        | ...                                                    |
  ```

### 2. Fetch Current Price
Get the current price and peg deviation for a specific stablecoin.

- **Prompt**:
  ```plaintext
  Get the current price of USDT.
  ```
- **Output**:
  ```markdown
  **USDT Current Price**: $1.0002, Peg Deviation: 0.02%
  ```

### 3. Fetch Historical Data
Retrieve historical price data for a stablecoin over a specified number of days (default: 7).

- **Prompt**:
  ```plaintext
  Show the price history of USDC for the last 7 days.
  ```
- **Output**:
  ```markdown
  **USDC Historical Data (Last 7 Days)**:

  | Date       | Price  | Deviation (%) |
  |------------|--------|---------------|
  | 2025-04-29 | 1.0001 | 0.0100        |
  | 2025-04-30 | 0.9998 | -0.0200       |
  | ...        | ...    | ...           |
  ```

### 4. Analyze Peg Stability
Generate a comprehensive stability report for a stablecoin, including historical data, current price, and analysis.

- **Prompt**:
  ```plaintext
  Analyze the peg stability of DAI over the past week.
  ```
- **Output**:
  ```markdown
  - **DAI Historical Data (Last 7 Days)**:
    | Date       | Price  | Deviation (%) |
    |------------|--------|---------------|
    | 2025-04-29 | 1.0003 | 0.0300        |
    | ...        | ...    | ...           |
  - **DAI Current Price**: $1.0000, Peg Deviation: 0.00%
  - **Stability Analysis for DAI**:
    - Maximum Deviation: 0.15%
    - Stability Status: Stable
    - Note: Deviations > 3% indicate potential depegging risks.
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.