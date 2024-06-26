from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import matplotlib.pyplot as plt
import os

options = Options()
options.page_load_strategy = 'normal'
options.headless = True

# os.environ['MOZ_HEADLESS'] = '1'

# executable_path=r"C:\geckodriver\geckodriver.exe"

driver = webdriver.Firefox(options=options)

URL = "https://sgo.prim-edu.ru/"


user = {"login": "ГриммеМ", "password": "090508", "organisation": 'МБОУ "СОШ № 6"'}
marks = 0

class Grafic:
    def __init__(self, name: str, table_marks: pd.DataFrame, num_subject: int, f_mounth_name: str, s_mounth_name: str, t_mounth_name: str=None)  -> None:
        self.name = name
        self.table_marks = table_marks
        self.num_subject = num_subject
        self.f_mounth_name = f_mounth_name
        self.s_mounth_name = s_mounth_name
        self.t_mounth_name = t_mounth_name

    def table_filter(self) -> pd.DataFrame:
        subject = pd.Series(self.table_marks.loc[self.num_subject])
        subject = subject[subject.notna()]
        f_mounth = pd.DataFrame(subject.loc[self.f_mounth_name])
        s_mounth = pd.DataFrame(subject.loc[self.s_mounth_name])

        s_mounth = s_mounth.loc[s_mounth[self.num_subject] != 'УП']
        s_mounth = s_mounth.loc[s_mounth[self.num_subject] != 'Н']
        s_mounth = s_mounth[self.num_subject].astype(int)

        f_mounth = f_mounth.loc[f_mounth[self.num_subject] != 'УП']
        f_mounth = f_mounth.loc[f_mounth[self.num_subject] != 'Н']
        f_mounth = f_mounth[self.num_subject].astype(int)

        if self.t_mounth_name != None:
            t_mounth = pd.DataFrame(subject.loc[self.t_mounth_name])
            t_mounth = t_mounth.loc[t_mounth[self.num_subject] != 'УП']
            t_mounth = t_mounth.loc[t_mounth[self.num_subject] != 'Н']
            t_mounth = t_mounth[self.num_subject].astype(int)

            return f_mounth, s_mounth, t_mounth
            
        return f_mounth, s_mounth
    
    def create_grafic(self, f_mounth: pd.DataFrame, s_mounth: pd.DataFrame, t_mounth=None) -> plt.Figure:
        if type(t_mounth) != pd.DataFrame:
            fig, axs = plt.subplots(ncols=2, figsize=(11, 4))

            fig.suptitle(self.name)

            axs[0].plot(f_mounth, marker='o')
            axs[1].plot(s_mounth, marker='o')

            axs[0].grid(True)
            axs[1].grid(True)

            axs[0].set_xlabel(self.f_mounth_name)
            axs[1].set_xlabel(self.s_mounth_name)

            axs[0].set_yticks([2, 3, 4, 5])
            axs[1].set_yticks([2, 3, 4, 5])

            return fig
        
        else:
            fig, axs = plt.subplots(ncols=3, figsize=(11, 4))

            fig.suptitle(self.name)

            axs[0].plot(f_mounth, marker='o')
            axs[1].plot(s_mounth, marker='o')
            axs[2].plot(t_mounth, marker='o')

            axs[0].grid(True)
            axs[1].grid(True)
            axs[2].grid(True)

            axs[0].set_xlabel(self.f_mounth_name)
            axs[1].set_xlabel(self.s_mounth_name)
            axs[2].set_xlabel(self.t_mounth_name)

            axs[0].set_yticks([2, 3, 4, 5])
            axs[1].set_yticks([2, 3, 4, 5])
            axs[2].set_yticks([2, 3, 4, 5])

            return fig
    
    def save_image(self, filename: str, figure: plt.Figure) -> None:
        figure.savefig(filename)


def sign_in(login:str, password:str, organisation:str):

    driver.get(URL)
    print("Получение ссылки: ", URL)
    time.sleep(13)

    login_bar = driver.find_element(By.XPATH, """/html/body/div[1]/ng-view/main/div/div[3]/div[4]/input""")
    login_bar.send_keys(login)
    print("Введение Логина: ", login)
    time.sleep(0.5)
    
    password_bar = driver.find_element(By.XPATH, """/html/body/div[1]/ng-view/main/div/div[3]/div[5]/input""")
    password_bar.send_keys(password)
    print("Введение Пароля: ", password)
    time.sleep(0.5)

    if organisation != 'МБОУ "СОШ № 6"':
        return "Извините но мы работает только с оценками школы номер 6 в посёлке Новом."
    else:
        org = 'МБОУ "СОШ № 6"'
        org_search_bar = driver.find_element(By.XPATH, """/html/body/div[1]/ng-view/main/div/div[3]/div[3]/div/span/span[1]/span""")
        org_search_bar.click()
        time.sleep(3)

        org_serch_bar_ch = driver.find_element(By.XPATH, """/html/body/span/span/span[1]/input""")
        org_serch_bar_ch.send_keys(org)

        time.sleep(3)

        org_serch_org = driver.find_element(By.XPATH, """/html/body/span/span/span[2]/ul/li[12]""")
        org_serch_org.click()

        print("Выбор организации: ", organisation)

        time.sleep(2)

        enter_but = driver.find_element(By.XPATH, """/html/body/div[1]/ng-view/main/div/div[3]/div[7]""")
        enter_but.click()

        time.sleep(10)

def con(quarter: int):

    try:
        continue_button = driver.find_element(By.XPATH, """/html/body/div[3]/div/div/ns-modal/div/div[3]/div/div/button""")
        continue_button.click()

        print("Продолжение было")

        time.sleep(7)

    except Exception:
        print("Продолжения не было.")

        time.sleep(7)

    finally:
        otchet_but = driver.find_element(By.XPATH, """//html/body/app-component/div[1]/div[3]/div/app-menu/nav/ul/li[3]/a""")
        otchet_but.click()

        print("Выбор отчёта")
    
    time.sleep(2)

    otchet_pos_but = driver.find_element(By.XPATH, """/html/body/app-component/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[7]/td[2]/a""")
    otchet_pos_but.click()

    time.sleep(7)

    match quarter:
        case 1:
            quarter_but = driver.find_element(By.XPATH, """/html/body/app-component/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/form/div/filter-panel/div[3]/div/select/option[2]""")
        case 2:
            quarter_but = driver.find_element(By.XPATH, """/html/body/app-component/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/form/div/filter-panel/div[3]/div/select/option[3]""")

        case 3:
            quarter_but = driver.find_element(By.XPATH, """/html/body/app-component/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/form/div/filter-panel/div[3]/div/select/option[4]""")

        case 4:
            quarter_but = driver.find_element(By.XPATH, """/html/body/app-component/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/form/div/filter-panel/div[3]/div/select/option[5]""")

        case _:
            raise ValueError("Invalid Data")
    
    quarter_but.click()
    print("Выбор четверти: ", quarter)

def table_parcer():
    time.sleep(2)
    form_but = driver.find_element(By.XPATH, """/html/body/app-component/div[2]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/button[1]""")
    form_but.click()

    print("Парсинг таблицы")

    time.sleep(15)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one(".table-print")

    marks = pd.read_html(str(table))
    marks = pd.DataFrame(marks[0])

    print("Вывод оценок")

    return marks
    # marks.to_csv('marks.csv')

    # table = driver.find_element(By.XPATH, """/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div/div/table[2]""")

if __name__ == "__main__":
    sign_in(user["login"], user["password"], user["organisation"])
    con(2)
    grf = Grafic(name = 'Оценки по Физике за II четверть', table_marks=table_parcer(), num_subject=10, f_mounth_name='Ноябрь', s_mounth_name='Декабрь')
    f, s = grf.table_filter()
    grf.save_image(filename='grf2.png', figure=grf.create_grafic(f, s))