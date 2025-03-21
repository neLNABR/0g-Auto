import asyncio
import random
import hashlib
import time
import os

from eth_account import Account
from src.model.help.captcha import NoCaptcha
from src.model.onchain.web3_custom import Web3Custom
from loguru import logger
import primp

from src.utils.decorators import retry_async
from src.utils.config import Config
from src.utils.constants import EXPLORER_URL_0G

STORAGE_SCAN_CONTRACT = "0x0460aA47b41a66694c0a73f667a1b795A5ED3556"
CHAIN_ID = 16600

PANDA_0G_CONTRACT = "0x8260aBAd9079FE6B50fD9248D5996f810Fe01ceF"

# Минимальный ABI для проверки баланса NFT
NFT_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    }
]


@retry_async(default_value=False)
async def mintaura_panda(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Checking balance of Panda 0G NFT...")

        # Проверяем баланс NFT на кошельке
        nft_contract = web3.web3.eth.contract(
            address=web3.web3.to_checksum_address(PANDA_0G_CONTRACT), abi=NFT_ABI
        )

        nft_balance = await nft_contract.functions.balanceOf(wallet.address).call()

        if nft_balance > 0:
            logger.success(
                f"{account_index} | Wallet already has {nft_balance} Panda 0G NFT"
            )
            return True

        # Проверяем баланс нативной монеты
        balance = await web3.get_balance(wallet.address)
        if balance.ether == 0:
            raise Exception("Wallet balance is 0")

        logger.info(f"{account_index} | Starting mint of Panda 0G NFT...")

        # Данные для вызова функции mint на основе транзакций из примера
        data = (
            # Сигнатура функции mint
            "0x84bb1e42"
            # Адрес получателя (64 символа с паддингом)
            + wallet.address[2:].lower().zfill(64)
            # Количество NFT для минта (1)
            + "0000000000000000000000000000000000000000000000000000000000000001"
            # Адрес токена оплаты (EEEE... означает нативную монету)
            + "000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
            # Сумма оплаты (0)
            + "0000000000000000000000000000000000000000000000000000000000000000"
            # Смещение для данных (192 = 0xc0)
            + "00000000000000000000000000000000000000000000000000000000000000c0"
            # Смещение для дополнительных данных (384 = 0x180)
            + "0000000000000000000000000000000000000000000000000000000000000180"
            # Длина данных (128 = 0x80)
            + "0000000000000000000000000000000000000000000000000000000000000080"
            # Значение -1 (все F)
            + "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
            # Дополнительное значение (0)
            + "0000000000000000000000000000000000000000000000000000000000000000"
            # Адрес токена оплаты (повторно)
            + "000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
            # Значение 1
            + "0000000000000000000000000000000000000000000000000000000000000001"
            # Значение 0
            + "0000000000000000000000000000000000000000000000000000000000000000"
            # Значение 0
            + "0000000000000000000000000000000000000000000000000000000000000000"
        )

        # Получаем параметры газа
        gas_params = await web3.get_gas_params()
        if gas_params is None:
            raise Exception("Failed to get gas parameters")

        # Подготавливаем транзакцию
        tx_params = {
            "from": wallet.address,
            "to": web3.web3.to_checksum_address(PANDA_0G_CONTRACT),
            "value": 0,  # Минт бесплатный
            "data": data,
            "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
            "chainId": CHAIN_ID,
            **gas_params,
        }

        # Устанавливаем тип транзакции в зависимости от параметров газа
        if "maxFeePerGas" in gas_params:
            tx_params["type"] = 2

        # Оцениваем газ динамически
        try:
            estimated_gas = await web3.estimate_gas(tx_params)
            tx_params["gas"] = estimated_gas

        except Exception as e:
            raise Exception(f"Error estimating gas: {e}")

        # Выполняем транзакцию
        tx_hash = await web3.execute_transaction(
            tx_params,
            wallet=wallet,
            chain_id=CHAIN_ID,
            explorer_url=EXPLORER_URL_0G,
        )

        if tx_hash:
            logger.success(f"{account_index} | Successfully minted Panda 0G NFT")
            return True

        raise Exception("Failed to mint Panda 0G NFT")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Error minting Panda 0G NFT: {e}. Waiting {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
