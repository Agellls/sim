import requests
import time
from termcolor import colored
import hashlib
from datetime import datetime
import os
import base64


# def clear_screen():
#     os.system("cls" if os.name == "nt" else "clear")


# def setHwid():
#     # Define your_hwid
#     your_hwid = "your_base64_encoded_hwid"

#     # Read the hwid from the file
#     with open("hwid", "r") as f:
#         hwid = f.read().strip()

#     # Check if the hwid matches your_hwid or contains "@@@FFFF@@@"
#     if hwid == your_hwid or "@@@XDYI@@@" in hwid:
#         # Get the current datetime
#         now = datetime.now()

#         # Convert the datetime to string
#         now_str = str(now)

#         # Encode the string to bytes
#         now_bytes = now_str.encode("utf-8")

#         # Convert the bytes to base64
#         now_base64 = base64.b64encode(now_bytes)

#         # Convert the base64 bytes back to string
#         now_base64_str = now_base64.decode("utf-8")

#         # If "@@@FFFF@@@" is in hwid, replace "FFFF" with now_base64_str
#         if "@@@XDYI@@@" in hwid:
#             hwid = hwid.replace("XDYI", now_base64_str)

#         # Write the modified hwid to a file
#         with open("hwid", "w") as f:
#             f.write(hwid)


# def extractStringFromFile():
#     # Read the content from the file
#     with open("hwid", "r") as f:
#         content = f.read().strip()

#     # Find the start and end of the string
#     start = content.find("@@@") + 3
#     end = content.find("@@@", start)

#     # Extract the string
#     extracted_string = content[start:end]

#     return extracted_string


# def generateDeviceId(seed):
#     # Use the extractStringFromFile function to get the volatile_seed
#     volatile_seed = extractStringFromFile()

#     # Create a new MD5 hash object
#     m = hashlib.md5()

#     # Update the hash object with the combined seed and volatile_seed
#     m.update((seed + volatile_seed).encode("utf-8"))

#     # Return the device ID
#     return "agellls-" + m.hexdigest()[:16]


# def read_key_from_file(filename):
#     with open(filename, "r") as file:
#         key_line = file.read().strip()
#         key = key_line.split("=")[1].strip()  # Extract key from the line 'key = <key>'
#         return key


# def write_key_to_file(filename, key):
#     with open(filename, "w") as file:
#         file.write(f"key = {key}")


# def check_key(key, device_id):
#     response = requests.get(
#         f"https://agellls.000webhostapp.com/data_api.php?serial_number={key}"
#     )
#     uuid = response.text.strip()
#     if uuid == device_id:
#         print("Login Successful\n")
#         return True
#     else:
#         print("Login Failed\n")
#         return False


# def check_date_key(key):
#     response = requests.get(
#         f"https://agellls.000webhostapp.com/data_api_date.php?serial_number={key}"
#     )
#     date_end = response.text.strip()
#     return date_end


# def is_date_in_range(database_date):
#     try:
#         database_date = datetime.strptime(database_date, "%Y-%m-%d")
#         current_date = datetime.now()
#         return current_date <= database_date
#     except ValueError:
#         return False


# clear_screen()
# setHwid()

# seed = "agellls"
# device_id = generateDeviceId(seed)
# print("Your UUID : " + device_id + "\n")

# filename = "key"
# key = read_key_from_file(filename)

# while not check_key(key, device_id):
#     key = input("Please Input Key : ")
#     print("")
#     write_key_to_file(filename, key)

# while True:
#     database_date = check_date_key(key)
#     result = is_date_in_range(database_date)

#     if result:
#         break
#     else:
#         print("Key expired\n")
#         key = input("Please Input Key : ")
#         print("")
#         write_key_to_file(filename, key)


# get rate USD to IDR
def get_usd_to_idr_rate():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["rates"]["IDR"]
    else:
        print("Error fetching exchange rate")
        return None


# Open the file in read mode
with open("apikey", "r") as file:
    # Read the lines of the file
    lines = file.readlines()

apikey = lines[0].split("=")[1].strip()


def get_apikey(api_key):
    url = "https://smshub.org/stubs/handler_api.php"
    params = {
        "api_key": api_key,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        apikey = (
            response.text.replace("NO_ACTION", "") + "Apikey telah berhasil dipakai"
        )
        return apikey
    else:
        return None


def get_balance(api_key):
    url = "https://smshub.org/stubs/handler_api.php"
    params = {"api_key": api_key, "action": "getBalance"}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        if "BAD_KEY" in response.text:
            print("Invalid APIkey SMSHUB\n")
            new_api_key = input("Please enter a new APIkey SMSHUB : ")
            print("")
            with open("apikey", "w") as file:
                file.write(f"apikey = {new_api_key}")
            return get_balance(new_api_key)
        elif "NO_KEY" in response.text:
            print("Invalid APIkey SMSHUB\n")
            new_api_key = input("Please enter a new APIkey SMSHUB : ")
            print("")
            with open("apikey", "w") as file:
                file.write(f"apikey = {new_api_key}")
            return get_balance(new_api_key)
        else:
            print("+-----------------------------+\n")
            print("Welcome to SMSHUB version CLI \n")
            balance_usd = float(response.text.replace("ACCESS_BALANCE:", ""))
            exchange_rate = get_usd_to_idr_rate()
            if exchange_rate:
                balance_idr = balance_usd * exchange_rate
                balance_idr_formatted = round(
                    balance_idr, 3
                )  # Rounds to three decimal places
                print(
                    f"Your Balance : {balance_usd} USD or {balance_idr_formatted} IDR\n"
                )
            else:
                print(f"Your Balance : {balance_usd} USD\n")
    else:
        return None


def order_number(api_key, type_order, max_price):
    service, country, operator = type_order.split()

    url = "https://smshub.org/stubs/handler_api.php"
    params = {
        "api_key": api_key,
        "action": "getNumber",
        "service": service,
        "operator": operator,
        "country": country,
        "maxPrice": max_price,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        response_text = response.text.replace("ACCESS_NUMBER:", "")
        print("Service: " + colored(get_name_service(service_code), "cyan"))
        order_id, nomor = response_text.split(":")
        print(f"Order ID: {order_id}\nNomor: {colored(nomor, 'yellow')}")
        print("Status : Waiting OTP")
        return order_id, nomor
    else:
        return None, None


def wait_status(api_key, order_id):
    url = "https://smshub.org/stubs/handler_api.php"
    start_time = time.time()  # record the start time
    otp_received = False  # flag to indicate if the otp has been received

    while True:
        elapsed_time = time.time() - start_time  # calculate elapsed time
        if otp_received:
            break
        if elapsed_time > 60:  # if more than 1 minutes have passed
            user_input = input(
                "OTP not received in 1 minutes\n[y] Continue Waiting\n[n] Cancel & Exit\n[r] Cancel & Repeat a New Order\nChoose an option? (y/n/r): "
            )
            if user_input.lower() == "r":
                cancel_status(api_key, order_id)
                print("\n+-----------------------------+\n")
                print("Type [3] to make a New Order")
                break
            elif user_input.lower() == "y":
                print("Continue to wait for OTP...")
                start_time = time.time()  # reset the start time
                continue
            elif user_input.lower() == "n":
                cancel_status(api_key, order_id)
                print(
                    "Thank you for using this service\n\n+-----------------------------+\n"
                )
                exit(0)
            else:
                print("Wrong input. Wait a seconds & Please enter [y], [n], or [r]")

        url = f"{url}?api_key={api_key}&action=getStatus&id={order_id}"
        status_response = requests.get(url)
        if "STATUS_OK:" in status_response.text:
            otp_received = True
            otp = status_response.text.split(":")[
                1
            ].strip()  # split the response by ':' and get the second part
            print(f"otp: {colored(otp, 'green')}")  # print the otp in green
            if otp_received:
                break

        time.sleep(5)  # wait for 5 seconds before checking again


def resend_status(api_key, order_id, nomor):
    url = "https://smshub.org/stubs/handler_api.php"
    url = f"{url}?api_key={api_key}&action=setStatus&status=3&id={order_id}"
    status_response = requests.get(url)
    print("Service: " + colored(get_name_service(service_code), "cyan"))
    print(f"Order ID: {order_id}\nNomor: {colored(nomor, 'yellow')}")
    print("Status : Resend OTP")
    wait_status(api_key, order_id)


def cancel_status(api_key, order_id):
    url = "https://smshub.org/stubs/handler_api.php"
    url = f"{url}?api_key={api_key}&action=setStatus&status=8&id={order_id}"
    requests.get(url)
    print("Order canceled")


def complete_status(api_key, order_id):
    url = "https://smshub.org/stubs/handler_api.php"
    url = f"{url}?api_key={api_key}&action=setStatus&status=6&id={order_id}"
    requests.get(url)


def repeat_order(api_key, type_order, max_price):
    order_id, nomor = order_number(api_key, type_order, max_price)
    wait_status(api_key, order_id)
    return order_id, nomor


def check_price(api_key):
    # Base URL
    url = "https://smshub.org/stubs/handler_api.php"

    # Parameters
    params = {
        "api_key": api_key,
        "action": "getPrices",
    }

    # Get user input for service and country
    service = input("Enter the service [ni/ns/etc..]: ")
    country = input("Enter the country [0/6/etc..]: ")

    print("")

    # Set the service and country in the parameters
    params["service"] = service
    params["country"] = country
    response = requests.get(url, params=params)

    # Parse the response JSON
    response_json = response.json()

    # Extract the service data
    service_data = response_json.get(str(country), {}).get(service, {})

    # Check if the service data is empty
    if not service_data:
        print("Sorry, invalid service or country.")
        return

    # Fetch the USD to IDR exchange rate
    exchange_rate = get_usd_to_idr_rate()

    # Print the price and stock
    for price, stock in service_data.items():
        # Convert price to IDR
        price_idr = float(price) * exchange_rate
        # Format the price to three decimal places
        price_idr_formatted = round(price_idr, 3)
        print(
            f"Price: {colored(price, 'green')} USD / {colored(str(price_idr_formatted), 'yellow')} IDR => Stock: {colored(stock, 'cyan')}"
        )


def get_code_service():
    service_name = input("Enter the service name [amazon/gojek/etc..]: ")
    service_name = service_name.lower()
    with open("service", "r", encoding="utf-8") as file:
        for line in file:
            code, name = line.strip().split("|")
            if name == service_name:
                return code
    return None


def get_name_service(service_code):
    service_code = service_code
    with open("service", "r", encoding="utf-8") as file:
        for line in file:
            code, name = line.strip().split("|")
            if code == service_code:
                return name
    return None


def get_code_country():
    country_name = input("Enter the country name [indonesia/fiji/etc..]: ")
    country_name = country_name.lower()
    with open("country", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("|")
            code = parts[0]
            name = parts[1]
            operators = parts[2:]
            if name == country_name:
                return code, operators
    return None, None


def get_name_country(country):
    country_code = country
    with open("country", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("|")
            code = parts[0]
            name = parts[1]
            operators = parts[2:]
            if code == country_code:
                return name
    return None, None


def lower_price(service_search, target_price):
    # Fetch the USD to IDR exchange rate
    exchange_rate = get_usd_to_idr_rate()

    # Base URL
    url = "https://smshub.org/stubs/handler_api.php"

    # Parameters
    params = {
        "api_key": "173749Ue71b80c9cfc542c774bce15cee09798b",
        "action": "getPrices",
        "service": service_search,
    }

    # Convert target_price to float for comparison
    target_price = float(target_price)

    # Iterate over country codes from 0 to 200
    for country in range(202):
        # Check if the country code is 50, 100, 150, or 200
        if country in [51, 101, 151]:
            # Ask the user if they want to continue
            continue_check = input(
                "Check the previous data, Do you want to continue? [y/n]: "
            )
            if continue_check.lower() == "n":
                break

        # Set the country in the parameters
        params["country"] = str(country)
        response = requests.get(url, params=params)

        # Parse the response JSON
        response_json = response.json()

        # Extract the service data
        service_data = response_json.get(str(country), {}).get(service_search, {})

        # Get the country name
        country_name = get_name_country(str(country))

        # Check if the service data is empty
        if not service_data:
            print(
                colored(
                    f"Country {country_name} with code {country} is not available.",
                    "red",
                )
            )
        else:
            for price in service_data.keys():
                price_idr = float(price) * exchange_rate
                price_idr_formatted = round(price_idr, 3)
                # If the price is less than or equal to the target price, print the country code
                if float(price) <= target_price:
                    print(
                        colored(
                            f"Country {country_name} with code {country} has available and have the price of {price} USD / {price_idr_formatted} IDR.",
                            "green",
                        )
                    )
                    break  # Stop checking other prices for this country
                else:
                    print(
                        colored(
                            f"Country {country_name} with code {country} has available but the lower price {price} USD / {price_idr_formatted} IDR.",
                            "cyan",
                        )
                    )
                    break
    print("")


api_key = apikey
while True:
    print(get_balance(api_key))
    user_input = input(
        "List:\n[1] Order Number\n[2] Check Price Number\n[3] Check Service Code\n[4] Check Country Code\n[5] Check Lower Price [VIP Fiture]\n[0] Quit (After Input Key & Apikey Choose This!)\nChoose an option (1/2/3/4/0): "
    )
    print("\n+-----------------------------+\n")
    if user_input == "1":
        type_order = input("Enter order [ni 6 any/go 38 any/etc..]: ")
        max_price = input("Enter price [0.67/1.32/etc..]: ")
        print("\n+-----------------------------+\n")
        service_code, a, b = type_order.split(" ")
        order_id, nomor = order_number(api_key, type_order, max_price)
        wait_status(api_key, order_id)
        while True:
            print("\n+-----------------------------+\n")
            user_input = input(
                "List:\n[1] Resend OTP\n[2] Complete OTP\n[3] Repeat a New Order\nChoose an option[1/2/3]: "
            )
            print("\n+-----------------------------+\n")
            if user_input == "1":
                resend_status(api_key, order_id, nomor)
            elif user_input == "2":
                complete_status(api_key, order_id)
                print("Order completed\n")
                break
            elif user_input == "3":
                complete_status(api_key, order_id)
                print("Repeat a New Order\n")
                print("+-----------------------------+\n")
                order_id, nomor = repeat_order(api_key, type_order, max_price)
            else:
                print(
                    "Invalid input. Please type [1] to Resend OTP, [2] to Complete OTP, [3] to Repeat a New Order.\n"
                )
    elif user_input == "2":
        print("Check your price number")
        check_price(api_key)
        print("")
    elif user_input == "3":
        print("The service code: " + colored(get_code_service(), "green") + "\n")
    elif user_input == "4":
        code, operators = get_code_country()
        if code and operators:
            oper = ", ".join(operators)
            print("The country code: " + colored(code, "yellow"))
            print("The operators: " + colored(oper, "cyan") + "\n")
        else:
            print("Country not found.\n")
    elif user_input == "5":
        print("Search the lower price of your service")
        service_search = input("Enter the service code [ka/ni/etc..]: ")
        target_price = input("Enter the target price [0.67/3.00/etc..]: ")
        print("\n+-----------------------------+\n")
        lower_price(service_search, target_price)
    elif user_input == "0":
        print("Thank you for using this service\n")
        break
    else:
        print(
            "Invalid input. Please type [1] to Order a Number, [2] to Check Price, [3] to Check Service, [4] to Check Country, [5] to Check Lower Price and [0] to quit.\n"
        )
