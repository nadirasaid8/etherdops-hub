import os
import json
import time
import random
import aiohttp
from colorama import init
from src.headers import headers
from urllib.parse import unquote
from json.decoder import JSONDecodeError
from src.deeplchain import countdown_timer, clear, log, htm, banner, read_config, kng, mrh, pth, bru, log_error, hju

init(autoreset=True)
config = read_config()    

class Ether:
    def __init__(self):
        self.BASE_URL = "https://api.miniapp.dropstab.com/api"
        self.sleep_before_start = config.get('sleep_before_start', 10)
        self.delay = config.get('account_delay', 5)
        self.header = headers()
        self.proxies = self.load_proxies()

    def load_proxies(self):
        proxies_file = os.path.join(os.path.dirname(__file__), '../proxies.txt')
        formatted_proxies = []
        with open(proxies_file, 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy:
                    if proxy.startswith("socks5://"):
                        formatted_proxies.append(proxy)
                    elif not (proxy.startswith("http://") or proxy.startswith("https://")):
                        formatted_proxies.append(f"http://{proxy}")
                    else:
                        formatted_proxies.append(proxy)
        return formatted_proxies
    
    def load_query(self):
        try:
            with open('data.txt', 'r') as f:
                queries = [line.strip() for line in f.readlines()]
            return queries
        except FileNotFoundError:
            log("File data.txt not found.")
            return []
        except Exception as e:
            log("Failed to get Query:", str(e))
            return []

    @staticmethod
    def extract_user_data(query: str) -> dict:
        if not query:
            raise ValueError("Received empty auth data.")
        try:
            return json.loads(unquote(query).split("user=")[1].split("&auth")[0])
        except (IndexError, JSONDecodeError) as e:
            log(f"Error decoding user data: {e}")
            return {}

    async def get_token(self, query: str, proxy, session):
        url = f"{self.BASE_URL}/auth/login"
        headers = self.header
        payload = {"webAppData": query}
        async with session.post(url, headers=headers, json=payload, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                token = data.get("jwt", {}).get("access", {}).get("token")
                return token
            
    async def get_user_info(self,  token, proxy, session):
        url = f"{self.BASE_URL}/user/current"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.get(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                return data

    async def daily_bonus(self, token, proxy, session):
        url = f"{self.BASE_URL}/bonus/dailyBonus"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.post(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                result = data.get('result',False)
                if result:
                    log(hju + f"Daily reward claimed | Streaks: {pth}{data['streaks']}")
                else:
                    log(kng + f"Daily reward already claimed")

    async def check_tasks(self, token, proxy, session):
        url = f"{self.BASE_URL}/quest"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        try:
            async with session.get(url, headers=headers, proxy=proxy) as response:
                if response is not None:
                    tasks = await response.json()
                    for task in tasks:
                        name = task.get('name','')
                        quests = task.get('quests',[])
                        for quest in quests:
                            claimAllowed = quest.get('claimAllowed',False)
                            name = quest.get('name','')
                            status = quest.get('status')
                            if status == "COMPLETED":
                                log(kng + f"Task {pth}{name} {kng}is completed")
                            else:
                                if claimAllowed:
                                    await self.claim_task(token, quest["id"], name, proxy, session)
                                else:
                                    await self.verify_task(token, quest["id"], name, proxy, session)
        except Exception as e:
            log(f"Error Detail : {e}")

    async def verify_task(self, token, task_id, name, proxy, session):
        url = f"{self.BASE_URL}/quest/{task_id}/verify"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.put(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                log(hju + f"Verification Task {pth}{name} {kng}: {data.get('status','')}")

    async def claim_task(self, token, task_id, name, proxy, session):
        url = f"{self.BASE_URL}/quest/{task_id}/claim"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.put(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                log(hju + f"Claim Task {pth}{name} {kng}: {data.get('status','')}")

    async def referral(self, token, proxy, session):
        url = f"{self.BASE_URL}/refLink"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.get(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                available = data.get('availableToClaim',0)
                if available > 0:
                    self.claim_ref(token, proxy, session)
                else:
                    log(kng + f"No Referral Reward Available")

    async def claim_ref(self, token, proxy, session):
        url = f"{self.BASE_URL}/refLink/claim"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.post(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                totalReward = data.get('totalReward',0)
                log(hju + f"Referral Reward claimed {pth}{totalReward}")

    async def get_order(self, token, proxy, session):
        url = f"{self.BASE_URL}/order"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.get(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                return data
    
    async def get_coins(self, token,  randoms, proxy, session):
        url = f"{self.BASE_URL}/order/coins"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.get(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                return data
    
    async def get_detail_coin(self, token, id, proxy, session):
        url = f"{self.BASE_URL}/order/coinStats/{id}"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.get(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                return data
        
    async def post_order(self, token, payload, proxy, session):
        url = f"{self.BASE_URL}/order"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.post(url, headers=headers, json=payload, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                list_periods = data.get('periods',[])
                for data in list_periods:
                    period = data.get('period',[])
                    hours = period.get('hours')
                    order = data.get('order',{})
                    if len(order) > 0:
                        shorts = "Long"
                        if order.get('short'):
                            shorts = "Short"
                        coin = order.get('coin')
                        log(hju + f"Open {pth}{shorts} {hju}in {pth}{coin.get('symbol')} {hju}at Price {pth}{coin.get('price')} {hju}time {pth}{hours} {hju}Hours")
                        break

    async def claim_order(self, token, order, proxy, session):
        id = order.get('id')
        url = f"{self.BASE_URL}/order/{id}/claim"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.put(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                log(hju + f"Last Prediction : {pth}{order.get('coin').get('symbol')} {hju}| Time: {pth}{order.get('period').get('hours')} {hju}| Reward : {pth}{order.get('reward')} {hju}| Correct : {pth}{order.get('result')}")
                return data
    
    async def mark_checked(self, token, order, proxy, session):
        id = order.get('id')
        url = f"{self.BASE_URL}/order/{id}/markUserChecked"
        headers = {**self.header,'authorization': f"Bearer {token}"}
        async with session.put(url, headers=headers, proxy=proxy) as response:
            if response is not None:
                data = await response.json()
                log(mrh + f"Last Prediction : {pth}{order.get('coin').get('symbol')} {mrh}| Time: {pth}{order.get('period').get('hours')} {mrh}| Correct : {pth}{order.get('result')}")
                return data

    async def place_order(self, token, detail_coin, random_coin, period_id, _method, proxy, session):
        status = [True, False]
        coins = random.choice(detail_coin) if random_coin else detail_coin[0]
        coin_id = coins.get('id')
        
        if _method == '1':
            payload = {'coinId': coin_id, 'short': False, 'periodId': period_id}
        elif _method == '2':
            payload = {'coinId': coin_id, 'short': True, 'periodId': period_id}
        elif _method == '3':
            payload = {'coinId': coin_id, 'short': random.choice(status), 'periodId': period_id}
        else:
            payload = {'coinId': coin_id, 'short': random.choice(status), 'periodId': period_id}
            
        await self.post_order(token=token, payload=payload, proxy=proxy, session=session)