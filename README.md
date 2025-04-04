# Сферум Рассыльщик `Sferum Sendler`

Этот проект - небольшой рассыльщик для Сферума с простым графическим интерфейсом.

## Зачем это нужно?

Если Вам нужно набить сообщения в чаты Сферума или, например, напомнить коллегам про активность.

## Функционал

- Ввод cookie для определения пользователя, от чьего имени будут отправляться сообщения.
- Ввод текста сообщения
- Ввод ID пользователя/ей, которому/ым будет рассылаться сообщение
- Бесконечная отправка сообщения с паузой в 5 секунд с возможностью остановить цикл
- Сохранение введенных данных в `settings.json`, чтобы не вводить заново каждый раз.

Исполняемый файл лежит в папке `dist` — возможность пользоваться программой без python и настройки окружения.

## Как найти значения для полей?

### Cookie
1. Открыть [Сферум](https://web.vk.me/) в браузере.
2. Нажать <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd>.
3. Выбрать "Приложение" → "Хранилище" → "Файлы cookie" → `https://web.vk.me`.
4. Написать в фильтре (или выбрать из списка) `remixdsid` и скопировать значение из столбца "Value". Это и будет Ваш cookie.

### Сообщение
Просто напишите, что хотите отправить. Хоть `"Привет!"`, хоть `"Тест от бота"`.

### Chat IDs
- Открыть чат в Сферуме, а затем адресную строку: `https://web.vk.me/convo/123456789?entrypoint=list_all`. Число `123456789` — это и есть ID чата.
- Ввести ID в поле. Если их несколько, то в поле через запятую, например: `123456789, 987654321`.

Подсказка с картинкой в программе покажет пример, как это выглядит.



## Установка и запуск для тех, кто хочет покопаться в коде

Если вы не просто берёте `.exe`, а хотите запустить через Python или доработать:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Ivadus/Sferum-GUI-Messenger.git
   cd Sferum-GUI-Messenger
   ```

2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите:
   ```bash
   python message_sender.py
   ```


## Сборка в .exe
Исполняемый файл уже есть в `dist/message_sender.exe`. Если хотите собрать сами:

```bash
pyinstaller --onefile --add-data "chat_id_example.png;." --add-data "vk;vk" --hidden-import=PIL --hidden-import=requests --hidden-import=aiogram --windowed --icon=app_icon.ico message_sender.py
```

- `chat_id_example.png` — картинка для подсказки, лежит рядом с кодом.
- `vk/` — папка с логикой для VK API.
- `app_icon.ico` — иконка программы (если нет, уберите `--icon=app_icon.ico`).

## Особенности
- **Запуск**: `.exe` в `dist` работает без Python на любом Windows. На слабых компьютерах может запускаться с задержкой (до минуты) — это PyInstaller распаковывает файлы.
- **Сохранение**: Данные из полей сохраняются в `settings.json` в той же папке, где `.exe`.

## Лицензия
Лицензии нет, берите и пользуйтесь