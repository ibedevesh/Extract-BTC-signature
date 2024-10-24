# Bitcoin Wallet Analyzer

This project provides a **Bitcoin wallet analyzer** that retrieves wallet information, fetches transactions from the **Blockchain.info API**, and extracts cryptographic signatures from sent transactions.

---

## Features

- **Retrieve wallet information**: Total BTC received, sent, and the final balance.
- **Fetch and analyze transactions**: Identify sent transactions from the wallet.
- **Extract digital signatures** from transaction inputs.
- **Error handling** for API requests and data parsing issues.

---

## Prerequisites

1. **Python 3.x** installed on your machine.
2. Install the required Python packages:
   ```bash
   pip install requests
