import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# constants
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
MONTH_WISE_DB_ID = {
    "september" : os.getenv("Sept_db_id")
}
num_to_month = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december"
}
headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }

def get_month():
    while True:
        try:
            month_num = int(input("Enter the month (1-12): ").strip())
            if 1 <= month_num <= 12:
                return num_to_month[month_num]
            print("❌ Month must be between 1 and 12")
        except ValueError:
            print("❌ Please enter a valid number")

def get_notes():
    notes = input("Enter the notes : ").strip()
    if not notes:
        return "will add notes later"
    return notes

def get_category():
    while True:
        category = input("Enter the category : ").strip()
        if category:
            return category
        print("Please enter the Category!")

def get_amount():
    while  True:
        try:
            amt = int(input("Enter amount : ").strip())
            if amt <= 0 : 
                raise ValueError("❌ Amount must be greater than  0")
            return amt
        except ValueError as e:
            print(f"❌ {e}")

def get_date():
    while True:
        user_input = input("Enter the date in yyyy-mm-dd format (leave blank for today): ").strip()
        if not user_input:  
            return datetime.today().strftime("%Y-%m-%d")
        try:
            # validate by parsing
            parsed_date = datetime.strptime(user_input, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")  # return as string
        except ValueError:
            print("❌ Please enter a valid date in yyyy-mm-dd format")

def get_daily_db_jsonData(db_id , notes , category , amount , today):
    return {
        "parent" : {"database_id" : db_id} ,
        "properties" : {
            "Notes" : {"title": [{"text": {"content": notes}}]} ,
            "Category" : {"select" : {"name" : category}} ,
            "Amount" : {"number" : amount},
            "Date": {"date": {"start": today}}
        }
    }

def get_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }

def add_expense():
    # getting the data
    user_month = get_month()
    notes = get_notes()
    category = get_category()
    amount = get_amount()
    today = get_date()

    # month checking
    db_id = MONTH_WISE_DB_ID.get(user_month)
    if not db_id:
        print(f"❌ No database found for '{user_month}'")
        return


    #api call 
    url = "https://api.notion.com/v1/pages"

    # for daily jo kharcha hua uska data
    daily_json = get_daily_db_jsonData(db_id,notes,category,amount,today)

    try:
        res = requests.post(url , headers=headers , json=daily_json)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"API Error : {e.response.text}")
        return 
    
    print(f"Addded Expense to {user_month} month: {category} - {amount} - {today} ✅")



# def main():
#     print("Welcome to notion expense tracker !\n")
#     while True:
#         print("1. Add a new expense : \n2. View all the expenses : \n3. Exit the app")
#         choice = input("Enter your choice : ").strip()

#         match choice:
#             case "1":
#                 add_expense()
#             case "2":
#                 # view_expenses()
#                 pass
#             case "3":
#                 print("😊 Thankyou for ur visit!")
#                 break
#             case _:
#                 print("Please enter a valid choice !")

if __name__ == "__main__":
    add_expense()