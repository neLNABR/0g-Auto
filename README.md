# 🌐 0G Auto – Automation for the 0G Blockchain (Galileo Compatible)

> **0G Auto** is a powerful tool to automate tasks involving tokens, smart contracts, and services on the **0G Network**.  
> _0G Auto — мощный инструмент для автоматизации работы с токенами, смарт-контрактами и сервисами в сети 0G._

---

## ⚠️ Important Notice / Важно

🚨 **Faucet Access via Twitter Only!**  
_Фаусет работает только через Twitter!_

- 🕒 Twitter account must be over **30 days old**  
  _Твиттер-аккаунт должен быть создан более 30 дней назад_
- 👥 Must have at least **10 followers**  
  _Нужно иметь минимум 10 подписчиков_

📩 **Support:** [@jackthedevv](https://t.me/jackthedevv)

---

## ⚙️ Features / Возможности

### 💧 Faucets / Фаусеты
- `faucet` – Claim tokens from faucet  
  _Получение токенов из фаусета_
- `faucet_tokens` – Request multiple token types  
  _Запрос разных типов токенов_

### 🛠️ Deployment / Деплой
- `easynode_deploy` – Launch a node via EasyNode  
  _Деплой ноды через EasyNode_
- `storagescan_deploy` – Deploy smart contracts via StorageScan  
  _Размещение смарт-контрактов через StorageScan_
- `mintair_deploy` – Deploy via MintAir  
  _Деплой через MintAir_

### 🔄 Token Swaps / Обмен токенов
- `zero_exchange_swaps` – Swap tokens using Zero Exchange  
  _Обмен токенов через Zero Exchange_

### 🎮 Games / Игры
- `puzzlemania` – Auto-play PuzzleMania  
  _Автоматическая игра в PuzzleMania_

---

## 📦 Installation / Установка

### 1️⃣ Clone the Repository / Клонируйте репозиторий
```bash
git clone https://github.com/neLNABR/0g-Auto.git
cd 0g-Auto
```

### 2️⃣ Install Dependencies / Установите зависимости
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Settings / Настройка конфигурации
Edit the file: `config.yaml`  
_Измените параметры в `config.yaml`_

### 4️⃣ Add Your Data / Добавьте данные
- `data/twitter_token.txt` – one token per line  
  _Один токен на строку_
- `data/referral_codes.txt` – one referral code per line  
  _Один ключ на строку_
- `data/private_keys.txt` – one private key per line  
  _Один приватный ключ на строку_
- `data/proxies.txt` – one HTTP proxy per line (`user:pass@ip:port`)  
  _Один прокси на строку (**только HTTP!**)_

### 5️⃣ Run the Bot / Запуск бота
```bash
python main.py
```

---

## 📲 Telegram Logs / Телеграм-отчеты

To enable logging to Telegram, modify `config.yaml`:  
_Чтобы включить отчеты в Telegram, настройте `config.yaml`:_

```yaml
SEND_TELEGRAM_LOGS: true
TELEGRAM_BOT_TOKEN: "your_bot_token"
TELEGRAM_USERS_IDS: [your_user_id]
```

---

## 🧪 Disclaimer / Отказ от ответственности

This tool is for **educational and testing purposes only**. Use at your own risk.  
_Инструмент предоставляется **только в образовательных и тестовых целях**. Используйте на свой страх и риск._  
_Misuse may result in penalties or blacklisting._  
_Злоупотребление может привести к санкциям или блокировке._

---

## 📄 License / Лицензия

**MIT License** – Free to use with attribution.  
_Свободное использование с указанием авторства._

