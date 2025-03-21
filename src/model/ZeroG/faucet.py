import asyncio
import random
from loguru import logger
from eth_account import Account
from src.model.help.captcha import NoCaptcha
from src.model.onchain.web3_custom import Web3Custom
import primp

from src.utils.decorators import retry_async
from src.utils.config import Config
from src.utils.constants import EXPLORER_URL_0G

# Token Contract Constants
FAUCET_CONTRACTS = {
    "USDT": "0x9A87C2412d500343c073E5Ae5394E3bE3874F76b",
    "ETH": "0xce830D0905e0f7A9b300401729761579c5FB6bd6",
    "BTC": "0x1E0D871472973c562650E991ED8006549F8CBEfc",
}

CHAIN_ID = 16600
MINT_ABI = [
    {
        "name": "mint",
        "type": "function",
        "inputs": [],
        "outputs": [],
        "payable": True,
        "signature": "0x1249c58b",
        "stateMutability": "payable",
    }
]


@retry_async(default_value=False)
async def faucet(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Starting faucet...")

        nocaptcha_client = NoCaptcha(config.CAPTCHA.NOCAPTCHA_API_KEY, session=session)
        result = await nocaptcha_client.solve_hcaptcha(
            sitekey="1230eb62-f50c-4da4-a736-da5c3c342e8e",
            referer="https://hub.0g.ai",
            invisible=False,
        )

        if result is None:
            raise Exception("Captcha not solved")

        captcha_token = result["generated_pass_UUID"]
        logger.success(f"{account_index} | Captcha solved for faucet")

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,zh-TW;q=0.6,zh;q=0.5",
            "content-type": "application/json",
            "origin": "https://hub.0g.ai",
            "priority": "u=1, i",
            "referer": "https://hub.0g.ai/",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        json_data = {
            "address": wallet.address,
            "hcaptchaToken": captcha_token,
            "token": "A0GI",
        }

        response = await session.post(
            "https://992dkn4ph6.execute-api.us-west-1.amazonaws.com/",
            headers=headers,
            json=json_data,
        )

        if "Service is busy. Please retry later." in response.text:
            random_pause = random.randint(
                config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
                config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
            )
            raise Exception(f"Faucet is busy. Please retry later.")

        if "Please wait 24 hours before requesting again" in response.text:
            logger.success(
                f"{account_index} | Faucet already requested today. Wait 24 hours before requesting again."
            )
            return True

        if "Invalid Captcha" in response.text:
            raise Exception("Invalid Captcha")

        if response.status_code == 200:
            logger.success(f"{account_index} | Faucet requested successfully")
            return True

        raise Exception(f"Unknown error: {response.status_code} | {response.text}")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        if "hours before requesting again" in str(e):
            logger.success(
                f"{account_index} | Faucet already requested today. Wait some time before requesting again."
            )
            return True
        logger.error(
            f"{account_index} | Faucet error: {e}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise


@retry_async(default_value=False)
async def mint_token(
    account_index: int,
    web3: Web3Custom,
    wallet: Account,
    token_name: str,
    contract_address: str,
    config: Config,
) -> bool:
    """Mint tokens from faucet"""
    try:
        contract = web3.web3.eth.contract(
            address=web3.web3.to_checksum_address(contract_address), abi=MINT_ABI
        )

        # Build mint transaction
        gas_params = await web3.get_gas_params()
        if gas_params is None:
            raise Exception("Failed to get gas parameters")

        # Set optimal gas price if not set
        if "gasPrice" not in gas_params and "maxFeePerGas" not in gas_params:
            gas_params["gasPrice"] = web3.web3.to_wei(0.00000002, "ether")

        tx_params = {
            "from": wallet.address,
            "value": 0,
            "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
            "chainId": CHAIN_ID,
            **gas_params,
        }

        # Set transaction type based on gas params
        if "maxFeePerGas" in gas_params:
            tx_params["type"] = 2

        mint_tx = await contract.functions.mint().build_transaction(tx_params)

        # Try to estimate gas
        try:
            estimated_gas = await web3.estimate_gas(mint_tx)
            mint_tx["gas"] = estimated_gas
        except Exception as e:
            raise Exception(f"Error estimating gas: {e}")

        # Execute transaction
        tx_hash = await web3.execute_transaction(
            mint_tx,
            wallet=wallet,
            chain_id=CHAIN_ID,
            explorer_url=EXPLORER_URL_0G,
        )

        if tx_hash:
            logger.success(f"{account_index} | Successfully faucet {token_name}")
            return True

        raise Exception("Failed to mint token")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Failed to faucet {token_name}: {str(e)}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise


async def faucet_tokens(
    account_index: int,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    """Mint all available tokens from faucets"""
    try:
        success_minted = 0
        logger.info(f"{account_index} | Starting tokens faucet...")

        balance = await web3.get_balance(wallet.address)
        if balance.ether < 0.00000001:
            logger.error(
                f"{account_index} | Insufficient A0GI balance. Start 'faucet' task first."
            )
            return False

        for token_name in FAUCET_CONTRACTS.keys():
            try:
                success = await mint_token(
                    account_index,
                    web3,
                    wallet,
                    token_name,
                    FAUCET_CONTRACTS[token_name],
                    config,
                )
                if success:
                    success_minted += 1
                    logger.success(
                        f"{account_index} | Successfully minted {token_name}"
                    )
                else:
                    logger.error(f"{account_index} | Failed to mint {token_name}")
            except Exception as e:
                # Продолжаем с другими токенами даже если этот не удался
                logger.error(f"{account_index} | Error minting {token_name}: {str(e)}")
                continue
            finally:
                # Add delay between mints regardless of success
                random_pause = random.randint(
                    config.SETTINGS.PAUSE_BETWEEN_SWAPS[0],
                    config.SETTINGS.PAUSE_BETWEEN_SWAPS[1],
                )
                logger.info(
                    f"{account_index} | Sleeping {random_pause} seconds after attempting {token_name}..."
                )
                await asyncio.sleep(random_pause)

        if success_minted >= 1:
            logger.success(
                f"{account_index} | Successfully minted {success_minted} out of {len(FAUCET_CONTRACTS)} tokens"
            )
            return True
        else:
            logger.error(f"{account_index} | Failed to mint any tokens.")
            return False

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Faucet tokens error: {e}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
