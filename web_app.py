"""
Красивый веб-интерфейс для калькулятора обеда
"""

from flask import Flask, render_template_string, request, jsonify
from calculator import calculate_base_cost, validate_order
from discounts import apply_discounts_and_surcharges, is_peak_hour
from optimizer import optimize_meal

app = Flask(__name__)

# Меню столовой с эмодзи
MENU = {
    "1": {"name": "🥗 Цезарь", "price": 150, "emoji": "🥗", "category": "salad"},
    "2": {"name": "🥗 Оливье", "price": 130, "emoji": "🥗", "category": "salad"},
    "3": {"name": "🍜 Борщ", "price": 120, "emoji": "🍜", "category": "soup"},
    "4": {"name": "🍜 Солянка", "price": 140, "emoji": "🍜", "category": "soup"},
    "5": {"name": "🍚 Гречка с котлетой", "price": 180, "emoji": "🍚", "category": "main"},
    "6": {"name": "🍛 Плов", "price": 190, "emoji": "🍛", "category": "main"},
    "7": {"name": "🍝 Макароны с сыром", "price": 150, "emoji": "🍝", "category": "main"},
    "8": {"name": "🥤 Компот", "price": 50, "emoji": "🥤", "category": "drink"},
    "9": {"name": "☕ Чай", "price": 40, "emoji": "☕", "category": "drink"},
    "10": {"name": "☕ Кофе", "price": 80, "emoji": "☕", "category": "drink"}
}

# HTML шаблон с красивым дизайном
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор обеда | Столовая</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            animation: slideIn 0.5s ease-out;
        }

        .main-card {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '🍽️';
            position: absolute;
            font-size: 200px;
            opacity: 0.1;
            right: -30px;
            bottom: -50px;
            transform: rotate(-15deg);
        }

        .header h1 {
            color: white;
            font-size: 3rem;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
        }

        .tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
            padding: 0 20px;
        }

        .tab-btn {
            flex: 1;
            padding: 18px 30px;
            font-size: 1.1rem;
            font-weight: 600;
            background: none;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #6c757d;
            position: relative;
        }

        .tab-btn:hover {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
        }

        .tab-btn.active {
            color: #667eea;
        }

        .tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 3px;
        }

        .tab-content {
            display: none;
            padding: 30px;
            animation: slideIn 0.3s ease-out;
        }

        .tab-content.active {
            display: block;
        }

        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .menu-item {
            background: white;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid #e9ecef;
            position: relative;
            overflow: hidden;
        }

        .menu-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-color: #667eea;
        }

        .menu-item.selected {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-color: #667eea;
        }

        .item-emoji {
            font-size: 3rem;
            margin-bottom: 10px;
        }

        .item-name {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }

        .item-price {
            font-size: 1rem;
            color: #667eea;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .item-count {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .item-count button {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: none;
            background: #667eea;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .item-count button:hover {
            transform: scale(1.1);
            background: #5a67d8;
        }

        .item-count span {
            font-size: 1.2rem;
            font-weight: 600;
            min-width: 30px;
            text-align: center;
        }

        .control-panel {
            background: #f8f9fa;
            border-radius: 20px;
            padding: 25px;
            margin-top: 20px;
        }

        .control-group {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .control-group label {
            font-weight: 600;
            color: #333;
            min-width: 120px;
        }

        .time-slider {
            flex: 1;
            max-width: 300px;
        }

        input[type="range"] {
            width: 100%;
            height: 6px;
            border-radius: 5px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            outline: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }

        .btn {
            padding: 12px 30px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s;
            border: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }

        .btn-secondary {
            background: #e9ecef;
            color: #333;
        }

        .btn-secondary:hover {
            background: #dee2e6;
        }

        .result-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 25px;
            margin-top: 20px;
            display: none;
            color: white;
            animation: slideIn 0.4s ease-out;
        }

        .result-card.show {
            display: block;
        }

        .result-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 15px;
        }

        .result-details {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 15px 0;
        }

        .total-cost {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            padding: 15px;
        }

        .budget-input {
            flex: 1;
            max-width: 200px;
        }

        .budget-input input {
            width: 100%;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ddd;
            font-size: 1rem;
        }

        @media (max-width: 768px) {
            .menu-grid {
                grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            }

            .header h1 {
                font-size: 2rem;
            }

            .tab-btn {
                padding: 12px 15px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-card">
            <div class="header">
                <h1>🍽️ Калькулятор обеда</h1>
                <p>Выберите блюда и получите полную стоимость с учётом скидок и наценок</p>
            </div>

            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('manual')">📝 Ручной выбор</button>
                <button class="tab-btn" onclick="switchTab('optimize')">🎯 Оптимизация под бюджет</button>
            </div>

            <div id="manual-tab" class="tab-content active">
                <div class="menu-grid" id="menu-grid">
                    {% for id, item in menu.items() %}
                    <div class="menu-item" data-id="{{ id }}" data-name="{{ item.name }}" data-price="{{ item.price }}">
                        <div class="item-emoji">{{ item.emoji }}</div>
                        <div class="item-name">{{ item.name }}</div>
                        <div class="item-price">{{ item.price }} ₽</div>
                        <div class="item-count">
                            <button onclick="changeCount('{{ id }}', -1)">−</button>
                            <span id="count-{{ id }}">0</span>
                            <button onclick="changeCount('{{ id }}', 1)">+</button>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <div class="control-panel">
                    <div class="control-group">
                        <label>🕐 Час посещения:</label>
                        <div class="time-slider">
                            <input type="range" id="hour" min="8" max="20" value="12" oninput="updateHour(this.value)">
                        </div>
                        <span id="hour-value" style="font-weight: bold;">12:00</span>
                        <span id="peak-badge" style="margin-left: 10px; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem;"></span>
                    </div>
                    <div class="control-group">
                        <label>💳 Скидочная карта:</label>
                        <label style="display: flex; align-items: center; gap: 10px;">
                            <input type="checkbox" id="has_card" onchange="updateCard(this.checked)">
                            <span>Есть карта лояльности</span>
                        </label>
                    </div>
                    <div style="display: flex; gap: 15px; justify-content: center; margin-top: 20px;">
                        <button class="btn btn-primary" onclick="calculate()">💰 Рассчитать стоимость</button>
                        <button class="btn btn-secondary" onclick="clearAll()">🗑️ Очистить всё</button>
                    </div>
                </div>

                <div id="result" class="result-card">
                    <div class="result-title">📊 Детализация заказа</div>
                    <div id="result-details" class="result-details"></div>
                    <div class="total-cost" id="total-cost"></div>
                </div>
            </div>

            <div id="optimize-tab" class="tab-content">
                <div class="control-panel">
                    <div class="control-group">
                        <label>💰 Ваш бюджет:</label>
                        <div class="budget-input">
                            <input type="number" id="budget" value="300" step="50" placeholder="Введите бюджет">
                        </div>
                    </div>
                    <div class="control-group">
                        <label>🕐 Час посещения:</label>
                        <div class="time-slider">
                            <input type="range" id="opt-hour" min="8" max="20" value="12" oninput="updateOptHour(this.value)">
                        </div>
                        <span id="opt-hour-value" style="font-weight: bold;">12:00</span>
                    </div>
                    <div class="control-group">
                        <label>💳 Скидочная карта:</label>
                        <label>
                            <input type="checkbox" id="opt-has_card">
                            <span>Есть карта лояльности</span>
                        </label>
                    </div>
                    <div style="text-align: center; margin-top: 20px;">
                        <button class="btn btn-primary" onclick="optimize()">🎯 Подобрать оптимальный набор</button>
                    </div>
                </div>

                <div id="opt-result" class="result-card">
                    <div class="result-title">✨ Оптимальный набор для вас</div>
                    <div id="opt-details" class="result-details"></div>
                    <div class="total-cost" id="opt-cost"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedItems = {};

        {% for id in menu.keys() %}
        selectedItems['{{ id }}'] = 0;
        {% endfor %}

        function changeCount(id, delta) {
            let newCount = selectedItems[id] + delta;
            if (newCount >= 0 && newCount <= 5) {
                selectedItems[id] = newCount;
                document.getElementById(`count-${id}`).innerText = newCount;

                let menuItem = document.querySelector(`[data-id="${id}"]`);
                if (newCount > 0) {
                    menuItem.classList.add('selected');
                } else {
                    menuItem.classList.remove('selected');
                }
            }
        }

        function updateHour(value) {
            document.getElementById('hour-value').innerText = value + ':00';
            let peak = [12, 13, 14, 18, 19, 20].includes(parseInt(value));
            let badge = document.getElementById('peak-badge');
            if (peak) {
                badge.innerHTML = '⚠️ Час пик (наценка 20%)';
                badge.style.background = '#ffc107';
                badge.style.color = '#333';
            } else {
                badge.innerHTML = '✅ Обычное время';
                badge.style.background = '#28a745';
                badge.style.color = 'white';
            }
        }

        function updateCard(checked) {
            console.log('Карта:', checked ? 'есть' : 'нет');
        }

        function updateOptHour(value) {
            document.getElementById('opt-hour-value').innerText = value + ':00';
        }

        async function calculate() {
            let items = {};
            for (let [id, count] of Object.entries(selectedItems)) {
                if (count > 0) {
                    let name = document.querySelector(`[data-id="${id}"]`).dataset.name;
                    let price = parseInt(document.querySelector(`[data-id="${id}"]`).dataset.price);
                    items[name] = { price: price, count: count };
                }
            }

            if (Object.keys(items).length === 0) {
                alert('Пожалуйста, выберите хотя бы одно блюдо!');
                return;
            }

            let hour = parseInt(document.getElementById('hour').value);
            let hasCard = document.getElementById('has_card').checked;

            let response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ items: items, hour: hour, has_card: hasCard })
            });

            let data = await response.json();

            let detailsHtml = '';
            data.details.forEach(d => {
                detailsHtml += `<div style="padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">${d}</div>`;
            });

            if (data.discount > 0) {
                detailsHtml += `<div style="padding: 8px 0; color: #ffd700;">✨ Скидка по карте: -${data.discount} руб.</div>`;
            }
            if (data.surcharge > 0) {
                detailsHtml += `<div style="padding: 8px 0; color: #ff9800;">⚠️ Наценка час пик: +${data.surcharge} руб.</div>`;
            }

            document.getElementById('result-details').innerHTML = detailsHtml;
            document.getElementById('total-cost').innerHTML = `💰 Итого: ${data.total} ₽`;
            document.getElementById('result').classList.add('show');
            document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
        }

        async function optimize() {
            let budget = parseFloat(document.getElementById('budget').value);
            let hour = parseInt(document.getElementById('opt-hour').value);
            let hasCard = document.getElementById('opt-has_card').checked;

            let response = await fetch('/optimize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ budget: budget, hour: hour, has_card: hasCard })
            });

            let data = await response.json();

            if (data.items && Object.keys(data.items).length > 0) {
                let detailsHtml = '';
                for (let [name, info] of Object.entries(data.items)) {
                    detailsHtml += `<div style="padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                        🍽️ ${name}: ${info.count} шт. x ${info.price} руб.
                    </div>`;
                }
                document.getElementById('opt-details').innerHTML = detailsHtml;
                document.getElementById('opt-cost').innerHTML = `💰 Итого: ${data.cost} ₽<br>
                    <small style="font-size: 0.9rem;">Отклонение от бюджета: ${data.diff} ₽</small>`;
            } else {
                document.getElementById('opt-details').innerHTML = '<div style="text-align: center;">😔 Не удалось подобрать набор под ваш бюджет</div>';
                document.getElementById('opt-cost').innerHTML = '';
            }
            document.getElementById('opt-result').classList.add('show');
            document.getElementById('opt-result').scrollIntoView({ behavior: 'smooth' });
        }

        function clearAll() {
            for (let id of Object.keys(selectedItems)) {
                selectedItems[id] = 0;
                document.getElementById(`count-${id}`).innerText = '0';
                document.querySelector(`[data-id="${id}"]`).classList.remove('selected');
            }
            document.getElementById('result').classList.remove('show');
        }

        function switchTab(tab) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            document.getElementById('manual-tab').classList.remove('active');
            document.getElementById('optimize-tab').classList.remove('active');
            document.getElementById(tab + '-tab').classList.add('active');
        }

        updateHour(12);
        updateOptHour(12);
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, menu=MENU)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    items = data.get('items', {})
    hour = data.get('hour', 12)
    has_card = data.get('has_card', False)

    if not items:
        return jsonify({'error': 'Ничего не выбрано'})

    base_cost, details = calculate_base_cost(items)
    final_cost, discount, surcharge = apply_discounts_and_surcharges(base_cost, has_card, hour)

    return jsonify({
        'total': final_cost,
        'details': details,
        'discount': discount,
        'surcharge': surcharge
    })


@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    budget = data.get('budget', 300)
    hour = data.get('hour', 12)
    has_card = data.get('has_card', False)

    result = optimize_meal(MENU, budget, has_card, hour)

    if result:
        return jsonify({
            'items': result['items'],
            'cost': result['cost'],
            'diff': abs(result['cost'] - budget)
        })
    return jsonify({'items': {}})


if __name__ == '__main__':
    app.run(debug=True, port=5000)