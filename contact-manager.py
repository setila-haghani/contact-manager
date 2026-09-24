import json
import re
from colorama import init, Fore

init(autoreset=True)

FILE_NAME = "contacts.json"
contacts = []

# colors
PRIMARY = Fore.CYAN
SUCCESS = Fore.GREEN
ERROR = Fore.RED
WARNING = Fore.YELLOW
TEXT = Fore.WHITE
MUTED = Fore.LIGHTBLACK_EX


def line(char="─", length=50):
    return char * length


def header(title, subtitle=""):
    print()
    print(PRIMARY + "╭" + line() + "╮")
    print(PRIMARY + "│" + title.center(50) + "│")

    if subtitle:
        print(MUTED + "│" + subtitle.center(50) + "│")

    print(PRIMARY + "╰" + line() + "╯")


def success(message):
    print(SUCCESS + f"  ✓ {message}")


def error(message):
    print(ERROR + f"  ✕ {message}")


def warning(message):
    print(WARNING + f"  ! {message}")


# check email
def valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# check phone number
def valid_phone(phone):
    return phone.isdigit() and 10 <= len(phone) <= 15


def full_name(contact):
    return f"{contact['first_name']} {contact['last_name']}"


def find_contact_index(first_name, last_name):
    target = f"{first_name} {last_name}".lower()

    for i, contact in enumerate(contacts):
        if full_name(contact).lower() == target:
            return i

    return -1


# add a new contact
def add_contact():
    header("ADD CONTACT")

    first_name = input("  First name  › ").strip()
    last_name = input("  Last name   › ").strip()

    if not first_name or not last_name:
        error("Name cannot be empty.")
        return

    email = input("  Email       › ").strip()

    if not valid_email(email):
        error("Invalid email address.")
        return

    phone = input("  Phone       › ").strip()

    if not valid_phone(phone):
        error("Invalid phone number.")
        return

    if find_contact_index(first_name, last_name) != -1:
        error("This contact already exists.")
        return

    contact = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone
    }

    contacts.append(contact)
    sort_contacts()

    success("Contact added successfully.")


# sort contacts by name
def sort_contacts():
    contacts.sort(
        key=lambda contact: (
            contact["first_name"].lower(),
            contact["last_name"].lower()
        )
    )


# show all contacts
def show_contacts():
    if not contacts:
        warning("No contacts found.")
        return

    sort_contacts()

    header("CONTACTS", f"{len(contacts)} contact(s)")

    for i, contact in enumerate(contacts, start=1):
        print()
        print(PRIMARY + f"  {i:02}  " + TEXT + full_name(contact))
        print(MUTED + f"       Email   {contact['email']}")
        print(MUTED + f"       Phone   {contact['phone']}")

    print()
    print(MUTED + line())


# search using binary search
def search_contact():
    if not contacts:
        warning("No contacts found.")
        return

    sort_contacts()

    header("SEARCH CONTACT")

    target = input("  Full name   › ").strip().lower()

    left = 0
    right = len(contacts) - 1

    while left <= right:
        middle = (left + right) // 2
        current_name = full_name(contacts[middle]).lower()

        if current_name == target:
            contact = contacts[middle]

            print()
            print(PRIMARY + "╭" + line() + "╮")
            print(PRIMARY + "│" + "CONTACT FOUND".center(50) + "│")
            print(PRIMARY + "├" + line() + "┤")

            print(TEXT + f"│  Name      {full_name(contact):<37}│")
            print(TEXT + f"│  Email     {contact['email']:<37}│")
            print(TEXT + f"│  Phone     {contact['phone']:<37}│")

            print(PRIMARY + "╰" + line() + "╯")

            return

        elif target < current_name:
            right = middle - 1

        else:
            left = middle + 1

    error("Contact not found.")


# edit an existing contact
def edit_contact():
    if not contacts:
        warning("No contacts found.")
        return

    header("EDIT CONTACT")

    first_name = input("  Current first name › ").strip()
    last_name = input("  Current last name  › ").strip()

    index = find_contact_index(first_name, last_name)

    if index == -1:
        error("Contact not found.")
        return

    contact = contacts[index]

    print()
    print(MUTED + "  Press Enter to keep the current value.")
    print()

    new_first = input(
        f"  First name [{contact['first_name']}] › "
    ).strip()

    new_last = input(
        f"  Last name  [{contact['last_name']}] › "
    ).strip()

    new_email = input(
        f"  Email      [{contact['email']}] › "
    ).strip()

    new_phone = input(
        f"  Phone      [{contact['phone']}] › "
    ).strip()

    if new_first:
        contact["first_name"] = new_first

    if new_last:
        contact["last_name"] = new_last

    if new_email:
        if not valid_email(new_email):
            error("Invalid email. Changes cancelled.")
            return

        contact["email"] = new_email

    if new_phone:
        if not valid_phone(new_phone):
            error("Invalid phone number. Changes cancelled.")
            return

        contact["phone"] = new_phone

    sort_contacts()

    success("Contact updated successfully.")


# delete a contact
def delete_contact():
    if not contacts:
        warning("No contacts found.")
        return

    header("DELETE CONTACT")

    first_name = input("  First name › ").strip()
    last_name = input("  Last name  › ").strip()

    index = find_contact_index(first_name, last_name)

    if index == -1:
        error("Contact not found.")
        return

    contact = contacts[index]

    print()
    print(WARNING + f"  You are deleting: {full_name(contact)}")

    confirm = input("  Confirm (y/n) › ").strip().lower()

    if confirm == "y":
        contacts.pop(index)
        success("Contact deleted.")
    else:
        warning("Deletion cancelled.")


# save contacts to json
def save_contacts():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(
                contacts,
                file,
                ensure_ascii=False,
                indent=4
            )

    except OSError:
        error("Could not save contacts.")


# load contacts when program starts
def load_contacts():
    global contacts

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            contacts = json.load(file)

    except FileNotFoundError:
        contacts = []

    except (json.JSONDecodeError, OSError):
        warning("Could not load contacts.")
        contacts = []


# main menu
def menu():
    while True:
        print()
        print(PRIMARY + "╭" + line() + "╮")
        print(PRIMARY + "│" + "CONTACT MANAGER".center(50) + "│")
        print(MUTED + "│" + "Personal Contact Database".center(50) + "│")
        print(PRIMARY + "╰" + line() + "╯")

        print()
        print(TEXT + "  01   Add contact")
        print(TEXT + "  02   Search contact")
        print(TEXT + "  03   Edit contact")
        print(TEXT + "  04   Delete contact")
        print(TEXT + "  05   View contacts")
        print(TEXT + "  06   Save changes")
        print(MUTED + "  00   Exit")

        print()
        print(MUTED + line())

        choice = input(
            PRIMARY + "  Select an option › "
        ).strip()

        if choice == "1":
            add_contact()

        elif choice == "2":
            search_contact()

        elif choice == "3":
            edit_contact()

        elif choice == "4":
            delete_contact()

        elif choice == "5":
            show_contacts()

        elif choice == "6":
            save_contacts()
            success("Changes saved.")

        elif choice == "0":
            save_contacts()
            print()
            print(MUTED + "  Session closed.")
            break

        else:
            error("Invalid option.")


load_contacts()
menu()