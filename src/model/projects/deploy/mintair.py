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

# The contract payload from the example transaction
PAYLOAD_TIMER_CONTRACT = "0x6080604052348015600f57600080fd5b5061018d8061001f6000396000f3fe608060405234801561001057600080fd5b50600436106100365760003560e01c8063557ed1ba1461003b578063d09de08a14610059575b600080fd5b610043610063565b60405161005091906100d9565b60405180910390f35b61006161006c565b005b60008054905090565b600160008082825461007e9190610123565b925050819055507f3912982a97a34e42bab8ea0e99df061a563ce1fe3333c5e14386fd4c940ef6bc6000546040516100b691906100d9565b60405180910390a1565b6000819050919050565b6100d3816100c0565b82525050565b60006020820190506100ee60008301846100ca565b92915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600061012e826100c0565b9150610139836100c0565b9250828201905080821115610151576101506100f4565b5b9291505056fea2646970667358221220801aef4e99d827a7630c9f3ce9c8c00d708b58053b756fed98cd9f2f5928d10f64736f6c634300081c0033"


@retry_async(default_value=False)
async def mintair_deploy(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Deploying timer contract...")

        # Проверяем баланс нативной монеты
        balance = await web3.get_balance(wallet.address)
        if balance.ether == 0:
            raise Exception("Wallet balance is 0")

        logger.info(f"{account_index} | Starting deployment of timer contract...")

        # Получаем параметры газа
        gas_params = await web3.get_gas_params()
        if gas_params is None:
            raise Exception("Failed to get gas parameters")

        # Подготавливаем транзакцию для деплоя контракта
        tx_params = {
            "from": wallet.address,
            "value": 0,
            "data": PAYLOAD_TIMER_CONTRACT,
            "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
            "chainId": CHAIN_ID,
            **gas_params,
        }

        # Устанавливаем тип транзакции в зависимости от параметров газа
        if "maxFeePerGas" in gas_params:
            tx_params["type"] = "0x2"  # Use hex string format

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
            logger.success(f"{account_index} | Successfully deployed timer contract")
            return True

        raise Exception("Failed to deploy timer contract")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Error deploying timer contract: {e}. Waiting {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
