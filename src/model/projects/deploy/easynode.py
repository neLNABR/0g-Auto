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

CHAIN_ID = 16601

PAYLOAD = "0x608060405260405161052438038061052483398181016040528101906100259190610188565b60003411610068576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161005f90610212565b60405180910390fd5b600034111561011f5760008173ffffffffffffffffffffffffffffffffffffffff163460405161009790610263565b60006040518083038185875af1925050503d80600081146100d4576040519150601f19603f3d011682016040523d82523d6000602084013e6100d9565b606091505b505090508061011d576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610114906102c4565b60405180910390fd5b505b506102e4565b600080fd5b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006101558261012a565b9050919050565b6101658161014a565b811461017057600080fd5b50565b6000815190506101828161015c565b92915050565b60006020828403121561019e5761019d610125565b5b60006101ac84828501610173565b91505092915050565b600082825260208201905092915050565b7f4465706c6f796d656e7420726571756972657320612066656500000000000000600082015250565b60006101fc6019836101b5565b9150610207826101c6565b602082019050919050565b6000602082019050818103600083015261022b816101ef565b9050919050565b600081905092915050565b50565b600061024d600083610232565b91506102588261023d565b600082019050919050565b600061026e82610240565b9150819050919050565b7f466565207472616e73666572206661696c656400000000000000000000000000600082015250565b60006102ae6013836101b5565b91506102b982610278565b602082019050919050565b600060208201905081810360008301526102dd816102a1565b9050919050565b610231806102f36000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80632baeceb714610046578063a87d942c14610050578063d09de08a1461006e575b600080fd5b61004e610078565b005b6100586100ca565b604051610065919061013e565b60405180910390f35b6100766100d3565b005b60008081548092919061008a90610188565b91905055507f1a00a27c962d5410357331e1a8cffff62058bd0161ad624818df31152f1eeb456000546040516100c0919061013e565b60405180910390a1565b60008054905090565b6000808154809291906100e5906101b2565b91905055507f3cf8b50771c17d723f2cb711ca7dadde485b222e13c84ba0730a14093fad6d5c60005460405161011b919061013e565b60405180910390a1565b6000819050919050565b61013881610125565b82525050565b6000602082019050610153600083018461012f565b92915050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600061019382610125565b915060008214156101a7576101a6610159565b5b600182039050919050565b60006101bd82610125565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8214156101f0576101ef610159565b5b60018201905091905056fea2646970667358221220526250c31d8148ffcfa6d06ab24c6dfbf02441f204c5578890519ec2fdd071c564736f6c63430008090033000000000000000000000000fda77b68d08988e91932a3a4ff4d49d4771536f8"


@retry_async(default_value=False)
async def easynode_deploy(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Deploying easynode contract...")

        # Проверяем баланс нативной монеты
        balance = await web3.get_balance(wallet.address)
        if balance.ether == 0:
            raise Exception("Wallet balance is 0")

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
                    "value": web3.web3.to_wei(0.05, "ether"),
                    "data": PAYLOAD,
                    "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
                    "chainId": CHAIN_ID,
                    "maxFeePerGas": max_fee_per_gas,
                    "maxPriorityFeePerGas": max_priority_fee,
                    "type": "0x2",
                }

            except Exception as e:
                logger.warning(
                    f"{account_index} | Error setting EIP-1559 parameters: {e}, falling back to legacy"
                )
                supports_eip1559 = False

        if not supports_eip1559:
            tx_params = {
                "from": wallet.address,
                "value": web3.web3.to_wei(0.1, "ether"),
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

        # Выполняем транзакцию
        tx_hash = await web3.execute_transaction(
            tx_params,
            wallet=wallet,
            chain_id=CHAIN_ID,
            explorer_url=EXPLORER_URL_0G,
        )

        if tx_hash:
            logger.success(f"{account_index} | Successfully deployed easynode contract")
            return True

        raise Exception("Failed to deploy easynode contract")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Error deploying easynode contract: {e}. Waiting {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
