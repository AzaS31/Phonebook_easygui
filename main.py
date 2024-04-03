import json
import easygui

# Функция для загрузки контактов
def load_contacts():
    try:
        with open("contacts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
# Функция для сохранение контактов
def save_contacts(contacts):
    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False)

# Функция для добавление новых контактов
def add_contact(contacts):
    fields = ["Фамилия", "Имя", "Отчество", "Электронная почта", "Телефон"]
    contact_info = easygui.multenterbox("Введите информацию о контакте:", "Добавление контакта", fields)
    if contact_info is None:  
        return
    contact = dict(zip(fields, contact_info))
    contact['mobile_numbers'] = [contact.pop('Телефон')] 
    contacts.append(contact)
    easygui.msgbox("Контакт успешно добавлен")

# Функция поиска контактов
def search_contact(contacts):
    search_query = easygui.choicebox("Выберите критерий поиска:", "Поиск контакта", ["Имя", "Фамилия", "Электронная почта", "Телефон"])
    if search_query is None:
        return
    
    search_term = easygui.enterbox(f"Введите {search_query.lower()} для поиска:", "Поиск контакта")
    if search_term is None:
        return
    
    found_contacts = []
    for contact in contacts:
        if search_term.lower() in contact.get(search_query, '').lower():
            found_contacts.append(contact)
    
    if found_contacts:
        display_contacts(found_contacts)
    else:
        easygui.msgbox("Контакт не найден.")

# Функция для отображения всех контактов
def display_contacts(contacts):
    contacts_info = "\n".join([f"{contact['Фамилия']} {contact['Имя']} {contact['Отчество']}, email: {contact['Электронная почта']}, телефоны: {', '.join(contact['mobile_numbers'])}" for contact in contacts])
    easygui.textbox("Все контакты:", "Контакты", contacts_info)

# Функция для измения контактов
def change_contact(contacts):
    if not contacts:
        easygui.msgbox("Список контактов пуст.")
        return
    
    search_query = easygui.choicebox("Выберите критерий поиска:", "Поиск контакта", ["Имя", "Фамилия", "Электронная почта", "Телефон"])
    if search_query is None:
        return
    
    search_term = easygui.enterbox(f"Введите {search_query.lower()} для поиска:", "Поиск контакта")
    if search_term is None:
        return
    
    found_contacts = []
    for contact in contacts:
        if search_term.lower() in contact.get(search_query, '').lower():
            found_contacts.append(contact)
    
    if not found_contacts:
        easygui.msgbox("Контакт не найден.")
        return
    
    chosen_contact_names = [f"{contact['Фамилия']} {contact['Имя']} {contact['Отчество']}" for contact in found_contacts]
    
    if len(chosen_contact_names) == 1:
        easygui.msgbox("Найден только один контакт.")
        chosen_contact_info = found_contacts[0]
    else:
        chosen_contact_name = easygui.choicebox("Выберите контакт для изменения:", "Изменение контакта", chosen_contact_names)
        if chosen_contact_name is None:
            return
        chosen_index = chosen_contact_names.index(chosen_contact_name)
        chosen_contact_info = found_contacts[chosen_index]
    
    fields = ["Фамилия", "Имя", "Отчество", "Электронная почта", "Телефон"]
    
    values = list(chosen_contact_info.values())
    
    updated_info = easygui.multenterbox("Введите новую информацию о контакте:", "Изменение контакта", fields, values)
    if updated_info is None:
        return
    
    index_in_contacts = contacts.index(chosen_contact_info)
    
    contacts[index_in_contacts].update(dict(zip(fields, updated_info)))
    contacts[index_in_contacts]['mobile_numbers'] = [contacts[index_in_contacts].pop('Телефон')]
    
    easygui.msgbox("Контакт успешно изменен.")

# Функция для удаления контактов
def remove_contact(contacts):
    if not contacts:
        easygui.msgbox("Список контактов пуст.")
        return
    
    search_query = easygui.choicebox("Выберите критерий поиска:", "Поиск контакта", ["Имя", "Фамилия", "Электронная почта", "Телефон"])
    if search_query is None:
        return
    
    search_term = easygui.enterbox(f"Введите {search_query.lower()} для поиска:", "Поиск контакта")
    if search_term is None:
        return
    
    found_contacts = []
    for contact in contacts:
        if search_term.lower() in contact.get(search_query, '').lower():
            found_contacts.append(contact)
    
    if not found_contacts:
        easygui.msgbox("Контакт не найден.")
        return
    
    chosen_contact_names = [f"{contact['Фамилия']} {contact['Имя']} {contact['Отчество']}" for contact in found_contacts]
    
    if len(chosen_contact_names) == 1:
        easygui.msgbox("Найден только один контакт.")
        chosen_contact_info = found_contacts[0]
    else:
        chosen_contact_name = easygui.choicebox("Выберите контакт для удаления:", "Удаление контакта", chosen_contact_names)
        if chosen_contact_name is None:
            return
        chosen_index = chosen_contact_names.index(chosen_contact_name)
        chosen_contact_info = found_contacts[chosen_index]
    
    index_in_contacts = contacts.index(chosen_contact_info)
    
    del contacts[index_in_contacts]
    
    easygui.msgbox("Контакт успешно удален.")


def main():
    contacts = load_contacts()  

    choices = ["Добавить контакт", "Найти контакт", "Показать все контакты", "Изменить контакт", "Удалить контакт", "Выход"]
    while True:
        choice = easygui.choicebox("Выберите действие:", "Управление контактами", choices)
        if choice == "Добавить контакт":
            add_contact(contacts)
        elif choice == "Найти контакт":
            search_contact(contacts)    
        elif choice == "Показать все контакты":
            display_contacts(contacts)
        elif choice == "Изменить контакт":
            change_contact(contacts)
        elif choice == "Удалить контакт":
            remove_contact(contacts)  
        elif choice == "Выход":
            break
        save_contacts(contacts)

main()
