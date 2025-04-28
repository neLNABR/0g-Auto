import asyncio
import random
from loguru import logger
from eth_account import Account
from src.model.help.captcha import NoCaptcha, Solvium
from src.model.onchain.web3_custom import Web3Custom
import primp
from http.cookies import SimpleCookie

from src.utils.decorators import retry_async
from src.utils.config import Config
from src.utils.constants import EXPLORER_URL_0G
from src.utils.client import (
    create_client,
    create_twitter_client,
)

# Token Contract Constants
FAUCET_CONTRACTS = {
    "USDT": "0xA8F030218d7c26869CADd46C5F10129E635cD565",
    "ETH": "0x2619090fcfDB99a8CCF51c76C9467F7375040eeb",
    "BTC": "0x6dc29491a8396Bd52376b4f6dA1f3E889C16cA85",
}

CHAIN_ID = 80087
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


async def faucets(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
    proxy: str,
    twitter_token: str,
):
    try:
        logger.info(f"{account_index} | Starting faucets...")

        success_default, success_mictonode = False, False

        oauth_token, oauth_verifier = await _connect_twitter(
            account_index, session, web3, config, wallet, proxy, twitter_token
        )

        if not oauth_token or not oauth_verifier:
            logger.error(f"{account_index} | Failed to connect to Twitter.")
            raise Exception("Failed to connect to Twitter.")

        logger.success(f"{account_index} | Twitter connected successfully")

        success_default = await default_faucet(
            account_index,
            session,
            web3,
            config,
            wallet,
            proxy,
            oauth_token,
            oauth_verifier,
        )

        # success_mictonode = await mictonode_faucet(
        #     account_index,
        #     session,
        #     web3,
        #     config,
        #     wallet,
        #     proxy,
        # )

        if success_default or success_mictonode:
            logger.success(f"{account_index} | Successfully completed faucets")
            return True
        else:
            logger.warning(f"{account_index} | All faucets failed")
            return False

    except Exception as e:
        logger.error(f"{account_index} | Faucets error: {e}")
        return False


@retry_async(default_value=False)
async def _connect_twitter(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
    proxy: str,
    twitter_token: str,
) -> tuple[str, str]:
    try:
        headers = {
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "accept": "*/*",
            "origin": "https://faucet.0g.ai",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://faucet.0g.ai/",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4",
            "priority": "u=1, i",
        }

        response = await session.post(
            "https://faucet.0g.ai/api/request-token", headers=headers
        )

        oauth_token = response.json()["url"].split("oauth_token=")[1].strip()

        twitter_client = await create_twitter_client(proxy, twitter_token)

        headers = {
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": "https://faucet.0g.ai/",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4",
            "priority": "u=0, i",
        }

        params = {
            "oauth_token": oauth_token,
        }

        response = await twitter_client.get(
            "https://api.x.com/oauth/authenticate", params=params, headers=headers
        )

        if "Could not authenticate you" in response.text:
            logger.error(
                f"{account_index} | Twitter token is invalid. Please check your twitter token!"
            )
            async with config.lock:
                if (
                    not config.spare_twitter_tokens
                    or len(config.spare_twitter_tokens) == 0
                ):
                    raise Exception(
                        "Twitter token is invalid and no spare tokens available. Please check your twitter token!"
                    )

                # Get a new token from the spare tokens list
                new_token = config.spare_twitter_tokens.pop(0)
                old_token = twitter_token
                twitter_token = new_token

                # Update the token in the file
                try:
                    with open("data/twitter_tokens.txt", "r", encoding="utf-8") as f:
                        tokens = f.readlines()

                    # Process tokens to replace old with new and remove duplicates
                    processed_tokens = []
                    replaced = False

                    for token in tokens:
                        stripped_token = token.strip()

                        # Skip if it's a duplicate of the new token
                        if stripped_token == new_token:
                            continue

                        # Replace old token with new token
                        if stripped_token == old_token:
                            if not replaced:
                                processed_tokens.append(f"{new_token}\n")
                                replaced = True
                        else:
                            processed_tokens.append(token)

                    # If we didn't replace anything (old token not found), add new token
                    if not replaced:
                        processed_tokens.append(f"{new_token}\n")

                    with open("data/twitter_tokens.txt", "w", encoding="utf-8") as f:
                        f.writelines(processed_tokens)

                    logger.info(
                        f"{account_index} | Replaced invalid Twitter token with a new one"
                    )

                    # Retry the connection with the new token
                    raise Exception("Trying again with a new token...")
                except Exception as file_err:
                    logger.error(
                        f"{account_index} | Failed to update token in file: {file_err}"
                    )
                    raise

        if 'name="authenticity_token" value="' in response.text:
            authenticity_token = response.text.split(
                'name="authenticity_token" value="'
            )[1].split('"')[0]
        else:
            authenticity_token = response.text.split(
                'name="authenticity_token" type="hidden" value="'
            )[1].split('"')[0]

        headers = {
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "origin": "https://api.x.com",
            "content-type": "application/x-www-form-urlencoded",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": "https://api.x.com/",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4",
            "priority": "u=0, i",
        }

        data = {
            "authenticity_token": authenticity_token,
            "oauth_token": oauth_token,
        }

        response = await twitter_client.post(
            "https://x.com/oauth/authorize", headers=headers, data=data
        )

        oauth_verifier = response.text.split("oauth_verifier=")[1].split('"')[0]

        # headers = {
        #     'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'upgrade-insecure-requests': '1',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #     'sec-fetch-site': 'cross-site',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-dest': 'document',
        #     'referer': 'https://x.com/',
        #     'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4',
        #     'priority': 'u=0, i',
        # }

        # params = {
        #     'oauth_token': oauth_token,
        #     'oauth_verifier': oauth_verifier,
        # }

        # response = await session.get('https://faucet.0g.ai/api/x-callback', params=params, headers=headers)

        headers = {
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "navigate",
            "sec-fetch-dest": "document",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "referer": "https://x.com/",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4",
            "priority": "u=0, i",
        }

        params = {
            "oauth_token": oauth_token,
            "oauth_verifier": oauth_verifier,
        }

        response = await session.get(
            "https://faucet.0g.ai/", params=params, headers=headers
        )

        return oauth_token, oauth_verifier

    except Exception as e:
        logger.error(f"{account_index} | Connect faucet twitter error: {e}")
        raise e


@retry_async(default_value=False)
async def default_faucet(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
    proxy: str,
    oauth_token: str,
    oauth_verifier: str,
):
    try:
        logger.info(f"{account_index} | Starting faucet...")

        if not oauth_token or not oauth_verifier:
            logger.error(f"{account_index} | Failed to connect to Twitter.")
            raise Exception("Failed to connect to Twitter.")

        if config.CAPTCHA.USE_NOCAPTCHA:
            logger.info(
                f"[{account_index}] | Solving hCaptcha challenge with NoCaptcha..."
            )
            nocaptcha_client = NoCaptcha(
                config.CAPTCHA.NOCAPTCHA_API_KEY, session=session
            )
            result = await nocaptcha_client.solve_hcaptcha(
                sitekey="914e63b4-ac20-4c24-bc92-cdb6950ccfde",
                referer="https://faucet.0g.ai/",
                invisible=False,
            )
            captcha_token = result["generated_pass_UUID"]

        else:
            logger.info(
                f"[{account_index}] | Solving hCaptcha challenge with Solvium..."
            )
            solvium = Solvium(
                api_key=config.CAPTCHA.SOLVIUM_API_KEY,
                session=session,
                proxy=proxy,
            )

            captcha_token = await solvium.solve_captcha(
                sitekey="914e63b4-ac20-4c24-bc92-cdb6950ccfde",
                pageurl="https://faucet.0g.ai/",
            )

        if captcha_token is None:
            raise Exception("Captcha not solved")

        logger.success(f"{account_index} | Captcha solved for faucet")

        # curl_client = await create_curl_client(proxy)

        headers = {
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="131", "Not-A.Brand";v="8", "Chromium";v="131"',
            "content-type": "text/plain;charset=UTF-8",
            "sec-ch-ua-mobile": "?0",
            "accept": "*/*",
            "origin": "https://faucet.0g.ai",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": f"https://faucet.0g.ai/?oauth_token={oauth_token}&oauth_verifier={oauth_verifier}",
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4",
            "priority": "u=1, i",
        }

        json_data = {
            "address": wallet.address,
            "hcaptchaToken": captcha_token,
            "oauth_token": oauth_token,
            "oauth_verifier": oauth_verifier,
        }

        response = await session.post(
            "https://faucet.0g.ai/api/faucet", headers=headers, json=json_data
        )

        if "hours before requesting again" in response.text:
            logger.success(
                f"{account_index} | Faucet already requested today. {response.text}"
            )
            return True

        if "Internal Server Error" in response.text:
            raise Exception(f"Faucet is just a piece of shit. Trying again...")

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
            try:
                # Get the current gas price from the network
                current_gas_price = await web3.web3.eth.gas_price
                gas_params["gasPrice"] = current_gas_price
                logger.info(
                    f"{account_index} | Using network gas price: {web3.web3.from_wei(gas_params['gasPrice'], 'gwei')} gwei"
                )
            except Exception as e:
                # Don't use fallback values, raise an error instead
                logger.error(f"{account_index} | Failed to get network gas price: {e}")
                raise Exception(f"Failed to get network gas price: {e}")

        tx_params = {
            "from": wallet.address,
            "value": 0,
            "nonce": await web3.web3.eth.get_transaction_count(
                wallet.address, "pending"
            ),
            "chainId": CHAIN_ID,
            **gas_params,
        }

        # Set transaction type based on gas params
        if "maxFeePerGas" in gas_params:
            tx_params["type"] = "0x2"

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


@retry_async(default_value=False)
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
        if balance.ether < 0.00001:
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


@retry_async(default_value=False)
async def mictonode_faucet(
    account_index: int,
    session: primp.AsyncClient,
    web3: Web3Custom,
    config: Config,
    wallet: Account,
    proxy: str,
):
    try:
        session = await create_client(proxy)

        logger.info(f"{account_index} | Starting Mictonode faucet...")

        base_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="131", "Not-A.Brand";v="8", "Chromium";v="131"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "accept-language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7,zh-TW;q=0.6,zh;q=0.5,uk;q=0.4",
            "sec-fetch-site": "same-origin",
            "origin": "https://0g-faucet.mictonode.com",
        }

        # Step 1: Get challenge token
        logger.info(f"{account_index} | Obtaining Vercel challenge token...")
        response = await session.get(
            "https://0g-faucet.mictonode.com/", headers=base_headers
        )
        challenge_token = response.headers.get("x-vercel-challenge-token")

        if not challenge_token:
            raise Exception("Vercel challenge token not found in response headers")

        logger.success(
            f"{account_index} | Got Vercel challenge token: {challenge_token}"
        )

        # Step 2: Solve the Vercel challenge
        logger.info(f"{account_index} | Solving Vercel challenge...")
        solvium = Solvium(
            api_key=config.CAPTCHA.SOLVIUM_API_KEY,
            session=session,
            proxy=proxy,
        )

        vcrcs_token = await solvium.solve_vercel_challenge(
            challenge_token=challenge_token,
            site_url="https://0g-faucet.mictonode.com",
            session=session,
        )

        if not vcrcs_token:
            raise Exception("Failed to solve Vercel challenge")

        logger.success(f"{account_index} | Vercel challenge solved successfully")

        # Step 3: Submit solution and get cookie
        logger.info(f"{account_index} | Getting vcrcs cookie...")
        headers = {
            **base_headers,
            "x-vercel-challenge-token": challenge_token,
            "x-vercel-challenge-version": "2",
            "x-vercel-challenge-solution": vcrcs_token,
            "accept": "*/*",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://0g-faucet.mictonode.com/.well-known/vercel/security/static/challenge.v2.min.js",
        }

        response = await session.post(
            "https://0g-faucet.mictonode.com/.well-known/vercel/security/request-challenge",
            headers=headers,
            timeout=30,
        )

        # Step 4: Parse and set the cookie
        if "set-cookie" not in response.headers:
            raise Exception("No cookies found in Vercel challenge response")

        cookie = SimpleCookie(response.headers["set-cookie"])
        if "_vcrcs" not in cookie:
            raise Exception("_vcrcs cookie not found in response")

        vcrcs_cookie = cookie["_vcrcs"].value
        session.set_cookies("https://0g-faucet.mictonode.com", {"_vcrcs": vcrcs_cookie})

        logger.success(f"{account_index} | Got vcrcs cookie: {vcrcs_cookie[:10]}...")

        # Step 5: Now solve the hCaptcha
        logger.info(f"{account_index} | Solving hCaptcha challenge with Solvium...")
        captcha_token = await solvium.solve_captcha(
            sitekey="6c5e817a-6d02-4698-bfec-3844064c7da4",
            pageurl="https://0g-faucet.mictonode.com/",
        )

        if not captcha_token:
            raise Exception("hCaptcha not solved")

        logger.success(f"{account_index} | hCaptcha solved for faucet")

        # Step 6: Submit the faucet request
        json_data = {
            "address": wallet.address,
            "hcaptchaToken": captcha_token,
        }

        headers = {
            **base_headers,
            "accept": "*/*",
            "content-type": "text/plain;charset=UTF-8",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://0g-faucet.mictonode.com/",
        }

        response = await session.post(
            "https://0g-faucet.mictonode.com/api/faucet",
            headers=headers,
            json=json_data,
        )

        if '"success":true' in response.text:
            logger.success(f"{account_index} | Faucet Mictonode requested successfully")
            return True

        if "System is busy processing another transaction" in response.text:
            raise Exception("Faucet is busy. Please retry later.")

        if "hours before requesting again" in response.text:
            logger.success(
                f"{account_index} | Faucet already requested today. {response.text}"
            )
            return True

        if "Internal Server Error" in response.text:
            raise Exception(f"Faucet is just a piece of shit. Trying again...")

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

        if "hours before requesting from this IP address again" in response.text:
            logger.success(
                f"{account_index} | Faucet already requested today. Wait 24 hours before requesting again or change IP."
            )
            return True

        if "Invalid Captcha" in response.text:
            raise Exception("Invalid Captcha")

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
            f"{account_index} | Faucet Mictonode error: {e}. Sleeping {random_pause} seconds..."
        )
        await asyncio.sleep(random_pause)
        raise

