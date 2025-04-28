import asyncio
import random
import time
from typing import Optional

from loguru import logger
from src.utils.decorators import retry_async
from src.utils.config import Config
from src.model.onchain.web3_custom import Web3Custom
from eth_account import Account
import primp
from web3 import Web3 as SyncWeb3
from eth_abi import abi

from src.utils.constants import EXPLORER_URL_0G
from src.model.projects.swaps.zero_exchange.constants import (
    TOKENS,
    ERC_20_ABI,
    ROUTER_ADDRESS,
    ROUTER_ABI,
    MAX_UINT256,
)


async def zero_exchange_swaps(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
):
    try:
        logger.info(f"{account_index} | Starting swaps...")

        # Проверяем баланс нативных токенов для газа
        native_balance = await web3.get_balance(wallet.address)
        if native_balance.wei == 0:
            raise Exception("Native token balance is 0")

        # Получаем балансы всех трех токенов
        token_balances = {}
        for symbol, token_data in TOKENS.items():
            balance = await web3.get_token_balance(
                wallet_address=wallet.address,
                token_address=token_data["address"],
                token_abi=ERC_20_ABI,
                decimals=token_data["decimals"],
                symbol=symbol,
            )
            token_balances[symbol] = balance.wei
            logger.info(
                f"{account_index} | {symbol} Balance: {balance.wei / 10**18:.4f}"
            )

        # Проверяем, есть ли токены с балансом
        tokens_with_balance = [
            symbol for symbol, balance in token_balances.items() if balance > 0
        ]

        if not tokens_with_balance:
            raise Exception("No tokens with balance available for swaps")

        # Определяем количество свапов из конфига
        num_swaps = random.randint(
            config.ZERO_EXCHANGE_SWAPS.NUMBER_OF_SWAPS[0],
            config.ZERO_EXCHANGE_SWAPS.NUMBER_OF_SWAPS[1],
        )
        logger.info(f"{account_index} | Will perform {num_swaps} swaps")

        for swap_num in range(num_swaps):
            # Обновляем список токенов с балансом перед каждым свапом
            tokens_with_balance = [
                symbol for symbol, balance in token_balances.items() if balance > 0
            ]

            if not tokens_with_balance:
                logger.warning(
                    f"{account_index} | No more tokens with balance after {swap_num} swaps"
                )
                break

            # Выбираем случайный токен для свапа из тех, где есть баланс
            token_in_symbol = random.choice(tokens_with_balance)
            token_in_balance = token_balances[token_in_symbol]
            token_in_address = TOKENS[token_in_symbol]["address"]

            # Выбираем токен для получения (только USDT если входящий ETH или BTC, иначе ETH или BTC)
            if token_in_symbol == "USDT":
                available_out_tokens = ["ETH", "BTC"]
                token_out_symbol = random.choice(available_out_tokens)
            else:
                # Если входящий токен ETH или BTC, то выходящий только USDT
                token_out_symbol = "USDT"

            token_out_address = TOKENS[token_out_symbol]["address"]

            # Определяем процент баланса для свапа
            swap_percent = random.randint(
                config.ZERO_EXCHANGE_SWAPS.BALANCE_PERCENT_TO_SWAP[0],
                config.ZERO_EXCHANGE_SWAPS.BALANCE_PERCENT_TO_SWAP[1],
            )

            # Рассчитываем сумму для свапа
            amount_to_swap = int(token_in_balance * swap_percent / 100)

            logger.info(
                f"{account_index} | Swap {swap_num + 1}/{num_swaps}: "
                f"Swapping {swap_percent}% of {token_in_symbol} ({amount_to_swap / 10**18:.4f}) -> {token_out_symbol}"
            )

            # Выполняем свап
            await swap_tokens(
                account_index=account_index,
                session=session,
                web3=web3,
                config=config,
                wallet=wallet,
                token_in_address=token_in_address,
                token_out_address=token_out_address,
                amount_in=amount_to_swap,
                min_amount_out=0,
            )

            # Обновляем балансы после свапа
            token_balances[token_in_symbol] -= amount_to_swap
            new_balance = await web3.get_token_balance(
                wallet_address=wallet.address,
                token_address=token_out_address,
                token_abi=ERC_20_ABI,
                decimals=TOKENS[token_out_symbol]["decimals"],
                symbol=token_out_symbol,
            )
            token_balances[token_out_symbol] = new_balance.wei

            if swap_num < num_swaps - 1:
                pause = random.randint(
                    config.SETTINGS.PAUSE_BETWEEN_SWAPS[0],
                    config.SETTINGS.PAUSE_BETWEEN_SWAPS[1],
                )
                logger.info(
                    f"{account_index} | Waiting {pause} seconds before next swap..."
                )
                await asyncio.sleep(pause)

        return True

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Failed to start swaps: {str(e)}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        return False


@retry_async(delay=5.0, backoff=2.0, default_value=False)
async def swap_tokens(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
    token_in_address: str,
    token_out_address: str,
    amount_in: int,
    min_amount_out: int,
):
    try:
        # Определяем символы токенов для логов
        token_in_symbol = next(
            (
                k
                for k, v in TOKENS.items()
                if v["address"].lower() == token_in_address.lower()
            ),
            "Unknown",
        )
        token_out_symbol = next(
            (
                k
                for k, v in TOKENS.items()
                if v["address"].lower() == token_out_address.lower()
            ),
            "Unknown",
        )

        amount_in_readable = amount_in / 10**18
        logger.info(
            f"{account_index} | Swapping {amount_in_readable:.4f} {token_in_symbol} -> {token_out_symbol}"
        )

        # Проверяем баланс
        balance = await web3.get_balance(wallet.address)
        if balance.wei == 0:
            raise Exception("Native token balance is 0")

        # Апрув токена
        router_address = ROUTER_ADDRESS
        chain_id = await web3.web3.eth.chain_id

        # Используем максимальное значение uint256 для неограниченного апрува
        await web3.approve_token(
            token_address=token_in_address,
            spender_address=router_address,
            amount=MAX_UINT256,  # Unlimited approval
            wallet=wallet,
            chain_id=chain_id,
            token_abi=ERC_20_ABI,
            explorer_url=EXPLORER_URL_0G,
        )

        # Параметры свапа
        swap_params = {
            "tokenIn": token_in_address,
            "tokenOut": token_out_address,
            "fee": 3000,  # 0.3%
            "recipient": wallet.address,
            "deadline": int(time.time()) + 1800,  # +30 минут
            "amountIn": amount_in,
            "amountOutMinimum": min_amount_out,
            "sqrtPriceLimitX96": 0,
        }

        # Кодируем функцию и параметры
        function_signature = "exactInputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))"
        function_selector = SyncWeb3.keccak(text=function_signature)[:4]

        encoded_params = abi.encode(
            [
                "address",
                "address",
                "uint24",
                "address",
                "uint256",
                "uint256",
                "uint256",
                "uint160",
            ],
            [
                swap_params["tokenIn"],
                swap_params["tokenOut"],
                swap_params["fee"],
                swap_params["recipient"],
                swap_params["deadline"],
                swap_params["amountIn"],
                swap_params["amountOutMinimum"],
                swap_params["sqrtPriceLimitX96"],
            ],
        )

        encoded_data = function_selector + encoded_params

        # Отправляем транзакцию свапа
        tx_hash = await web3.send_transaction(
            to=router_address,
            data=encoded_data,
            wallet=wallet,
            chain_id=chain_id,
        )

        logger.info(
            f"{account_index} | Swap transaction sent, waiting for confirmation (timeout: {config.SETTINGS.WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS}s)..."
        )
        receipt = await web3.web3.eth.wait_for_transaction_receipt(
            tx_hash,
            timeout=config.SETTINGS.WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS,
        )

        if receipt["status"] == 1:
            logger.success(
                f"{account_index} | Successfully swapped {amount_in_readable:.4f} {token_in_symbol} -> {token_out_symbol}"
            )
            return tx_hash
        else:
            raise Exception("Swap transaction failed")

    except Exception as e:
        random_pause = random.randint(
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
            config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
        )
        logger.error(
            f"{account_index} | Failed to swap tokens: {str(e)}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise
