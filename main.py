import datetime
import re

class Birthday(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        if not re.fullmatch(r"\d{2}.\d{2}.\d{4}", value):
            raise ValueError("Birthday must be in DD.MM.YYYY format.")
        # Додаткова перевірка правильності дати (наприклад, щоб не було 31.02)
        try:
            datetime.datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date.")

class Record:
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must have 10 digits.")
        super().__init__(value)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return self.birthday.value if hasattr(self, 'birthday') else "Birthday not set."

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.datetime.today()
        one_week = today + datetime.timedelta(days=7)
        birthdays = []
        for record in self.data.values():
            if hasattr(record, 'birthday'):
                birthday_date = datetime.datetime.strptime(record.birthday.value, "%d.%m.%Y")
                birthday_this_year = birthday_date.replace(year=today.year)
                if today <= birthday_this_year < one_week:
                    birthdays.append(record.name.value)
        return birthdays

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        elif command == "add-birthday":
            name, birthday = args
            record = book.find(name)
            if record:
                record.add_birthday(birthday)
                print(f"Birthday added for {name}")
            else:
                print(f"No contact found for {name}")

        elif command == "show-birthday":
            name = args[0]
            record = book.find(name)
            if record:
                print(record.show_birthday())
            else:
                print(f"No contact found for {name}")

        elif command == "birthdays":
            for name in book.get_birthdays_per_week():
                print(f"Congratulate {name} this week!")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
