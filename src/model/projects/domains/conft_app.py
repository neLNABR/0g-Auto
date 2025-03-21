import asyncio
import random
import string

from eth_account import Account
from src.model.help.captcha import NoCaptcha
from src.model.onchain.web3_custom import Web3Custom
from loguru import logger
import primp

from src.utils.decorators import retry_async
from src.utils.config import Config
from src.utils.constants import EXPLORER_URL_0G


# NFT Contract Constants
CONFT_NFT_ADDRESS = "0x9059cA87Ddc891b91e731C57D21809F1A4adC8D9"
CONFT_CHAIN_ID = 16600
CONFT_NFT_ABI = [
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "owner", "type": "address", "internalType": "address"}],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "constant": True,
        "signature": "0x70a08231",
        "stateMutability": "view",
    },
    {
        "name": "mintPrice",
        "type": "function",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "constant": True,
        "signature": "0x6817c76c",
        "stateMutability": "view",
    },
    {
        "name": "mint",
        "type": "function",
        "inputs": [],
        "outputs": [],
        "payable": True,
        "signature": "0x1249c58b",
        "stateMutability": "payable",
    },
]

# Username generation constants
VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"


def generate_username() -> str:
    """Generate a random username with alternating consonants and vowels."""
    length = random.randint(8, 12)
    username = []

    # Randomly decide if we start with vowel or consonant
    start_with_vowel = random.choice([True, False])

    for i in range(length):
        # If position is even, use the starting choice (vowel/consonant)
        # If position is odd, use the opposite
        use_vowel = start_with_vowel if i % 2 == 0 else not start_with_vowel

        if use_vowel:
            username.append(random.choice(VOWELS))
        else:
            username.append(random.choice(CONSONANTS))

    return "".join(username)


async def conft_app(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Starting conft app...")

        balance = await web3.get_balance(wallet.address)
        if balance.ether == 0:
            raise Exception("wallet balance is 0")

        mint_nft_result = await mint_nft(account_index, session, web3, config, wallet)
        if not mint_nft_result:
            raise Exception("Failed to mint NFT")

        mint_domain_result = await mint_domain(
            account_index, session, web3, config, wallet
        )
        if not mint_domain_result:
            raise Exception("Failed to mint domain")

        return True

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Conft app error: {e}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise


@retry_async(default_value=False)
async def mint_nft(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        # Create contract instance
        nft_contract = web3.web3.eth.contract(
            address=web3.web3.to_checksum_address(CONFT_NFT_ADDRESS),
            abi=CONFT_NFT_ABI,
        )

        # Check if user already has NFT
        balance = await nft_contract.functions.balanceOf(wallet.address).call()
        if balance > 0:
            logger.success(f"{account_index} | Already have Conft.app NFT in wallet")
            return True

        # Get mint price
        mint_price = await nft_contract.functions.mintPrice().call()

        # Check if wallet has enough balance
        wallet_balance = await web3.get_balance(wallet.address)
        if wallet_balance.wei < mint_price:
            raise Exception(
                f"Insufficient balance. Need {web3.convert_from_wei(mint_price, 18)} ETH, have {wallet_balance.ether} ETH"
            )

        # Build mint transaction
        gas_params = await web3.get_gas_params()
        if gas_params is None:
            raise Exception("Failed to get gas parameters")

        tx_params = {
            "from": wallet.address,
            "value": mint_price,
            "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
            "chainId": CONFT_CHAIN_ID,
            **gas_params,
        }

        # Set transaction type based on gas params
        if "maxFeePerGas" in gas_params:
            tx_params["type"] = 2

        mint_tx = await nft_contract.functions.mint().build_transaction(tx_params)

        # Execute transaction
        tx_hash = await web3.execute_transaction(
            mint_tx,
            wallet=wallet,
            chain_id=CONFT_CHAIN_ID,
            explorer_url=EXPLORER_URL_0G,
        )

        if tx_hash:
            logger.success(f"{account_index} | Successfully minted NFT")
            return True
        return False

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Mint conft.app nft error: {e}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise


# Domain Contract Constants
DOMAIN_CONTRACT_ADDRESS = "0xCF7f37B4916AC5c530C863f8c8bB26Ec1e8d2Ccb"
DOMAIN_CONTRACT_ABI = [
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "owner", "type": "address", "internalType": "address"}],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "constant": True,
        "signature": "0x70a08231",
        "stateMutability": "view",
    },
]


@retry_async(default_value=False)
async def mint_domain(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        # Create domain contract instance
        domain_contract = web3.web3.eth.contract(
            address=web3.web3.to_checksum_address(DOMAIN_CONTRACT_ADDRESS),
            abi=DOMAIN_CONTRACT_ABI,
        )

        # Check if user already has a domain
        balance = await domain_contract.functions.balanceOf(wallet.address).call()
        if balance > 0:
            logger.success(f"{account_index} | Already have Conft.app domain in wallet")
            return True

        domain_for_mint = generate_username()

        # Encode domain name as bytes
        domain_bytes = domain_for_mint.encode().hex()

        # Construct the payload
        # Function signature (0x692b3956) +
        # Offset to domain name (60) +
        # Duration (1) +
        # Quantity (1) +
        # Length of domain name +
        # Domain name (padded to 32 bytes)

        # Calculate the length of the domain name in bytes
        domain_length = len(domain_for_mint)

        # Construct the payload parts
        function_signature = "0x692b3956"
        offset = "0000000000000000000000000000000000000000000000000000000000000060"
        duration = "0000000000000000000000000000000000000000000000000000000000000001"
        quantity = "0000000000000000000000000000000000000000000000000000000000000001"
        name_length = hex(domain_length)[2:].zfill(64)

        # Pad domain bytes to multiple of 32 bytes
        padded_domain = domain_bytes + "0" * (64 - len(domain_bytes))

        # Combine all parts
        data = (
            function_signature
            + offset
            + duration
            + quantity
            + name_length
            + padded_domain
        )

        # Build transaction
        gas_params = await web3.get_gas_params()
        if gas_params is None:
            raise Exception("Failed to get gas parameters")

        tx_params = {
            "from": wallet.address,
            "to": web3.web3.to_checksum_address(DOMAIN_CONTRACT_ADDRESS),
            "value": 0,  # Free mint
            "nonce": await web3.web3.eth.get_transaction_count(wallet.address),
            "chainId": CONFT_CHAIN_ID,
            "data": data,
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
            raise Exception(f"Failed to estimate gas: {e}")

        # Execute transaction
        tx_hash = await web3.execute_transaction(
            tx_params,
            wallet=wallet,
            chain_id=CONFT_CHAIN_ID,
            explorer_url=EXPLORER_URL_0G,
        )

        if tx_hash:
            logger.success(
                f"{account_index} | Successfully minted domain {domain_for_mint}"
            )
            return True
        return False

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Mint conft.app domain error: {e}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
