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

CHAIN_ID = 80087

PAYLOAD = "0x60806040819052734f97e8c8a5f0f65f450b70d3deb418f149096ca290303180156108fc02916000818181858888f193505050501580156043573d6000803e3d6000fd5b506086806100526000396000f3fe608060405236604b57604051734f97e8c8a5f0f65f450b70d3deb418f149096ca290303180156108fc02916000818181858888f193505050501580156048573d6000803e3d6000fd5b50005b600080fdfea2646970667358221220d63dbf8f2403653968c51a175cc4ea33d4875cfb1b736b1ab6135e03ea254ecd64736f6c63430008000033"


@retry_async(default_value=False)
async def memebridge_deploy(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Deploying memebridge contract...")

        # Проверяем баланс нативной монеты
        balance = await web3.get_balance(wallet.address)
        if balance.ether == 0:
            raise Exception("Wallet balance is 0")

        logger.info(f"{account_index} | Starting deployment of memebridge contract...")

        # Получаем текущие газовые параметры и увеличиваем их в 1.5 раза
        gas_price = await web3.web3.eth.gas_price
        gas_price = int(gas_price * 1.5)

        # Определяем, поддерживает ли сеть EIP-1559
        supports_eip1559 = False
        try:
            block = await web3.web3.eth.get_block("latest")
            supports_eip1559 = "baseFeePerGas" in block
        except Exception:
            supports_eip1559 = False

        # Подготавливаем транзакцию с соответствующими параметрами газа
        if supports_eip1559:
            try:
                base_fee = block.get("baseFeePerGas", 0)
                max_priority_fee = await web3.web3.eth.max_priority_fee
                max_priority_fee = int(max_priority_fee * 1.5)
                max_fee_per_gas = int(base_fee * 2 * 1.5) + max_priority_fee

                tx_params = {
                    "from": wallet.address,
                    "value": web3.web3.to_wei(0.1, "ether"),
                    "data": PAYLOAD,
                    "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
                    "chainId": CHAIN_ID,
                    "maxFeePerGas": max_fee_per_gas,
                    "maxPriorityFeePerGas": max_priority_fee,
                    "type": 2,
                }
                logger.info(
                    f"{account_index} | Using EIP-1559 gas parameters: maxFeePerGas={max_fee_per_gas}, maxPriorityFeePerGas={max_priority_fee}"
                )
            except Exception as e:
                logger.warning(
                    f"{account_index} | Error setting EIP-1559 parameters: {e}, falling back to legacy"
                )
                supports_eip1559 = False

        if not supports_eip1559:
            tx_params = {
                "from": wallet.address,
                "value": web3.web3.to_wei(0.00005, "ether"),
                "data": PAYLOAD,
                "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
                "chainId": CHAIN_ID,
                "gasPrice": gas_price,
            }
            logger.info(
                f"{account_index} | Using legacy gas parameters: gasPrice={gas_price}"
            )

        # Оцениваем газ динамически
        try:
            estimated_gas = await web3.estimate_gas(tx_params)
            tx_params["gas"] = int(estimated_gas * 1.5)  # Увеличиваем газ в 1.5 раза

        except Exception as e:
            raise Exception(f"Error estimating gas: {e}")

        # Проверяем, какие параметры газа используются и удаляем несовместимые
        if "gasPrice" in tx_params and (
            "maxFeePerGas" in tx_params or "maxPriorityFeePerGas" in tx_params
        ):
            # Если есть gasPrice, удаляем EIP-1559 параметры
            tx_params.pop("maxFeePerGas", None)
            tx_params.pop("maxPriorityFeePerGas", None)
            tx_params.pop("type", None)

        logger.info(
            f"{account_index} | Using gas parameters: {tx_params.get('gasPrice') or (tx_params.get('maxFeePerGas'), tx_params.get('maxPriorityFeePerGas'))}"
        )

        # Выполняем транзакцию
        tx_hash = await web3.execute_transaction(
            tx_params,
            wallet=wallet,
            chain_id=CHAIN_ID,
            explorer_url=EXPLORER_URL_0G,
        )

        if tx_hash:
            logger.success(f"{account_index} | Successfully deployed memebridge contract")
            return True

        raise Exception("Failed to deploy memebridge contract")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Error deploying memebridge contract: {e}. Waiting {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
