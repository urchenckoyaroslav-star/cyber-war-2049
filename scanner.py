import requests
import time

SERVER_URL = "http://127.0.0.1:5000/api/update"

# Твои 4 BEP20 кошелька
WALLETS = {
    "musk": "0x6d60e0e6b581aa27fde2608ad55d86e67b705573",
    "zuck": "0x5a289561bf0bbd6b6748d8dcda2e37ef8d6d120a",
    "bulls": "0xa4871e3de547f04b2130b7163e4e426300bf6634",
    "bears": "0x748f510de5c5c1f89f160b6e557b464e18f09d91"
}

# Смарт-контракт USDT в сети Binance Smart Chain (BEP20)
USDT_BSC_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"

def get_usdt_balance_bsc(address):
    """Тянет баланс USDT (BEP20) через публичный BscScan API"""
    try:
        url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={USDT_BSC_CONTRACT}&address={address}&tag=latest"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10).json()
        
        if res.get('status') == '1':
            # В BSC у USDT 18 нулей (decimals)
            raw_balance = float(res.get('result', 0))
            return raw_balance / (10 ** 18)
        return 0.0
    except Exception as e:
        print(f"⚠️ Ошибка сканирования {address}: {e}")
        return 0.0

print("🚀 BSC BLOCKCHAIN SCANNER INITIATED...")

while True:
    new_balances = {}
    print(f"\n[{time.strftime('%H:%M:%S')}] Checking BEP20 balances...")
    
    for team, address in WALLETS.items():
        balance = get_usdt_balance_bsc(address)
        new_balances[team] = balance
        print(f" - {team.upper()}: ${balance:.2f}")
        time.sleep(1) # Задержка, чтобы BscScan не заблочил за спам запросами

    try:
        requests.post(SERVER_URL, json=new_balances)
        print("✅ Data successfully sent to server.")
    except:
        print("❌ Server is offline.")

    # Ждем 3 минуты до следующего сканирования
    time.sleep(180)