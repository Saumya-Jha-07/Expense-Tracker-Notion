import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")

MONTH_WISE_DB_ID = {
    "september" : os.getenv("Sept_db_id")
}



def add_expense():
    # getting the data
    user_month = input("Enter full month name : ").strip().lower()
    notes = input("Enter notes : ").strip()
    Category = input("Enter category : ").strip()
    Amount = int(input("Enter amount : ").strip())
    today = input("Enter the date in yyyy-mm-dd format ONLY or leave blank for today's date : ") or datetime.today().strftime("%Y-%m-%d")

    # month checking
    DB_ID = ""
    for month,db_id in MONTH_WISE_DB_ID.items():
        if user_month == month:
            DB_ID = db_id
            break
    
    if not DB_ID:
        print("Sahi se month input de bhutni ke!")

    #api call 
    url = "https://api.notion.com/v1/pages"

    # for daily jo kharcha hua uska data
    daily_db_data = {
        "parent" : {"database_id" : DB_ID} ,
        "properties" : {
            "Notes" : {"title": [{"text": {"content": notes}}]} ,
            "Category" : {"select" : {"name" : Category}} ,
            "Amount" : {"number" : Amount},
            "Date": {"date": {"start": today}}
        }
    }
    daily_db_headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28"
    }

    

    try:
        res = requests.post(url , headers=daily_db_headers , json=daily_db_data)
        res.raise_for_status()
    except Exception as e:
        print(f"Error in api call : {e}")
        return 
    
    print(f"Addded Expense to {month} month: {Category} - {Amount} - {today} ✅")



def main():
    print("Welcome to notion expense tracker !\n")
    while True:
        print("1. Add a new expense : \n2. View all the expenses : \n3. Exit the app")
        choice = input("Enter your choice : ").strip()

        match choice:
            case "1":
                add_expense()
            case "2":
                # view_expenses()
                pass
            case "3":
                print("😊 Thankyou for ur visit!")
                break
            case _:
                print("Please enter a valid choice !")

if __name__ == "__main__":
    add_expense()