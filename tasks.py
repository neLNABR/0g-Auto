TASKS = ["FAUCET"]

TASKS_DO = [
    ("easynode_deploy", "storagescan_deploy", "mintair_deploy", "zero_exchange_swaps", "puzzlemania")
]

EASYNODE_DEPLOY = ["easynode_deploy"]
FAUCET = ["faucet"]
FAUCET_TOKENS = ["faucet_tokens"]
PUZZLEMANIA = ["puzzlemania"]
STORAGESCAN_DEPLOY = ["storagescan_deploy"]
MINTAIR_DEPLOY = ["mintair_deploy"]
ZERO_EXCHANGE_SWAPS = ["zero_exchange_swaps"]

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
    ("storagescan_deploy", "mintair_deploy"),
    ["puzzlemania", "easynode_deploy"],
    "storagescan_deploy",
]
--------------------------------


BELOW ARE THE READY-MADE TASKS THAT YOU CAN USE:
СНИЗУ ПРИВЕДЕНЫ ГОТОВЫЕ ПРИМЕРЫ ЗАДАЧ, КОТОРЫЕ ВЫ МОЖЕТЕ ИСПОЛЬЗОВАТЬ:
以下是您可以使用的现成任务：

crusty_refuel - refuel MEGAETH at https://www.crustyswap.com/
crusty_refuel_from_one_to_all - refuel MEGAETH from one to all wallets at https://www.crustyswap.com/
cex_withdrawal - withdraw ETH from cex exchange (okx, bitget)
faucet - faucet A0GI tokens (needs captcha and twitter)
storagescan_deploy - deploy storagescan file
mintair_deploy - deploy contract at https://contracts.mintair.xyz/
puzzlemania - complete tasks on https://puzzlemania.0g.ai/
easynode_deploy - deploy easynode contract at https://playground.easy-node.xyz/
faucet_tokens - faucet ETH/BTC/USDT tokens https://test.zer0.exchange/faucet
zero_exchange_swaps - swaps tokens on https://test.zer0.exchange/swap
"""
