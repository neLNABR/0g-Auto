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


@retry_async(default_value=False)
async def deploy_storage_scan(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Starting deploying storage scan...")

        balance = await web3.get_balance(wallet.address)
        if balance.ether == 0:
            raise Exception("wallet balance is 0")

        # Generate random bytes directly (32 bytes)
        content_hash = bytes([random.randint(0, 255) for _ in range(32)])

        # Construct the payload exactly as in successful transaction
        data = (
            # Function signature
            "0xef3e12dc"
            +
            # Offset to data structure (32)
            "0000000000000000000000000000000000000000000000000000000000000020"
            +
            # Length (20)
            "0000000000000000000000000000000000000000000000000000000000000014"
            +
            # Offset to bytes (96)
            "0000000000000000000000000000000000000000000000000000000000000060"
            +
            # Offset to array (128)
            "0000000000000000000000000000000000000000000000000000000000000080"
            +
            # Empty bytes
            "0000000000000000000000000000000000000000000000000000000000000000"
            +
            # Array length (1)
            "0000000000000000000000000000000000000000000000000000000000000001"
            +
            # Hash value
            content_hash.hex()
            +
            # Final value (0)
            "0000000000000000000000000000000000000000000000000000000000000000"
        )

        # Get gas parameters
        gas_params = await web3.get_gas_params()
        if gas_params is None:
            raise Exception("Failed to get gas parameters")

        # Set optimal gas price if not set
        if "gasPrice" not in gas_params and "maxFeePerGas" not in gas_params:
            gas_params["gasPrice"] = web3.web3.to_wei(0.00000002, "ether")

        # Generate random value between 0.000005 and 0.00001 ETH
        random_value = random.uniform(0.000005, 0.00001)

        # Prepare transaction
        tx_params = {
            "from": wallet.address,
            "to": web3.web3.to_checksum_address(STORAGE_SCAN_CONTRACT),
            "value": web3.web3.to_wei(random_value, "ether"),
            "data": data,
            "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
            "chainId": CHAIN_ID,
            **gas_params,
        }

        # Set transaction type based on gas params
        if "maxFeePerGas" in gas_params:
            tx_params["type"] = 2

        # Try to estimate gas
        try:
            estimated_gas = await web3.estimate_gas(tx_params)
            tx_params["gas"] = estimated_gas
        except Exception as e:
            raise Exception(f"Error estimating gas: {e}")

        # Execute transaction
        tx_hash = await web3.execute_transaction(
            tx_params,
            wallet=wallet,
            chain_id=CHAIN_ID,
            explorer_url=EXPLORER_URL_0G,
        )

        if tx_hash:
            logger.success(f"{account_index} | Successfully deployed storage scan")
            return True

        raise Exception("Failed to deploy storage scan")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Storage scan deploy error: {e}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
