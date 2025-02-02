from web3 import Web3
from eth_account import Account
import time
import os
from config import networks, private_keys, my_addresses, labels, data_bridge
import codecs

# Fungsi untuk memusatkan teks
def center_text(text):
    terminal_width = os.get_terminal_size().columns
    lines = text.splitlines()
    centered_lines = [line.center(terminal_width) for line in lines]
    return "\n".join(centered_lines)

# Fungsi untuk membersihkan terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

ascii_art = """

   █████████   █████ ███████████   ██████████   ███████████      ███████    ███████████       █████████    █████████    █████████
  ███░░░░░███ ░░███ ░░███░░░░░███ ░░███░░░░███ ░░███░░░░░███   ███░░░░░███ ░░███░░░░░███     ███░░░░░███  ███░░░░░███  ███░░░░░███
 ░███    ░███  ░███  ░███    ░███  ░███   ░░███ ░███    ░███  ███     ░░███ ░███    ░███    ░███    ░███ ░███    ░░░  ███     ░░░
 ░███████████  ░███  ░██████████   ░███    ░███ ░██████████  ░███      ░███ ░██████████     ░███████████ ░░█████████ ░███         
 ░███░░░░░███  ░███  ░███░░░░░███  ░███    ░███ ░███░░░░░███ ░███      ░███ ░███░░░░░░      ░███░░░░░███  ░░░░░░░░███░███         
 ░███    ░███  ░███  ░███    ░███  ░███    ███  ░███    ░███ ░░███     ███  ░███            ░███    ░███  ███    ░███░░███     ███
 █████   █████ █████ █████   █████ ██████████   █████   █████ ░░░███████░   █████           █████   █████░░█████████  ░░█████████
 ░░░░░   ░░░░░ ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░   ░░░░░   ░░░░░    ░░░░░░░    ░░░░░           ░░░░░   ░░░░░  ░░░░░░░░░    ░░░░░░░░░ 

"""

description = """

"""

chain_symbols = {
    'ARB Sepolia': '\033[34m',
    'OP Sepolia': '\033[91m',
    'Blast Sepolia': '\033[93m',
    'Base Sepolia': '\033[96m'
}

green_color = '\033[92m'
reset_color = '\033[0m'
menu_color = '\033[95m'

explorer_urls = {
    'ARB Sepolia': 'https://sepolia.arbiscan.io/tx/',
    'OP Sepolia': 'https://sepolia-optimism.etherscan.io/tx/',
    'Blast Sepolia': 'https://testnet.blastscan.io/tx/',
    'Base Sepolia': 'https://sepolia.basescan.org/tx/',
    'BRN': 'https://brn.explorer.caldera.xyz/tx/'
}

def get_brn_balance(web3, my_address):
    balance = web3.eth.get_balance(my_address)
    return web3.from_wei(balance, 'ether')

def send_bridge_transaction(web3, account, my_address, data, network_name):
    my_address = Web3.to_checksum_address(my_address)  # Mengonversi alamat ke format checksum
    nonce = web3.eth.get_transaction_count(my_address, 'pending')
    value_in_ether = 0.8
    value_in_wei = web3.to_wei(value_in_ether, 'ether')

    try:
        gas_estimate = web3.eth.estimate_gas({
            'to': networks[network_name]['contract_address'],
            'from': my_address,
            'data': data,
            'value': value_in_wei
        })
        gas_limit = gas_estimate + 50000
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return None

    base_fee = web3.eth.get_block('latest')['baseFeePerGas']
    priority_fee = web3.to_wei(5, 'gwei')
    max_fee = base_fee + priority_fee

    transaction = {
        'nonce': nonce,
        'to': networks[network_name]['contract_address'],
        'value': value_in_wei,
        'gas': gas_limit * 2,
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': priority_fee,
        'chainId': networks[network_name]['chain_id'],
        'data': data
    }

    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, account.key)
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        balance = web3.eth.get_balance(my_address)
        formatted_balance = web3.from_wei(balance, 'ether')
        brn_balance = get_brn_balance(Web3(Web3.HTTPProvider('https://brn.rpc.caldera.xyz/http')), my_address)
        explorer_link = f"{explorer_urls[network_name]}{web3.to_hex(tx_hash)}"

        print(f"{green_color} Alamat Pengirim: {account.address}")
        print(f"⛽ Gas digunakan: {tx_receipt['gasUsed']}")
        print(f"️  Nomor blok: {tx_receipt['blockNumber']}")
        print(f" Saldo ETH: {formatted_balance} ETH")
        print(f" Saldo BRN: {brn_balance} BRN")
        print(f" Link Explorer: {explorer_link}\n{reset_color}")

        return web3.to_hex(tx_hash), value_in_ether
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None, None

def process_network_transactions(network_name, bridges, chain_data, successful_txs):
    web3 = Web3(Web3.HTTPProvider(chain_data['rpc_url']))
    if not web3.is_connected():
        raise Exception(f"Tidak dapat terhubung ke jaringan {network_name}")

    for bridge in bridges:
        for i, private_key in enumerate(private_keys):
            account = Account.from_key(private_key)
            data = data_bridge[bridge]
            result = send_bridge_transaction(web3, account, my_addresses[i], data, network_name)
            if result:
                tx_hash, value_sent = result
                successful_txs += 1
                if value_sent is not None:
                    print(f"{chain_symbols[network_name]} Total Tx Sukses: {successful_txs} | {labels[i]} | Bridge: {bridge} | Jumlah Bridge: {value_sent:.5f} ETH ✅{reset_color}\n")
                else:
                    print(f"{chain_symbols[network_name]} Total Tx Sukses: {successful_txs} | {labels[i]} | Bridge: {bridge} ✅{reset_color}\n")
                print(f"{'='*150}")
                print("\n")
            time.sleep(3)

    return successful_txs

def display_menu():
    print(f"{menu_color}Pilih chain untuk menjalankan transaksi:{reset_color}")
    print("")
    print(f"{chain_symbols['OP Sepolia']}1. OP -> BASE Sepolia{reset_color}")
    print(f"{chain_symbols['Base Sepolia']}2. BASE -> OP Sepolia{reset_color}")
    print(f"{chain_symbols['ARB Sepolia']}3. BASE -> ARB Sepolia{reset_color}")
    print(f"{chain_symbols['ARB Sepolia']}4. ARB -> BASE Sepolia{reset_color}")
    print(f"{menu_color}5. Run All & Looping (Recommended) {reset_color}")
    print("")
    choice = input("choose (1-5): ")
    return choice

def main():
    print("\033[92m" + center_text(ascii_art) + "\033[0m")
    print(center_text(description))
    print("\n\n")

    successful_txs = 0

    while True:
        choice = display_menu()
        clear_terminal()
        print("\033[92m" + center_text(ascii_art) + "\033[0m")
        print(center_text(description))
        print("\n\n")

        try:
            if choice == '1':
                print(f"{menu_color}Jalankan transaksi OP -> BASE Sepolia secara terus-menerus...{reset_color}")
                while True:
                    successful_txs = process_network_transactions('OP Sepolia', ["OP - BASE"], networks['OP Sepolia'], successful_txs)
                    print("Wait 5s for Safety (OP -> BASE)...")
                    time.sleep(5)

            elif choice == '2':
                print(f"{menu_color}Jalankan transaksi BASE -> OP Sepolia secara terus-menerus...{reset_color}")
                while True:
                    successful_txs = process_network_transactions('Base Sepolia', ["BASE - OP"], networks['Base Sepolia'], successful_txs)
                    print("Wait 5s for Safety (BASE -> OP)...")
                    time.sleep(5)

            elif choice == '3':
                print(f"{menu_color}Jalankan transaksi BASE -> ARB Sepolia secara terus-menerus...{reset_color}")
                while True:
                    successful_txs = process_network_transactions('Base Sepolia', ["BASE - ARB"], networks['Base Sepolia'], successful_txs)
                    print("Wait 5s for Safety (BASE -> ARB)...")
                    time.sleep(5)

            elif choice == '4':
                print(f"{menu_color}Jalankan transaksi ARB -> BASE Sepolia secara terus-menerus...{reset_color}")
                while True:
                    successful_txs = process_network_transactions('ARB Sepolia', ["ARB - BASE"], networks['ARB Sepolia'], successful_txs)
                    print("Wait 5s for Safety (ARB -> BASE)...")
                    time.sleep(5)

            elif choice == '5':
                print(f"{menu_color}Jalankan transaksi secara terus-menerus dari OP -> BASE, BASE -> OP, BASE -> ARB, ARB -> BASE{reset_color}")
                while True:
                    successful_txs = process_network_transactions('OP Sepolia', ["OP - BASE"], networks['OP Sepolia'], successful_txs)
                    print("Wait 5s for Safety (OP -> BASE)...")
                    time.sleep(5)

                    successful_txs = process_network_transactions('Base Sepolia', ["BASE - OP"], networks['Base Sepolia'], successful_txs)
                    print("Wait 5s for Safety (BASE -> OP)...")
                    time.sleep(5)

                    successful_txs = process_network_transactions('Base Sepolia', ["BASE - ARB"], networks['Base Sepolia'], successful_txs)
                    print("Wait 5s for Safety (BASE -> ARB)...")
                    time.sleep(5)

                    successful_txs = process_network_transactions('ARB Sepolia', ["ARB - BASE"], networks['ARB Sepolia'], successful_txs)
                    print("Wait 5s for Safety (ARB -> BASE)...")
                    time.sleep(5)

        except Exception as e:
            print(f"Error cok ^^ {e}")
            print("Wait 10s for Safety...")
            time.sleep(10)

if __name__ == "__main__":
    main()