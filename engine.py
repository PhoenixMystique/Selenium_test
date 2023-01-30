import math

import requests as requests
from selenium import webdriver
import csv
import os
from selenium.webdriver.common.by import By
import config
from pymongo import MongoClient

class Scrapper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        # self.driver.get(config.URL)
        self.data = []
        client = MongoClient(config.MongoDB)
        db = client["disease"]
        self.collection = db["data"]

    def get_data(self):
        elements = self.driver.find_elements(By.CSS_SELECTOR,config.css_card)
        for element in elements:
            name = element.find_element(By.XPATH,".//h6").text
            print(name)
            url = element.get_attribute("href")
            icon = element.find_element(By.XPATH,".//img").get_attribute("src")
            self.data.append([name, url, icon])
        print(self.data)

    def save_images(self):
        if not os.path.exists("image"):
            os.makedirs("image")
        for item in self.data:
            icon_url = item[2]
            icon_name = item[0]+ ".jpg"
            r = requests.get(icon_url)
            open("image/" + icon_name, "wb").write(r.content)
    def export_data(self):
         with open("data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "url", "Image"])
            writer.writerows(self.data)
         self.driver.close()
    def insert_data(self):
        for item in self.data:
            self.collection.insert_one({"name": item[0], "url": item[1], "image": item[0]+ ".jpg"})
    def close(self):
        self.driver.close()

    def mystery(self,n):
        V =pow(10, n + 1) * (9 * n - 1) + 10
        V = V/pow(9, 3) - n * (n + 1) / 18
        return math.floor(V)


en = Scrapper()
en.get_data()
# en.save_images() # uncomment this line to save images
en.export_data()
en.insert_data()

print(en.mystery(1))
print(en.mystery(2))
print(en.mystery(3))
print(en.mystery(4))

