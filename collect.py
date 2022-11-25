from web3 import Web3
import csv

host = '100.64.15.176'  # '127.0.0.1'
port = 8545

if __name__ == '__main__':
    url = f'http://{host}:{port}'
    print(f'Connecting to {url}')
    w3 = Web3(Web3.HTTPProvider(url))
    if not w3.isConnected():
        raise Exception(f'Failed to connect to {url}')
    print('Connected.')

    latest = w3.eth.block_number
    block_nums = 100000
    with open('distribute.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Block ID', 'Transactions', 'Gas Used'])
        for i in range(latest - block_nums, latest):
            block = w3.eth.get_block(i)
            writer.writerow([i, len(block['transactions']), block['gasUsed']])

            if i % 1000 == 0:
                print(f'{i}/{latest}')
