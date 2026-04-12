from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ФІКСОВАНІ СТАРТОВІ БАЛАНСИ (Щоб не мінялися при перезапуску)
# Я вибрав для тебе гарні рандомні цифри з невеликим розривом
START_BALANCES = {
    "musk": 155.40,
    "zuck": 122.15,
    "bulls": 148.90,
    "bears": 133.60
}

# Реальні баланси, які прийдуть з блокчейну через scanner.py
blockchain_balances = {
    "musk": 0.0,
    "zuck": 0.0,
    "bulls": 0.0,
    "bears": 0.0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/balances')
def get_balances():
    """Віддає суму: ФІКСОВАНИЙ СТАРТ + РЕАЛЬНИЙ БЛОКЧЕЙН"""
    total_balances = {
        "musk": START_BALANCES["musk"] + blockchain_balances["musk"],
        "zuck": START_BALANCES["zuck"] + blockchain_balances["zuck"],
        "bulls": START_BALANCES["bulls"] + blockchain_balances["bulls"],
        "bears": START_BALANCES["bears"] + blockchain_balances["bears"]
    }
    return jsonify(total_balances)

@app.route('/api/update', methods=['POST'])
def update_balances():
    """Приймає дані від scanner.py"""
    data = request.json
    if not data:
        return {"error": "No data"}, 400

    blockchain_balances["musk"] = data.get("musk", blockchain_balances["musk"])
    blockchain_balances["zuck"] = data.get("zuck", blockchain_balances["zuck"])
    blockchain_balances["bulls"] = data.get("bulls", blockchain_balances["bulls"])
    blockchain_balances["bears"] = data.get("bears", blockchain_balances["bears"])

    print(f"📊 Blockchain Sync: Musk +${blockchain_balances['musk']} | Zuck +${blockchain_balances['zuck']}")
    return {"status": "success"}, 200

if __name__ == '__main__':
    # Включаємо debug=True для розробки у VS Code
    app.run(debug=True, port=5000)