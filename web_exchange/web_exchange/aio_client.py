import asyncio
import websockets
import logging
import aiohttp
import sys

from aiofile import async_open
from aiopath import AsyncPath

from aiohttp_retry import RetryClient
from websockets.exceptions import ConnectionClosed, InvalidMessage
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from datetime import datetime, timedelta

from random import randint
from time import time

date = datetime.now()

logging.basicConfig(level=logging.INFO)

async def get_exchange(n):
    start_time = time()
    
    cur_list = []
    
    conn = aiohttp.TCPConnector(limit=50)
    
    async with aiohttp.ClientSession(connector=conn) as session:
        statuses = {400, 403, 404, 429, 500, 502}
        retry_client = RetryClient(session, retry_attempts=10, retry_for_statuses=statuses)
        tasks = []
        for days in range(n):
            delta_n = date - timedelta(days=days)
            _delta_n = delta_n.strftime("%d.%m.%Y")

            url = f"https://api.privatbank.ua/p24api/exchange_rates?date={_delta_n}"
            print(_delta_n)

            task = asyncio.create_task(fetch_data(retry_client, url))
            tasks.append(task)
            
            await asyncio.sleep(randint(1, 4))
            
        results = await asyncio.gather(*tasks)
        
        for result in results:
            for exchange_rate in result["exchangeRate"]:  
                if exchange_rate["currency"] == "USD" or exchange_rate["currency"] == "EUR":
                    if "saleRate" in exchange_rate and "purchaseRate" in exchange_rate:
                        currency = exchange_rate.get("currency")
                        sale_rate = exchange_rate.get("saleRate")
                        purchase_rate = exchange_rate.get("purchaseRate")

                        cur_list.append(
                            f"Date: {result['date']}, Currency: {currency}, Buy: {purchase_rate}, Sale: {sale_rate}"
                            )
                    else:
                        continue
                    
    elapsed_time = time() - start_time
    print(f"\nElapsed time: {elapsed_time:.2f} seconds\n")
    
    return cur_list


async def fetch_data(retry_client, url):
    async with retry_client.get(url) as resp:
        logging.info(f"\n{resp}\n")
        if resp.status != 200:
            print(f"Failed to fetch {url}")
        result = await resp.json()
        return result


async def write_logs(message):
    apath = AsyncPath("../web_exchange/logs/client.log")
    if not await apath.exists():
        await apath.parent.mkdir(parents=True, exist_ok=True)
        await apath.touch()
    async with async_open("logs/client.log", "a+", encoding="utf-8") as afile:
        await afile.write(message)


async def web_socket_operation():
    
    logger = logging.getLogger('websocket')
    logger.setLevel(logging.INFO)
    address = "ws://localhost:8081"
    async with websockets.connect(address) as websocket:
        while True:
            try:
                user_input = await get_data()
                
                logger.info(f'User input: {user_input}')
                
                await websocket.send(user_input)
                print(f"\nRequest >>> {user_input}")

                get_currency = await websocket.recv()
                print(f"\nResponse <<< {get_currency}")

            except KeyboardInterrupt:
                print(f"\nKeyboard Interrupt: exit program\n")
                break
            
async def get_data():
    print(
    "\n\tHello, to get today’s exchange rate,\n\
    please enter << exchange today >> or << exchange n >>,\n\
    where << n >> is the exchange rate for a certain number of days.\n"
    
    "\n\tFor autocomplete press tab, please\n"
    )
    numbers = [str(i) for i in range(2, 11)]
    word_list = ['exchange', 'today', 'exit'] + numbers
    compl = WordCompleter(word_list)
    sess = PromptSession()
    user_input = await sess.prompt_async(
        "Input command: ",
        enable_history_search=True,
        completer=compl
    )
    
    await write_logs(f"log.Date: {date}; User input: {user_input}\n")
    
    if all(word in word_list for word in user_input.split()) and user_input != "exit":
        return user_input
    elif user_input == "exit":
        return sys.exit()
    else:
        print(f"Command << {user_input} >> not found")
    
if __name__ == "__main__":
    try:
        asyncio.run(web_socket_operation())
    except OSError:
        print("")
        logging.info("Server is inactive\n")    
        