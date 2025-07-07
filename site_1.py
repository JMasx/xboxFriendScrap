import time
import random
import networkx as nx
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import os  # Uncomment if using relative path for chromedriver

# Absolute path to chromedriver (change this as needed)
ABSOLUTE_DRIVER_PATH = 'C:/Users/masca/Documents/Dev/newgen-scrappers/chromedriver-win64/chromedriver.exe'

def scrape_friends_for_gamertag(driver, wait, gamertag):
    url = f"https://www.xbox.com/en-US/play/user/{gamertag}"
    driver.get(url)
    print(f"\nVisiting profile of {gamertag}")

    time.sleep(random.uniform(3.5, 7.5))  

    try:
        friends_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(text(), 'Friends')]/parent::div")
        ))
        friends_button.click()
        print(f"Clicked Friends button on {gamertag}")
    except Exception as e:
        print(f"Failed to click Friends button on {gamertag}: {e}")
        return []

    try:
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".FriendsAndFollowersList-module__userList___RYzIa")
        ))
        time.sleep(random.uniform(1, 2))
    except Exception as e:
        print(f"Friends list did not load for {gamertag}: {e}")
        return []

    friends = []
    try:
        friend_elements = driver.find_elements(By.CSS_SELECTOR, ".Gamertag-module__baseGamerTag___lwdQS")
        for elem in friend_elements:
            name = elem.text.strip()
            if not name:
                name = elem.get_attribute('innerText').strip()
            if name:
                friends.append(name)
    except Exception as e:
        print(f"Error extracting friends for {gamertag}: {e}")

    print(f"{gamertag} has {len(friends)} friends")
    return friends


def crawl_friend_graph(start_gamertag, max_profiles=150):
    # Use the absolute path variable for chromedriver
    service = Service(ABSOLUTE_DRIVER_PATH)

    # --- Optional: Use this for relative pathing (uncomment the lines below and comment the line above) ---
    # import os
    # driver_path = os.path.join(os.path.dirname(__file__), "chromedriver", "chromedriver.exe")
    # service = Service(driver_path)

    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 60)

    driver.get("https://www.xbox.com/en-US/play")
    print("Please log in manually, then press Enter to continue...")
    input()

    visited = set()
    queue = [start_gamertag]
    graph = {}

    profiles_scraped = 0

    while queue and len(visited) < max_profiles:
        current = queue.pop(0)
        if current in visited:
            continue

        friends = scrape_friends_for_gamertag(driver, wait, current)
        graph[current] = friends
        visited.add(current)
        profiles_scraped += 1

        for friend in friends:
            if friend not in visited and friend not in queue:
                queue.append(friend)

        sleep_time = random.uniform(3, 7)
        print(f"Sleeping {sleep_time:.1f} seconds to avoid rate limiting...")
        time.sleep(sleep_time)

        if profiles_scraped % 5 == 0:
            long_pause = random.uniform(10, 20)
            print(f"Taking a long pause of {long_pause:.1f} seconds after {profiles_scraped} profiles...")
            time.sleep(long_pause)

    driver.quit()
    return graph


def visualize_friend_graph(graph):
    G = nx.Graph()

    for user, friends in graph.items():
        G.add_node(user)
        for friend in friends:
            G.add_node(friend)
            G.add_edge(user, friend)

    pos = nx.spring_layout(G, k=0.5, iterations=50)

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

    plt.title("Xbox Friend Cluster Graph")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    start_user = "Jadenize"  # start user change
    friend_graph = crawl_friend_graph(start_user, max_profiles=50)

    print("\nFinal friend graph data:")
    for user, friends in friend_graph.items():
        print(f"{user}: {friends}")

    visualize_friend_graph(friend_graph)
