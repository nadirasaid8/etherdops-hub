# DROPTABS - ETHERDOPS

The EtherDrops Mini App is an application created by the [EtherDrops](https://t.me/fomo/app?startapp=ref_HHI7F) and DropsTab team with the support of DWF Labs.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [CONTACT](https://t.me/imspecials)

## How to Earn $DPS:
 - Visit: [Etherdrops](https://t.me/fomo/app?startapp=ref_HHI7F)
 - Start the bot & open Apps
 - Do Check-in Every day
 - Complete Quest to Earn DPS 
 - Trade Long / Short with 0 token

 ## Feature
 - **Drops Quest**: A feature that allows users to complete quests to earn DPS tokens
 - **Drops Check-in**: A feature that allows users to check-in daily to earn DPS tokens
 - **Drops Long/Short**: A feature that allows users to trade long or short

 ## IMPORTANT NOTE
  - This bot is under development for convenience and bugs
  - The query id for this script only lasts at least 1 to 2 days.

  ## Requirements

- Python 3.10+

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/nadirasaid8/etherdops-hub.git
    ```

2. **Navigate to the project directory**

    ```bash
    cd etherdops-hub
    ```

3. **Create a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `config.json` file**

    The `config.json` file should be in the root directory of the project. Here is a sample configuration:

    ```json
    {
        "account_delay": 5,
        "sleep_before_start": 15
    }

    ```
    - `sleep_before_start`: the sleep time before running the bot 
    - `account_delay`: Delay between processing each account (in seconds).

## Usage
before starting the bot you must have your own initdata / queryid telegram!

1. Use PC/Laptop or Use USB Debugging Phone
2. open the `Etherdrops telegram bot`
3. Inspect Element or `(F12)` on the keyboard
4. at the top of the choose "`Application`" 
5. then select "`Session Storage`" 
6. Select the links "`Etherdrops`" and "`tgWebAppData`"
7. Take the value part of "`tgWebAppData`"
8. take the part that looks like this: 

```txt 
query_id=xxxxxxxxx-Rxxxxuj&user=%7B%22id%22%3A1323733375%2C%22first_name%22%3A%22xxxx%22%2C%22last_name%22%3A%22%E7%9A%BF%20xxxxxx%22%2C%22username%22%3A%22xxxxx%22%2C%22language_code%22%3A%22id%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=xxxxx&hash=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
9. add it to `data.txt` file or create it if you dont have one


You can add more and run the accounts in turn by entering a query id in new line like this:
```txt
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
query_id=xxxxxxxxx-Rxxxxxxx&hash=xxxxxxxxxxx
```

10. **Create a `proxies.txt` file**

    The `proxies.txt` file should be in the root directory and contain a list of proxies in the format `username:password@host:port`.

    Example:

    ```
    user1:pass1@ip1:port1
    user2:pass2@ip2:port2
    ```

11. **To run the bot, execute the following command:**

```bash
python main.py
```

### Instant Setup:
- **Loading setup via CLI argument:** If the `--setup` argument is provided, the script will load the corresponding `.json` file and run the bot directly without displaying the menu.
- **Menu display:** If no `--setup` argument is provided, the script will display the menu as usual.
- **Setup saving:** The option to save setups has been included in the menu as option `8`.

This will allow you to run the script directly with a predefined setup like this:

```bash
python main.py --setup mysetup
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact [ https://t.me/DeeplChain ]
