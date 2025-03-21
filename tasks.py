TASKS = ["FULL_TASK"]


FULL_TASK = [
    "FAUCET",
    "FAUCET_TOKENS",
    "SWAPS",
    "STORAGESCAN_DEPLOY",
    "CONFT_APP",
]

ONLY_SWAPS = [
    "STORAGESCAN_DEPLOY",
    "CONFT_APP",
    "SWAPS",
]

EVERY_DAY = [
    "FAUCET",
    "FAUCET_TOKENS",
    ["SWAPS", "SKIP"],
    ("MINT_PANDA_0G", "MINT_NERZO_0GOG", "STORAGESCAN_DEPLOY", "CONFT_APP"),
    "SWAPS",
]

FAUCET = ["faucet"]
SWAPS = ["swaps"]
FAUCET_TOKENS = ["faucet_tokens"]
STORAGESCAN_DEPLOY = ["storagescan_deploy"]
CONFT_APP = ["conft_mint"]
MINT_AURA = ["mint_aura"]
MINT_PANDA_0G = ["mint_panda_0g"]

"""
EN:
You can create your own task with the modules you need 
and add it to the TASKS list or use our ready-made preset tasks.

( ) - Means that all of the modules inside the brackets will be executed 
in random order
[ ] - Means that only one of the modules inside the brackets will be executed 
on random
SEE THE EXAMPLE BELOW:

RU:
Вы можете создать свою задачу с модулями, которые вам нужны, 
и добавить ее в список TASKS, см. пример ниже:

( ) - означает, что все модули внутри скобок будут выполнены в случайном порядке
[ ] - означает, что будет выполнен только один из модулей внутри скобок в случайном порядке
СМОТРИТЕ ПРИМЕР НИЖЕ:

CHINESE:
你可以创建自己的任务，使用你需要的模块，
并将其添加到TASKS列表中，请参见下面的示例：

( ) - 表示括号内的所有模块将按随机顺序执行
[ ] - 表示括号内的模块将按随机顺序执行

--------------------------------
!!! IMPORTANT !!!
EXAMPLE | ПРИМЕР | 示例:

TASKS = [
    "CREATE_YOUR_OWN_TASK",
]
CREATE_YOUR_OWN_TASK = [
    "faucet",
    ("faucet_tokens", "swaps"),
    ["storagescan_deploy", "conft_mint"],
    "swaps",
]
--------------------------------


BELOW ARE THE READY-MADE TASKS THAT YOU CAN USE:
СНИЗУ ПРИВЕДЕНЫ ГОТОВЫЕ ПРИМЕРЫ ЗАДАЧ, КОТОРЫЕ ВЫ МОЖЕТЕ ИСПОЛЬЗОВАТЬ:
以下是您可以使用的现成任务：


faucet - faucet A0GI tokens (needs captcha)
faucet_tokens - faucet ETH/BTC/USDT tokens (needs A0GI balance)
swaps - swaps tokens randomly on 0g hub
storagescan_deploy - deploy storagescan file
conft_mint - mint conftApp nft (once per wallet) and mint Domain
mint_aura - mint aura panda nft (once per wallet) - https://www.mintaura.io/panda
mint_panda_0g - mint panda 0g nft (once per wallet) - https://nerzo.xyz/0gog
"""
