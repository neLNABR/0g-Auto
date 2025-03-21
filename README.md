# 🌐 0G Auto

**Этот инструмент автоматизирует взаимодействие с различными функциями в сети, включая операции с токенами и смарт-контрактами.**  
*This tool automates interaction with various functions in the network, including token operations and smart contracts.*

---

## ⚙️ Доступные функции / Available Features

### 💧 ФАУСЕТЫ / FAUCETS
- `"faucet"` — получение токенов из фаусета  
  *Receive tokens from faucet*
- `"faucet_tokens"` — получение различных токенов  
  *Receive different types of tokens*

### 🚀 ДЕПЛОЙ / DEPLOY
- `"storagescan_deploy"` — деплой контракта на StorageScan  
  *Deploy a contract on StorageScan*

### 🎨 NFT
- `"conft_mint"` — минт NFT и домена  
  *Mint an NFT and domain*

### 🔄 СВАПЫ / SWAPS
- `"swaps"` — свап токенов  
  *Token swaps*

---

## 📋 Требования / Requirements
- Python 3.11.6 или выше  
  *Python 3.11.6 or higher*

---

## 📦 Установка / Installation

### 1. Клонируйте репозиторий / Clone the repository
```bash
git clone https://github.com/neLNABR/0g-Auto.git
cd 0g-Auto
```

### 2. Установите зависимости / Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Настройте конфигурацию / Configure your settings
Измените параметры в `config.yaml`  
*Edit your configuration in `config.yaml`*

### 4. Добавьте ваши данные / Add your data:
- `data/private_keys.txt` — один приватный ключ на строку  
  *one private key per line*
- `data/proxies.txt` — один прокси на строку (формат: `user:pass@ip:port`)  
  *one proxy per line (format: `user:pass@ip:port`)*  
  **Поддерживаются только HTTP прокси / Only HTTP proxies are supported**

### 5. Запустите бот / Run the bot
```bash
python main.py
```

---

## 📲 Настройка логов в Telegram / Telegram Logging

В `config.yaml` вы можете включить логирование в Telegram:  
*In `config.yaml` you can enable Telegram log reporting:*

```yaml
SEND_TELEGRAM_LOGS: false         # включение/выключение логов / enable/disable logs
TELEGRAM_BOT_TOKEN: "ваш_токен"   # токен бота от @BotFather / bot token from @BotFather
TELEGRAM_USERS_IDS: [ваш_id]      # Telegram ID получателей логов / list of Telegram user IDs
```

---

## 🧪 Disclaimer

This tool is provided **for educational and testing purposes only**.  
Use at your own risk. Any misuse, including abuse of the 0g network, may lead to penalties or blacklisting.

---

## 📄 License

MIT
