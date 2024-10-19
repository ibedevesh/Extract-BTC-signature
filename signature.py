import requests
from datetime import datetime
import binascii

def get_btc_wallet_info(address, offset=0):
    url = f"https://blockchain.info/rawaddr/{address}?offset={offset}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data: HTTP {response.status_code}")
        return None, None, None
    data = response.json()
    wallet_info = {
        'address': data['address'],
        'total_received': data['total_received'] / 1e8,
        'total_sent': data['total_sent'] / 1e8,
        'final_balance': data['final_balance'] / 1e8,
        'n_tx': data['n_tx']
    }
    return wallet_info, data['txs'], data.get('n_tx', 0)

def extract_signature(script_hex):
    try:
        # Convert hex to bytes
        script_bytes = binascii.unhexlify(script_hex)
        
        # The signature is typically the second element in the script
        # It starts after the first opcode (usually 0x48 or 0x47 for the signature length)
        sig_start = 1
        sig_length = script_bytes[sig_start]
        
        # Extract the signature (excluding the hash type byte at the end)
        signature = script_bytes[sig_start+1:sig_start+1+sig_length-1]
        
        return binascii.hexlify(signature).decode('ascii')
    except Exception as e:
        print(f"Error extracting signature: {e}")
        return None

def analyze_transactions(address):
    offset = 0
    all_transactions = []
    total_txs = None

    while total_txs is None or len(all_transactions) < total_txs:
        wallet_info, transactions, n_tx = get_btc_wallet_info(address, offset)
        if wallet_info is None:
            break
        if total_txs is None:
            total_txs = n_tx
            print(f"\nTotal number of transactions: {total_txs}")
        all_transactions.extend(transactions)
        offset += len(transactions)
        print(f"Fetched {len(all_transactions)} out of {total_txs} transactions")

    sent_txs = []

    for tx in all_transactions:
        for input in tx['inputs']:
            if input.get('prev_out', {}).get('addr') == address:
                script = input.get('script', '')
                signature = extract_signature(script)
                if signature:
                    sent_txs.append({
                        'txid': tx['hash'],
                        'time': datetime.fromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M:%S'),
                        'signature': signature
                    })
                break
    
    return sent_txs

if __name__ == "__main__":
    wallet_address = input("Enter the Bitcoin wallet address: ")
    
    wallet_info, _, _ = get_btc_wallet_info(wallet_address)
    if wallet_info:
        print("\nWallet Information:")
        print(f"Address: {wallet_info['address']}")
        print(f"Total Received: {wallet_info['total_received']:.8f} BTC")
        print(f"Total Sent: {wallet_info['total_sent']:.8f} BTC")
        print(f"Final Balance: {wallet_info['final_balance']:.8f} BTC")
        print(f"Number of Transactions: {wallet_info['n_tx']}")
        print()
    else:
        print("Failed to retrieve wallet information.")
        exit()

    print("Analyzing transactions...")
    sent_txs = analyze_transactions(wallet_address)

    if sent_txs:
        print(f"\nFound {len(sent_txs)} sent transactions with signatures:")
        for tx in sent_txs:
            print(f"Transaction ID: {tx['txid']}")
            print(f"Time: {tx['time']}")
            print(f"Signature: {tx['signature']}")
            print("---")
        
        print("\nSignatures:")
        for i, tx in enumerate(sent_txs, 1):
            print(f"{i}. {tx['signature']}")
    else:
        print("\nNo sent transactions with signatures found for this address.")
