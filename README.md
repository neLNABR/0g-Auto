# 🌐 0G Auto. Works with Galileo (latest blockchain version)

**0G Auto — это инструмент для автоматизации работы с токенами, смарт-контрактами и разными сервисами сети 0G.**

*This tool automates work with tokens, smart contracts, and various 0G network services.*

---

# ⚠️ ВАЖНО / IMPORTANT

> **Сейчас faucet работает только через Twitter!**
> - Твиттер-аккаунт должен быть создан более 30 дней назад.
> - Нужно иметь минимум 10 подписчиков.
>
> **The faucet now works only via Twitter!**
> - Your Twitter account must be older than 30 days.
> - Your account must have at least 10 followers.

> **Support @jackthedevv**
---

## ⚙️ Доступные функции / Available Features

### 💧 Фаусеты / Faucets
- `faucet` — получение токенов из фаусета / Receive tokens from faucet
- `faucet_tokens` — запрос разных типов токенов / Request different types of tokens

### 🛠️ Деплой / Deploy
- `easynode_deploy` — деплой ноды через EasyNode / Deploy a node via EasyNode
- `storagescan_deploy` — деплой смарт-контрактов через StorageScan / Deploy smart contracts via StorageScan
- `mintair_deploy` — деплой через MintAir / Deploy via MintAir

### 🔄 Свапы / Swaps
- `zero_exchange_swaps` — обмен токенов через Zero Exchange / Token swap via Zero Exchange

### 🎮 Игры / Games
- `puzzlemania` — автоигра PuzzleMania / Auto play PuzzleMania

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

### 4. Добавьте ваши данные / Add your data:
- `data/twitter_token.txt` — один токен на строку // one token per line 
- `data/referral_codes.txt` — один ключ на строку // one referral code per line 
- `data/private_keys.txt` — один приватный ключ на строку // one private key per line 
- `data/proxies.txt` — один прокси на строку (`user:pass@ip:port`) (**поддерживаются только HTTP-прокси!**) 

### 5. Запустите бота / Run the bot
```bash
python main.py
```

---

## 📢 Telegram Логи / Telegram Logs

В `config.yaml` вы можете настроить отчеты в Telegram:

```yaml
SEND_TELEGRAM_LOGS: false
TELEGRAM_BOT_TOKEN: "your_bot_token"
TELEGRAM_USERS_IDS: [your_user_id]
```

---

## 🧪 Disclaimer

This tool is provided **for educational and testing purposes only**.
Use at your own risk. Any misuse, including abuse of the 0G network, may lead to penalties or blacklisting.

---

## 📄 License

MIT License.

