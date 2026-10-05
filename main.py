from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import asyncio

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

store = driver.find_element(By.XPATH, '//*[@id="store"]')
store_text = str(store.text).split("\n")
game = False

store_list = []
for item in range(0, len(store_text), 2):
    store_list.append(store_text[item])

store_dict = {}
keys_list = list(store_dict.keys())
for item in store_list:
    name, cost_str = item.split(" - ")
    cost = int(cost_str.replace(',', ''))
    store_dict[item] = (name,cost)
print(store_dict)

async def game_shop_logic():
    while game is True:
        global store_dict
        money = driver.find_element(By.ID, "money").text
        money_int = int(money)
        for x in sorted(store_dict, reverse=True):
            if money_int >= store_dict[x][1]:
                element = store.find_element(By.ID, f"buy{store_dict[x][0]}")
                print(f"element bought: {store_dict[x][0]}")
                element.click()
                await asyncio.sleep(0.01)
            else:
                print("not done")
                await asyncio.sleep(0.01)
        await asyncio.sleep(5)

async def game_time():
    global game
    game = True
    await asyncio.sleep(60*2)
    game = False


async def game_loop():
    global game
    while game is True:
        cookie.click()
        await asyncio.sleep(0.001)



async def main():
    task_time = asyncio.create_task(game_time())
    task_loop = asyncio.create_task(game_loop())
    task_logic_shop = asyncio.create_task(game_shop_logic())
    await task_time
    await task_loop
    await task_logic_shop
asyncio.run(main())