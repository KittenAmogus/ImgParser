import os
from threading import Thread
from termcolor import cprint, colored
from time import sleep as wt
from requests import get
from bs4 import BeautifulSoup as Sup
from fake_useragent import UserAgent as Agent
ua = Agent()


def flush():

    if not os.path.exists('images'):
        os.mkdir('images')

    for i in os.listdir('images'):
        os.remove('images/' + i)


def get_all_images(url):
    headers = {'user-agent': ua.random}

    try:
        html = get(url, headers=headers).content
    except Exception as e:
        print(colored(e, 'red'))
        quit(print(0 * input('Для выхода нажмите ENTER...\n')))
    if not html:
        return False
    sup = Sup(html, 'lxml')
    image_c = sup.find_all('img')

    clear_imgs = []

    for i in image_c:
        if not i.get('src'):
            continue
        clear_imgs.append(i.get('src'))

    return clear_imgs


def load_an_img(src: str, na):

    if not src.startswith('http'):
        src = global_url + src

    headers = {'user-agent': ua.random}

    byts = get(src, headers=headers).content

    if not byts:
        return False

    with open(f'images/img_{na}.png', 'wb') as img:
        img.write(byts)
        img.close()

    return True


def load_an_image_thread(chunk, zid, self_name):
    try:
        file_id = zid + 1

        for src in chunk:
            load_an_img(src, file_id)
            file_id += 1

        print(f'Я, {self_name}, работу закончил)')
    except Exception as ex:
        print(f'Я, {self_name}, потерялся по пути со словами: "{colored(ex, "cyan")}"')
    global working
    working -= 1


def load(url):
    flush()
    images = get_all_images(url)

    if input('Вывести ссылки на картинки? (Y/n): ') == 'Y':
        for image_src in images:

            if not image_src.startswith('http'):
                image_src = url + image_src
            print(f'Найдена картинка | {colored(image_src, "yellow")}')
            wt(0.01)
    print('------------')
    print(f'Найдено картинок: {len(images)}' if len(images) != 0
          else f'Я картинок не нашел, поищи сам: {colored(url, "yellow")}')
    if len(images) == 0:
        quit(print(0 * input('Для выхода нажмите ENTER...\n')))

    chunk_size = input('Сколько картинок на поток? (если не знаешь что это - жми ENTER): ')

    if chunk_size in ['', ' ', '\n']:
        chunk_size = 10
    else:
        try:
            chunk_size = int(chunk_size)
        except ValueError or TypeError or Exception:
            chunk_size = 10

    chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]  # Эти две строчки списаны :(

    threads_ = []

    normalize = 0

    print('\nНачинаем работу, потоки!!!!\n-------')

    for chunk in chunks:
        name = colored('Крутой Поток номер ' + str(chunks.index(chunk) + 1), "green")
        threads_.append(Thread(target=load_an_image_thread, args=(chunk, normalize, name), name=name))
        normalize += chunk_size

    return threads_


for line in colored(
    """

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣉⣁⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠉⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⣿⡟⠛⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣾⡿⠛⢿⣇⠀⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⢀⣿⠇⠀⠈⠻⢿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⡿⠋⠀⠀⢸⣿⡇⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⢿⣿⣿⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣶⣿⣿⠟⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣀⣀⡀⠀⠀⢸⣿⣷⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠁⠀⠀⠀⠀⠀⠀⢸⣿⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠉⠁⠀⠀⠉⠙⠻⣶⣸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⢸⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿
⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⣠⡶⠶⣶⣤⡀⠀⠀⠀⠀⠀⠘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⠛⣷⣶⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢰⣿⣷⣶⣿⣿⢿⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿
⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣄⠙⠿⠿⢏⣿⡿⠟⠀⠀⠀⠀⠀⠘⣟⠻⠿⠿⢁⠞⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿
⣿⣿⡇⠀⠀⠀⠀⠀⠀⠴⠶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⠶⠖⠊⠁⠀⠀⣤⣤⣤⣤⠀⠀⠀⠀⠒⠂⠉⠀⠀⠀⠀⠀⠴⢶⣿⡿⠶⠄⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿
⣿⣿⣷⡆⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠁⠀⠀⠀⠀⠈⠙⡟⠁⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠉⠉⢉⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻⣿⣿⣿⣿⡇⠐⠒⠀⠀⠀⠀⠀⣀⣠⡴⠷⣄⣀⡄⠀⠀⠀⠀⠀⠒⠂⠠⣴⣿⣿⡟⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣿⣤⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⡟⠉⠀⣀⣤⣦⣤⣤⣀⠀⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⠛⠉⠻⠿⢶⣦⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣶⡾⠿⠛⠉⢻⣷⣄⣴⣿⣿⡟⣿⣿⣿⡇⠀⠀⠀⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠉⠉⠛⠛⠛⠿⠿⠿⠿⠿⠿⠛⠛⠛⠉⠁⠀⠀⠀⢰⣿⣿⣿⣿⣿⠿⠟⠿⠿⠟⠃⠀⢀⣸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣧⡄⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⢸⣿⡆⠀⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠈⣿⣷⡄⢸⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⢰⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠹⣿⣿⣦⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⣀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣆⡀⠀⠀⠉⠙⠛⠻⠿⠿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⡿⠿⠿⠟⠛⠋⠉⠀⠀⠀⣰⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⣀⡀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣄⣀⣀⠀⠈⠻⣿⣿⣿⡿⠁⠀⢀⣀⣀⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠈⠻⠟⠀⢀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

    """, "green"
).splitlines():
    print(line)
    wt(0.1)

print('-------------------')

global_url = input('url: ').removesuffix('/')

threads = load(global_url)

working = 0

for thread in threads:
    thread.start()
    working += 1
    print(f'{thread.name} начал работу')

print('------------------------------\n')


while True:
    if working == 0:
        break
    wt(0.05)

print('------------------\n\nРабота окончена, нажмите ENTER для просмотра...\n')

from viewer import Viewer
Viewer().run()
