from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
import yaml
from pathlib import Path
import asyncio


@dataclass
class SettingsConfig:
    THREADS: int
    ATTEMPTS: int
    ACCOUNTS_RANGE: Tuple[int, int]
    EXACT_ACCOUNTS_TO_USE: List[int]
    PAUSE_BETWEEN_ATTEMPTS: Tuple[int, int]
    PAUSE_BETWEEN_SWAPS: Tuple[int, int]
    RANDOM_PAUSE_BETWEEN_ACCOUNTS: Tuple[int, int]
    RANDOM_PAUSE_BETWEEN_ACTIONS: Tuple[int, int]
    RANDOM_INITIALIZATION_PAUSE: Tuple[int, int]
    TELEGRAM_USERS_IDS: List[int]
    TELEGRAM_BOT_TOKEN: str
    SEND_TELEGRAM_LOGS: bool
    SHUFFLE_WALLETS: bool
    WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS: int


@dataclass
class FlowConfig:
    TASKS: List
    SKIP_FAILED_TASKS: bool


@dataclass
class ZeroExchangeSwapsConfig:
    BALANCE_PERCENT_TO_SWAP: Tuple[int, int]
    NUMBER_OF_SWAPS: Tuple[int, int]


@dataclass
class CaptchaConfig:
    SOLVIUM_API_KEY: str
    NOCAPTCHA_API_KEY: str
    USE_NOCAPTCHA: bool

@dataclass
class RpcsConfig:
    ZEROG: List[str]


@dataclass
class PuzzlemaniaConfig:
    USE_REFERRAL_CODE: bool
    INVITES_PER_REFERRAL_CODE: Tuple[int, int]
    COLLECT_REFERRAL_CODE: bool

@dataclass
class OthersConfig:
    SKIP_SSL_VERIFICATION: bool
    USE_PROXY_FOR_RPC: bool


@dataclass
class WalletInfo:
    account_index: int
    private_key: str
    address: str
    balance: float
    transactions: int


@dataclass
class WalletsConfig:
    wallets: List[WalletInfo] = field(default_factory=list)

@dataclass
class CrustySwapConfig:
    NETWORKS_TO_REFUEL_FROM: List[str]
    AMOUNT_TO_REFUEL: Tuple[float, float]
    MINIMUM_BALANCE_TO_REFUEL: float
    WAIT_FOR_FUNDS_TO_ARRIVE: bool
    MAX_WAIT_TIME: int
    BRIDGE_ALL: bool
    BRIDGE_ALL_MAX_AMOUNT: float


@dataclass
class WithdrawalConfig:
    currency: str
    networks: List[str]
    min_amount: float
    max_amount: float
    wait_for_funds: bool
    max_wait_time: int
    retries: int
    max_balance: float  # Maximum wallet balance to allow withdrawal to


@dataclass
class ExchangesConfig:
    name: str  # Exchange name (OKX, BINANCE, BYBIT)
    apiKey: str
    secretKey: str
    passphrase: str  # Only needed for OKX
    withdrawals: List[WithdrawalConfig]


@dataclass
class Config:
    SETTINGS: SettingsConfig
    FLOW: FlowConfig
    ZERO_EXCHANGE_SWAPS: ZeroExchangeSwapsConfig
    CAPTCHA: CaptchaConfig
    RPCS: RpcsConfig
    OTHERS: OthersConfig
    PUZZLEMANIA: PuzzlemaniaConfig
    CRUSTY_SWAP: CrustySwapConfig
    EXCHANGES: ExchangesConfig
    WALLETS: WalletsConfig = field(default_factory=WalletsConfig)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    spare_twitter_tokens: List[str] = field(default_factory=list)
    
    @classmethod
    def load(cls, path: str = "config.yaml") -> "Config":
        """Load configuration from yaml file"""
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # Load tasks from tasks.py
        try:
            import tasks

            if hasattr(tasks, "TASKS"):
                tasks_list = tasks.TASKS
            else:
                error_msg = "No TASKS list found in tasks.py"
                print(f"Error: {error_msg}")
                raise ValueError(error_msg)
        except ImportError as e:
            error_msg = f"Could not import tasks.py: {e}"
            print(f"Error: {error_msg}")
            raise ImportError(error_msg) from e

        return cls(
            SETTINGS=SettingsConfig(
                THREADS=data["SETTINGS"]["THREADS"],
                ATTEMPTS=data["SETTINGS"]["ATTEMPTS"],
                ACCOUNTS_RANGE=tuple(data["SETTINGS"]["ACCOUNTS_RANGE"]),
                EXACT_ACCOUNTS_TO_USE=data["SETTINGS"]["EXACT_ACCOUNTS_TO_USE"],
                PAUSE_BETWEEN_ATTEMPTS=tuple(
                    data["SETTINGS"]["PAUSE_BETWEEN_ATTEMPTS"]
                ),
                PAUSE_BETWEEN_SWAPS=tuple(data["SETTINGS"]["PAUSE_BETWEEN_SWAPS"]),
                RANDOM_PAUSE_BETWEEN_ACCOUNTS=tuple(
                    data["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACCOUNTS"]
                ),
                RANDOM_PAUSE_BETWEEN_ACTIONS=tuple(
                    data["SETTINGS"]["RANDOM_PAUSE_BETWEEN_ACTIONS"]
                ),
                RANDOM_INITIALIZATION_PAUSE=tuple(
                    data["SETTINGS"]["RANDOM_INITIALIZATION_PAUSE"]
                ),
                TELEGRAM_USERS_IDS=data["SETTINGS"]["TELEGRAM_USERS_IDS"],
                TELEGRAM_BOT_TOKEN=data["SETTINGS"]["TELEGRAM_BOT_TOKEN"],
                SEND_TELEGRAM_LOGS=data["SETTINGS"]["SEND_TELEGRAM_LOGS"],
                SHUFFLE_WALLETS=data["SETTINGS"].get("SHUFFLE_WALLETS", True),
                WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS=data["SETTINGS"].get(
                    "WAIT_FOR_TRANSACTION_CONFIRMATION_IN_SECONDS", 120
                ),
            ),
            FLOW=FlowConfig(
                TASKS=tasks_list,
                SKIP_FAILED_TASKS=data["FLOW"]["SKIP_FAILED_TASKS"],
            ),
            ZERO_EXCHANGE_SWAPS=ZeroExchangeSwapsConfig(
                BALANCE_PERCENT_TO_SWAP=tuple(
                    data["ZERO_EXCHANGE_SWAPS"]["BALANCE_PERCENT_TO_SWAP"]
                ),
                NUMBER_OF_SWAPS=tuple(data["ZERO_EXCHANGE_SWAPS"]["NUMBER_OF_SWAPS"]),
            ),
            CAPTCHA=CaptchaConfig(
                SOLVIUM_API_KEY=data["CAPTCHA"]["SOLVIUM_API_KEY"],
                NOCAPTCHA_API_KEY=data["CAPTCHA"]["NOCAPTCHA_API_KEY"],
                USE_NOCAPTCHA=data["CAPTCHA"]["USE_NOCAPTCHA"],
            ),
            RPCS=RpcsConfig(
                ZEROG=data["RPCS"]["ZEROG"],
            ),
            OTHERS=OthersConfig(
                SKIP_SSL_VERIFICATION=data["OTHERS"]["SKIP_SSL_VERIFICATION"],
                USE_PROXY_FOR_RPC=data["OTHERS"]["USE_PROXY_FOR_RPC"],
            ),
            PUZZLEMANIA=PuzzlemaniaConfig(
                USE_REFERRAL_CODE=data["PUZZLEMANIA"]["USE_REFERRAL_CODE"],
                INVITES_PER_REFERRAL_CODE=tuple(
                    data["PUZZLEMANIA"]["INVITES_PER_REFERRAL_CODE"]
                ),
                COLLECT_REFERRAL_CODE=data["PUZZLEMANIA"]["COLLECT_REFERRAL_CODE"],
            ),
            EXCHANGES=ExchangesConfig(
                name=data["EXCHANGES"]["name"],
                apiKey=data["EXCHANGES"]["apiKey"],
                secretKey=data["EXCHANGES"]["secretKey"],
                passphrase=data["EXCHANGES"]["passphrase"],
                withdrawals=[
                    WithdrawalConfig(
                        currency=w["currency"],
                        networks=w["networks"],
                        min_amount=w["min_amount"],
                        max_amount=w["max_amount"],
                        wait_for_funds=w["wait_for_funds"],
                        max_wait_time=w["max_wait_time"],
                        retries=w["retries"],
                        max_balance=w["max_balance"],
                    )
                    for w in data["EXCHANGES"]["withdrawals"]
                ],
            ),
            CRUSTY_SWAP=CrustySwapConfig(
                NETWORKS_TO_REFUEL_FROM=data["CRUSTY_SWAP"]["NETWORKS_TO_REFUEL_FROM"],
                AMOUNT_TO_REFUEL=tuple(data["CRUSTY_SWAP"]["AMOUNT_TO_REFUEL"]),
                MINIMUM_BALANCE_TO_REFUEL=data["CRUSTY_SWAP"][
                    "MINIMUM_BALANCE_TO_REFUEL"
                ],
                WAIT_FOR_FUNDS_TO_ARRIVE=data["CRUSTY_SWAP"][
                    "WAIT_FOR_FUNDS_TO_ARRIVE"
                ],
                MAX_WAIT_TIME=data["CRUSTY_SWAP"]["MAX_WAIT_TIME"],
                BRIDGE_ALL=data["CRUSTY_SWAP"]["BRIDGE_ALL"],
                BRIDGE_ALL_MAX_AMOUNT=data["CRUSTY_SWAP"]["BRIDGE_ALL_MAX_AMOUNT"],
            ),
        )


# Singleton pattern
def get_config() -> Config:
    """Get configuration singleton"""
    if not hasattr(get_config, "_config"):
        get_config._config = Config.load()
    return get_config._config
