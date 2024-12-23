# Напишите программу, с помощью которой можно искать информацию на Википедии с помощью консоли.
# 1. Спрашивать у пользователя первоначальный запрос.
# 2. Переходить по первоначальному запросу в Википедии.
# 3. Предлагать пользователю три варианта действий:
# листать параграфы текущей статьи;
# перейти на одну из связанных страниц — и снова выбор из двух пунктов:
# - листать параграфы статьи;
# - перейти на одну из внутренних статей.
# выйти из программы.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def start_browser():
    """Инициализация браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def search_wikipedia(browser, query):
    """Открыть страницу Википедии по запросу."""
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    browser.get(url)
    if "по запросу отсутствуют статьи" in browser.page_source:
        return False
    return True

def get_paragraphs(browser):
    """Получить список параграфов текущей статьи."""
    # paragraphs = browser.find_elements(By.XPATH, "//div[@class='mw-parser-output']/p")
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    return [p.text for p in paragraphs if p.text.strip()]

def get_links(browser):
    """Получить список связанных ссылок."""
    # links = browser.find_elements(By.XPATH, "//div[@class='mw-parser-output']//a[@href]")
    links = {}
    for element in browser.find_elements(By.TAG_NAME, "div"):
        # Чтобы искать атрибут класса
        cl = element.get_attribute("class")
        if cl == "hatnote navigation-not-searchable ts-main":
            link = element.find_element(By.TAG_NAME, "a")
            links[link.get_attribute("title")] = link.get_attribute("href")
    #return {link.text: link.get_attribute('href') for link in links if link.text.strip()}
    # return {link.text: link for link in links if link.text.strip()}
    return links

def main():
    print("Добро пожаловать в консольный поиск по Википедии с Selenium!")
    browser = start_browser()

    try:
        query = input("Введите начальный запрос: ")
        if not search_wikipedia(browser, query):
            print("Статья не найдена. Попробуйте другой запрос.")
            return

        print(f"\nВы открыли статью: {browser.title}\n")
        paragraphs = get_paragraphs(browser)
        paragraph_index = 0

        while True:
            print("\nДоступные действия:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на связанную страницу")
            print("3. Выйти из программы")
            choice = input("\nВаш выбор: ")

            if choice == '1':  # Листать параграфы
                if paragraph_index < len(paragraphs):
                    print(f"\n{paragraphs[paragraph_index]}\n")
                    paragraph_index += 1
                else:
                    print("Это последний параграф.")
                    paragraph_index = 0

            elif choice == '2':  # Перейти на связанную страницу
                print("\nСвязанные страницы:")
                links = get_links(browser)
                link_names = list(links.keys())[:10]  # Только первые 10 ссылок

                for i, name in enumerate(link_names, 1):
                    print(f"{i}. {name}")

                link_choice = input("\nВведите номер ссылки или 'назад' для возврата: ")
                if link_choice.isdigit() and 1 <= int(link_choice) <= len(link_names):
                    print(links[link_names[int(link_choice) - 1]])
                    browser.get(links[link_names[int(link_choice) - 1]])
                    print(f"\nВы открыли статью: {browser.title}\n")
                    paragraphs = get_paragraphs(browser)
                    paragraph_index = 0
                elif link_choice.lower() == 'назад':
                    continue
                else:
                    print("Неверный ввод.")

            elif choice == '3':  # Выйти
                print("До свидания!")
                break

            else:
                print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")

    finally:
        browser.quit()

if __name__ == "__main__":
    main()