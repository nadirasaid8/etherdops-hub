import sys
import asyncio
from . import *
from .core import Ether
from src.deeplchain import banner, clear, log_error, log, log_line, countdown_timer, read_config, mrh, pth, kng, hju, bru, htm, reset

config = read_config()
init(autoreset=True)

def get_status(status):
    return hju + "ON" + reset if status else mrh + "OFF" + reset

def write_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

def save_setup(setup_name, setup_data):
    with open(f'src/config/{setup_name}.json', 'w') as file:
        json.dump(setup_data, file, indent=4)
    clear()
    banner()
    print(hju + f" Setup saved on {kng}setup{pth}/{setup_name}.json")
    with open(f'src/config/{setup_name}.json', 'r') as file:
        setup_content = json.load(file)
        print(f"\n{json.dumps(setup_content, indent=4)}\n")
    print(hju + f" Quick start : {pth}python main.py {htm}--setup {pth}{setup_name}")
    input(f" Press Enter to continue...")

def load_setup(setup_file):
    with open(setup_file, 'r') as file:
        setup = json.load(file)
    return setup

def show_menu(use_proxy, random_coin, order_type, tasks_on):
    clear()
    banner()
    menu = f"""
{kng} Choose Setup :{reset}
{kng}  1.{reset} Use Proxy                  : {get_status(use_proxy)}
{kng}  2.{reset} Random Coin Predictions    : {get_status(random_coin)}
{kng}  3.{reset} Choose Predictions Type    : {get_status(order_type)}
{kng}  4.{reset} Auto Complete Tasks        : {get_status(tasks_on)}
{kng}  5.{reset} Additional Configs         : {hju}config.json{reset}
{mrh}    {pth} --------------------------------{reset}
{kng}  8.{reset} {kng}Save Setup{reset}
{kng}  9.{reset} {mrh}Reset Setup{reset}
{kng}  0.{reset} {hju}Start Bot {kng}(default){reset}
    """
    print(menu)
    choice = input(" Enter your choice (1/2/3/4/5/6/7/8): ")
    log_line()
    return choice

def show_upgrade_menu():
    clear()
    banner()
    menu = f"""
{hju} Active Menu {kng}'Auto Buy Upgrade'{reset}
{htm} {'~' * 50}{reset}
{kng} Order Method:{reset}
{kng} 1. {pth}Predict All Long{reset}
{kng} 2. {pth}Predict All Short{reset}
{kng} 3. {pth}Random Choice Long/Short{reset}
{kng} 4. {pth}back to {bru}main menu{reset}

    """
    print(menu)
    choice = input(" Enter your choice (1/2/3/4): ")
    return choice

def show_config():
    while True:
        clear()
        banner()
        config = read_config()
        
        menu = f"""
{hju} Active Menu {kng}'Change Configuration'{reset}
{htm} {'~' * 50}{reset}
{hju} Select the configuration to change:{reset}

 {kng} 1. delay for each account     {hju}(current: {config['account_delay']} seconds){reset}
 {kng} 2. sleep before start         {hju}(current: {config['sleep_before_start']} seconds){reset}
 {kng} 3. back to {bru}main menu{reset}

 {bru} NOTE: {pth}You must restart the bot after make a change{reset}

        """
        print(menu)
        
        choice = input(" Enter your choice (1/2/3): ")
        
        if choice in ['1', '2']:
            key_map = {
                '1': 'account_delay',
                '2': 'sleep_before_start',
            }
            
            key = key_map[choice]
            
            if choice == '99': 
                config[key] = not config[key]
            else: 
                new_value = input(f" Enter new value for {key}: ")
                try:
                    config[key] = int(new_value)
                except ValueError:
                    print(" Invalid input. Please enter a valid number.")
                    continue 

            write_config(config)
            print(f" {key} updated to {config[key]}")
        
        elif choice == '3':
            break 
        else:
            print(" Invalid choice. Please try again.")

async def run_bot(use_proxy, random_coin, tasks_on, order_type, _method):
    eth = Ether()
    proxy_index = 0
    countdown_timer(eth.sleep_before_start)
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                with open('data.txt', 'r') as f:
                    queries = [line.strip() for line in f.readlines()]

                total_queries = len(queries)
                log(hju + f"Number of accounts: {bru}{total_queries}")
                log(hju + f"Total Proxies: {pth}{len(eth.proxies)}" if eth.proxies else f"{pth}No proxies used")
                log(pth + "~" * 38)

                for index, query in enumerate(queries, start=1):
                    user_data = eth.extract_user_data(query)
                    username = user_data.get("username", 'Unknown')
                    log(hju + f"Account {pth}{index}/{total_queries}")
                    proxy = None

                    if use_proxy and eth.proxies:
                        proxy = eth.proxies[proxy_index]
                        proxy_host = proxy.split('@')[-1]
                        log(hju + f"Proxy: {pth}{proxy_host}")

                        proxy_index = (proxy_index + 1) % len(eth.proxies) 
                    log(hju + f"Username: {pth}{username}")

                    token = await eth.get_token(query, proxy, session)

                    if token:
                        user_info = await eth.get_user_info(token, proxy, session)
                        if user_info is not None:
                            log(hju + f"Balance: {pth}{user_info.get('balance', 0)}")
                        await eth.daily_bonus(token, proxy, session)
                        await eth.referral(token, proxy, session)

                        data_order = await eth.get_order(token, proxy, session)
                        if data_order is not None:
                            totalScore = data_order.get('totalScore', 0)
                            results = data_order.get('results', {})
                            log(bru + f"Record: {pth}{results.get('orders', 0)} {bru}Orders | {pth}{results.get('wins', 0)} {bru}Wins | "
                                    f"{pth}{results.get('loses', 0)} {bru}Loses | {pth}{results.get('winRate', 0.0)} {bru}Winrate")

                            list_periods = data_order.get('periods', [])
                            detail_coin = await eth.get_coins(token, order_type, proxy, session)
                            min_remaining_time = float('inf')

                            for period_data in list_periods:
                                period = period_data.get('period', {})
                                unlockThreshold = period.get('unlockThreshold', 0)
                                detail_order = period_data.get('order', {})
                                period_id = period.get('id', 1)

                                if detail_order is not None:
                                    coin = detail_order.get('coin', {})
                                    price_entry = detail_order.get('priceEntry')
                                    status = detail_order.get('status', '')
                                    remaining_time = detail_order.get('secondsToFinish', 0)
                                    hours = period.get('hours')
                                    change = detail_order.get('percentageChange', '')

                                    if remaining_time < min_remaining_time:
                                        min_remaining_time = remaining_time

                                    if status == "CLAIM_AVAILABLE":
                                        data_claim = await eth.claim_order(
                                            token=token, 
                                            order=detail_order, proxy=proxy, 
                                            session=session
                                        )
                                        if data_claim is not None:
                                            await eth.place_order(token, detail_coin, random_coin, period_id, _method, proxy, session)
                                            
                                            updated_data_order = await eth.get_order(token, proxy, session)
                                            if updated_data_order:
                                                list_periods = updated_data_order.get('periods', [])
                                                for period_data in list_periods:
                                                    detail_order = period_data.get('order', {})
                                                    if detail_order is not None:
                                                        remaining_time = detail_order.get('secondsToFinish', 0)

                                    elif status == "NOT_WIN":
                                        data_check = await eth.mark_checked(
                                            token=token, 
                                            order=detail_order, proxy=proxy, 
                                            session=session
                                        )
                                        if data_check is not None:
                                            await eth.place_order(token, detail_coin, random_coin, period_id, _method, proxy, session)
                                            
                                            updated_data_order = await eth.get_order(token, proxy, session)
                                            if updated_data_order:
                                                list_periods = updated_data_order.get('periods', [])
                                                for period_data in list_periods:
                                                    detail_order = period_data.get('order', {})
                                                    if detail_order is not None:
                                                        remaining_time = detail_order.get('secondsToFinish', 0)


                                    log(hju + f"Order Opened: {pth}{coin.get('symbol', 'Unknown')} {hju}at Price {pth}{price_entry} {hju}| Change: {pth}{change}%")
                                    log(hju + f"Remaining time: {pth}{remaining_time} {hju}minutes, Duration: {pth}{hours} {hju}hours")

                                if totalScore >= unlockThreshold and detail_order is None:
                                    await eth.place_order(token, detail_coin, random_coin, period_id, _method, proxy, session)

                            if tasks_on:
                                await eth.check_tasks(token, proxy, session)  

                            log(htm + "~" * 38)
                            countdown_timer(5)

                proxy_index = 0
                if min_remaining_time < float('inf'):
                    countdown_timer((min_remaining_time + 1) * 60) 
                else:
                    log(bru + f"No valid remaining time found.")

            except Exception as e:
                log(mrh + f"An unexpected error occurred: {htm} check last.log for details.")
                log_error(f"{str(e)}")



async def main():
    parser = argparse.ArgumentParser(description="Run the bot with a specified setup.")
    parser.add_argument('--setup', type=str, help='Specify the setup file to load')
    args = parser.parse_args()

    if args.setup:
        setup_file = f'src/config/{args.setup}.json'
        setup_data = load_setup(setup_file)
        use_proxy = setup_data.get('use_proxy', False)
        random_coin = setup_data.get('random_coin', False)
        tasks_on = setup_data.get('task_on', False)
        order_type = setup_data.get('order_type', False)
        _method = setup_data.get('_method', None)
        await run_bot(use_proxy, random_coin, tasks_on, order_type, _method)
    else:
        use_proxy = False
        random_coin = False
        tasks_on = False
        order_type = False
        _method = None

        while True:
            try:
                choice = show_menu(use_proxy, random_coin, order_type, tasks_on)
                if choice == '1':
                    use_proxy = not use_proxy
                elif choice == '2':
                    random_coin = not random_coin
                elif choice == '3':
                    _method = show_upgrade_menu()
                    if _method not in ['1', '2', '3']:
                        order_type = False
                    order_type = not order_type
                elif choice == '4':
                    tasks_on = not tasks_on
                elif choice == '5':
                    show_config()
                elif choice == '8':
                    setup_name = input(" Enter setup name (without space): ")
                    setup_data = {
                        'use_proxy': use_proxy,
                        'random_coin': random_coin,
                        'order_type': order_type,
                        '_method': _method,
                        'tasks_on': tasks_on,
                    }
                    save_setup(setup_name, setup_data)
                elif choice == '0':
                    await run_bot(use_proxy, random_coin, tasks_on, order_type, _method)
                elif choice == '9':
                    break
                else:
                    log(mrh + f"Invalid choice. Please try again.")
                time.sleep(1)
            except KeyboardInterrupt as e:
                sys.exit()

