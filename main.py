"""
To Do List

- Второй режим (жёсткого) тестирования (Done)
- Выравнивание логотипа по колонке (Done)
- Настройка переспрашивания
- Смена местами вопроса и ответа (Done)
- Количество оставшихся вопросов (Done)

Bugs:

- Кнопка домой - сбрасываются настройки (Fixed)

"""

import flet as ft
import time
from quiz import *
from random import choice, shuffle


file_path: str = ""
separator: str = "  -  "
reversing: bool = False
register_check: bool = False
duration_user: int = 2000
wrongs: int = 0
editing: str = ""
selection: str = ""

def main(page: ft.Page):

    # Изначальные настройки окна и переменных

    maincolor = "#9041c4"
    textcolor = "#7836a3"
    backgroundcolor = "#e0bcf7"

    page.window_width = 1200 # 1000
    page.window_height = 780 # 700
    page.window_min_width = 900
    page.window_min_height = 600
    page.window_resizable = True
    page.theme = ft.theme.Theme(color_scheme_seed=maincolor)
    page.theme_mode = ft.ThemeMode.DARK  # Тёмная тема насильно
    page.title = "OpenQuizz"
    page.update()

    page.fonts = {
        "Cuprum": "/fonts/Cuprum.ttf"
    }

    def editing(e):

        page.title = "OpenQuizz - Редактирование"
        task = separate_file(file_path, separator, reversing)

        def home(e):
            starting_window()

        def save(e):
            with open(file_path, "w") as f:
                f.truncate(0)
                for i in table.rows:
                    add = i.cells[0].content.value
                    f.write(f"{add}{separator}{task[add]}\n")
            starting_window()

        cancel_button = ft.IconButton(
            icon=ft.icons.HOME,
            icon_color=maincolor,
            bgcolor=backgroundcolor,
            on_click=home
        )

        save_file_button = ft.ElevatedButton(
            text="Сохранить и выйти",
            icon=ft.icons.SAVE,
            icon_color=maincolor,
            bgcolor=backgroundcolor,
            color=textcolor,
            on_click=save,
            expand=1
        )

        question_field = ft.TextField(
            label=f"Вопрос"
        )

        answer_field = ft.TextField(
            label=f"Ответ"
        )

        add_question_field = ft.TextField(
            label=f"Вопрос"
        )

        add_answer_field = ft.TextField(
            label=f"Ответ"
        )

        def close_edit_dlg_save(e):
            global editing
            edit_dlg.open = False
            task.pop(editing)
            task[question_field.value] = answer_field.value
            refresh_table()
            page.update()

        def close_edit_dlg_delete(e):
            global editing
            edit_dlg.open = False
            task.pop(editing)
            refresh_table()
            page.update()

        def close_edit_dlg_no_save(e):
            edit_dlg.open = False
            page.update()

        def close_add_dlg(e):
            add_dlg.open = False
            page.update()

        def close_add_dlg_save(e):
            add_dlg.open = False
            task[add_question_field.value] = add_answer_field.value
            refresh_table()
            add_question_field.value = ""
            add_answer_field.value = ""
            page.update()

        def change(e):
            question_field.value, answer_field.value = answer_field.value, question_field.value
            page.update()

        change_button = ft.IconButton(
            icon=ft.icons.COMPARE_ARROWS,
            icon_color=maincolor,
            bgcolor=backgroundcolor,
            on_click=change
        )

        edit_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование"),
            content=ft.Column(
                [
                    question_field,
                    ft.Row(
                        [
                            ft.Container(expand=1),
                            change_button,
                            ft.Container(expand=1),
                        ]
                    ),
                    answer_field
                ],
                height=page.window_height//4,
                width=page.window_width//2
            ),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=1),
                        ft.ElevatedButton(text="Сохранить", bgcolor="green", color="white",
                                          on_click=close_edit_dlg_save),
                        ft.ElevatedButton(text="Отменить", on_click=close_edit_dlg_no_save),
                        ft.ElevatedButton(text="Удалить", bgcolor="red", color="white", on_click=close_edit_dlg_delete),
                        ft.Container(expand=1)
                    ]
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        add_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавление"),
            content=ft.Column(
                [
                    add_question_field,
                    add_answer_field
                ],
                height=page.window_height // 4,
                width=page.window_width // 2
            ),
            actions=[
                ft.Row(
                    [
                        ft.Container(expand=1),
                        ft.ElevatedButton(text="Сохранить", bgcolor="green", color="white",
                                          on_click=close_add_dlg_save),
                        ft.ElevatedButton(text="Отменить", on_click=close_add_dlg),
                        ft.Container(expand=1)
                    ]
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def open_edit_dlg(e):
            global editing
            page.dialog = edit_dlg
            editing = str(e.control.content.value)
            question_field.value = editing
            answer_field.value = task[editing]
            edit_dlg.open = True
            page.update()

        def add(e):
            page.dialog = add_dlg
            add_dlg.open = True
            page.update()


        page.clean()
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Вопрос", size=25, text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Ответ", size=25, text_align=ft.TextAlign.CENTER)),
            ],
            expand=True
        )

        def refresh_table():
            table.rows = []
            for element in sorted(task):
                table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(element, size=15), on_tap=open_edit_dlg),
                            ft.DataCell(ft.Text(task[element], size=15))
                        ]
                    )
                )

        add_button = ft.IconButton(
            icon=ft.icons.ADD,
            icon_color="white",
            bgcolor="green",
            on_click=add
        )

        refresh_table()
        preview = ft.ListView(expand=True, controls=[table])
        page.add(preview)
        page.add(
            ft.Row(
                [
                    cancel_button,
                    save_file_button,
                    add_button
                ]
            )
        )

    # Мягкое тестирование

    def test_start(e):
        page.title = "OpenQuizz - Тест"
        page.clean()
        global answer1, answer2, answer3, answer4, wrongs, button1_text, button2_text, button3_text, button4_text


        # Наполнение ответов и проверка

        task = separate_file(file_path, separator, reversing)
        start_time = time.time()
        wrongs = 0
        questions = list(task.keys())
        remain_questions = list(task.keys())
        points = len(questions)

        counter = ft.Text(
            size=10,
            color="grey",
            value=f"{points}/{points}"
        )

        def check_button1(e):
            check(button1_text.value)

        def check_button2(e):
            check(button2_text.value)

        def check_button3(e):
            check(button3_text.value)

        def check_button4(e):
            check(button4_text.value)

        button1_text = ft.Text(
            value="test",
            size=15,
            color="white"
        )

        button2_text = ft.Text(
            value="test",
            size=15,
            color="white"
        )

        button3_text = ft.Text(
            value="test",
            size=15,
            color="white"
        )

        button4_text = ft.Text(
            value="test",
            size=15,
            color="white"
        )

        answer1 = ft.OutlinedButton(content=button1_text, expand=12, on_click=check_button1, height=100)
        answer2 = ft.OutlinedButton(content=button2_text, expand=12, on_click=check_button2, height=100)
        answer3 = ft.OutlinedButton(content=button3_text, expand=12, on_click=check_button3, height=100)
        answer4 = ft.OutlinedButton(content=button4_text, expand=12, on_click=check_button4, height=100)

        answ = ft.Column(
            [
                ft.Row(
            [
                        ft.Container(expand=1),
                        answer1,
                        ft.Container(expand=1),
                        answer2,
                        ft.Container(expand=1),
                    ],
                    expand=2
                ),
                   ft.Row(
            [
                        ft.Container(expand=1),
                        answer3,
                        ft.Container(expand=1),
                        answer4,
                        ft.Container(expand=1),
                    ],
                    expand=2
                ),
                ft.Container(expand=1)
            ],
            expand=1
        )

        question_text = ft.Text(
            'text',
            size=35,
            expand=20,
            text_align=ft.TextAlign.CENTER
        )

        quest = ft.Column(
            [
                ft.Container(expand=1),
                ft.Row(
                    [
                        ft.Container(expand=1),
                        question_text,
                        ft.Container(expand=1)
                    ]
                ),
                ft.Container(expand=1)
            ],
            expand=1
        )

        def check(answer:str):
            global wrongs

            current_question=question_text.value
            current_answer=task[current_question]

            if answer == current_answer and len(remain_questions) != 0:
                remain_questions.remove(current_question)
                counter.value = f"{len(remain_questions)}/{points}"
                page.snack_bar = ft.SnackBar(
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.Text(
                                f"Правильно",
                                color="green",
                                size=15
                            ),
                            ft.Container(expand=True)
                        ]
                    ),
                    duration=duration_user,
                    bgcolor="#1D1B1E",
                    open=True,
                    behavior=ft.SnackBarBehavior.FLOATING,
                    elevation=0,
                    width=page.window_width - 100,
                )
                page.snack_bar.open = True

            else:
                page.snack_bar = ft.SnackBar(
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.Text(
                                f"Неправильно. Правильный ответ: {current_answer}",
                                color="red",
                                size=15
                            ),
                            ft.Container(expand=True)
                        ]
                    ),
                    duration=duration_user,
                    bgcolor="#1D1B1E",
                    open=True,
                    behavior=ft.SnackBarBehavior.FLOATING,
                    elevation=0,
                    width=page.window_width - 100,

                )
                page.snack_bar.open = True
                wrongs += 1

            if len(remain_questions) == 0:
                page.snack_bar.visible = False
                timing = round(time.time() - start_time, 0)
                minutes = timing // 60
                seconds = timing - minutes * 60
                page.clean()
                page.add(
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.Text("Статистика", size=45),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("Время выполнения", size=30)),
                                    ft.DataColumn(ft.Text(f"{int(minutes)} мин {int(seconds)} сек", size=25))
                                ],
                                rows=[
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Изучено", size=30)),
                                            ft.DataCell(ft.Text(f"{len(questions)}", size=25)),
                                        ]
                                    ),
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Ошибок", size=30)),
                                            ft.DataCell(ft.Text(f"{wrongs}", size=25)),
                                        ]
                                    )
                                ]
                            ),
                            ft.Container(expand=True),
                        ]
                    ),
                    ft.Container(expand=True)
                )

            if len(remain_questions) != 0:
                current_question = choice(remain_questions)
                current_answer = task[current_question]
                answers = [current_answer]

                while len(answers) < 4:
                    tmp = task[choice(questions)]
                    if tmp not in answers:
                        answers.append(tmp)
                shuffle(answers)

                question_text.value = current_question

                for ans in range(1, 5):
                    exec(f"button{ans}_text.value = '{answers[ans - 1]}'")
                page.update()

        # Инициализация

        current_question = choice(remain_questions)
        current_answer = task[current_question]
        answers = [current_answer]

        while len(answers) < 4:
            tmp = task[choice(questions)]
            if tmp not in answers:
                answers.append(tmp)
        shuffle(answers)

        question_text.value = current_question

        for ans in range(1,5):
            exec(f"button{ans}_text.value = '{answers[ans - 1]}'")

        page.add(quest)
        page.add(answ)
        page.add(
            ft.Row(
                [
                    ft.Container(expand=1),
                    counter
                ]
            )
        )

    # Жёсткое тестирование

    def exam_start(e):
        page.title = "OpenQuizz - Экзамен"
        global wrongs
        page.clean()

        start_time = time.time()
        wrongs = 0
        task = separate_file(file_path, separator, reversing)

        questions = list(task.keys())
        points = len(questions)

        question_text = ft.Text(
            choice(questions),
            size=20,
            expand=True,
            text_align=ft.TextAlign.CENTER
        )

        answer_input = ft.TextField(
            label="Ответ",
            text_align=ft.TextAlign.CENTER,
            expand=True,
            border=ft.InputBorder.OUTLINE,
            autofocus=True
        )

        counter = ft.Text(
            size=10,
            color="grey",
            value=f"{points}/{points}"
        )

        # Проверка ответа на правильность и финальное окно

        def check_answer(e):
            global wrongs, register_check

            inp_ans = answer_input.value.replace(" ", "").replace("\n", "") if register_check \
                else answer_input.value.replace(" ", "").replace("\n", "").lower()
            ans = task[question_text.value].replace(" ", "") if register_check \
                else task[question_text.value].replace(" ", "").lower()

            if inp_ans == ans:

                questions.remove(question_text.value)

                if len(questions) != 0:
                    page.snack_bar = ft.SnackBar(
                        ft.Row(
                            [
                                ft.Container(expand=True),
                                ft.Text(
                                    f"Правильно",
                                    color="green",
                                    size=15
                                ),
                                ft.Container(expand=True)
                            ]
                        ),
                        duration=duration_user,
                        bgcolor="#1D1B1E",
                        open=True,
                        behavior=ft.SnackBarBehavior.FLOATING,
                        elevation=0,
                        width=page.window_width - 100,
                    )

                    current_question = choice(questions)
                    counter.value = f"{len(questions)}/{points}"
                    question_text.value = current_question
                    answer_input.value = ""
                    answer_input.focus()
                    page.update()
                else:
                    page.snack_bar.visible = False
                    timing = round(time.time() - start_time, 0)
                    minutes = timing // 60
                    seconds = timing - minutes * 60
                    page.clean()
                    page.add(
                        ft.Container(expand=True),
                        ft.Row(
                            [
                                ft.Text("Статистика", size=45),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Row(
                            [
                                ft.Container(expand=True),
                                ft.DataTable(
                                    columns=[
                                        ft.DataColumn(ft.Text("Время выполнения", size=30)),
                                        ft.DataColumn(ft.Text(f"{int(minutes)} мин {int(seconds)} сек", size=25))
                                    ],
                                    rows=[
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(ft.Text("Изучено", size=30)),
                                                ft.DataCell(ft.Text(f"{points}", size=25)),
                                            ]
                                        ),
                                        ft.DataRow(
                                            cells=[
                                                ft.DataCell(ft.Text("Ошибок", size=30)),
                                                ft.DataCell(ft.Text(f"{wrongs}", size=25)),
                                            ]
                                        )
                                    ]
                                ),
                                ft.Container(expand=True),
                            ]
                        ),
                        ft.Container(expand=True)

                    )
            else:
                wrongs += 1
                page.snack_bar = ft.SnackBar(
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.Text(
                                f"Неправильно. Правильный ответ: {task[question_text.value]}",
                                color="red",
                                size=15
                            ),
                            ft.Container(expand=True)
                        ]
                    ),
                    duration=duration_user,
                    bgcolor="#1D1B1E",
                    open=True,
                    behavior=ft.SnackBarBehavior.FLOATING,
                    elevation=0,
                    width=page.window_width-100,

                )
                page.snack_bar.duration = duration_user
                page.snack_bar.open = True

                prev_question = question_text.value

                if len(questions) > 1:
                    current_question = choice(questions)
                    while current_question == prev_question:
                        current_question = choice(questions)
                    question_text.value = current_question
                answer_input.value = ""
                answer_input.focus()
                page.update()

        check_button = ft.ElevatedButton(
            text="Проверить",
            icon=ft.icons.CHECK_CIRCLE_OUTLINE,
            icon_color=maincolor,
            color=textcolor,
            bgcolor=backgroundcolor,
            expand=2,
            on_click=check_answer
        )

        # Горячие клавиши

        def shortcut(e: ft.KeyboardEvent):
            if e.key in ["Enter", "Numpad Enter"]:
                check_answer(None)

        page.on_keyboard_event = shortcut

        page.add(ft.Container(expand=True))  # Контейнер, заполняющий пространство

        page.add(
            ft.Row(
                [
                    ft.Container(expand=True),
                    question_text,
                    ft.Container(expand=True)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        page.add(
            ft.Row(
                [
                    answer_input
                ]
            )
        )

        page.add(
            ft.Row(
                [
                    ft.Container(expand=1),
                    check_button,
                    ft.Container(expand=1)
                ]
            )
        )

        page.add(ft.Container(expand=True))  # Контейнер, заполняющий пространство

        page.add(
            ft.Row(
                [
                    ft.Container(expand=1),
                    counter
                ]
            )
        )

    # Окно предпросмотра открытого файла

    def home(e):
        starting_window()

    def preview_start(e):
        page.title = "OpenQuizz - Предпросмотр"
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Вопрос", size=25, text_align=ft.TextAlign.CENTER)),
                ft.DataColumn(ft.Text("Ответ", size=25, text_align=ft.TextAlign.CENTER))
            ],
            expand=True
        )

        cancel_button = ft.IconButton(
            icon=ft.icons.HOME,
            icon_color=maincolor,
            bgcolor=backgroundcolor,
            on_click=home,
        )

        exam_button = ft.ElevatedButton(
            "Экзамен",
            icon=ft.icons.ARROW_FORWARD,
            icon_color=maincolor,
            color=textcolor,
            bgcolor=backgroundcolor,
            on_click=exam_start,
            expand=True
        )

        test_button = ft.ElevatedButton(
            "Тест",
            icon=ft.icons.ARROW_FORWARD,
            icon_color=maincolor,
            color=textcolor,
            bgcolor=backgroundcolor,
            on_click=test_start,
            expand=True,
            visible=False if len(separate_file(file_path, separator, reversing).keys()) < 4 else True
        )

        preview = ft.ListView(expand=True, controls=[table])

        page.clean()
        page.add(preview)
        task = separate_file(file_path, separator, reversing)

        for element in task:
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(element, size=15)),
                        ft.DataCell(ft.Text(task[element], size=15))
                    ]
                )
            )

        page.add(
            ft.Row(
                [
                    cancel_button,
                    test_button,
                    exam_button
                ],
            )
        )

        page.update()

    def starting_window():
        page.title = "OpenQuizz"
        page.clean()

        txt_logo = ft.Container(
        padding=5,
        content=ft.Stack(
            expand=1,
            controls=
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "OpenQuizz",
                            ft.TextStyle(
                                size=150,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color="#E0BCF7",
                                    stroke_width=15,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "OpenQuizz",
                            ft.TextStyle(
                                size=150,
                                weight=ft.FontWeight.BOLD,
                                color="#800080",
                            ),
                        ),
                    ],
                ),
            ]
        ))

        page.add(
            ft.Container(
                ft.Row(
                    [
                        ft.Container(expand=1),
                        txt_logo,
                        ft.Container(expand=1)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                ),
                expand=2
            )
        )

        # Кнопка вызова диалогового окна для выбора файла, содержащего значения теста

        def pick_files_result(e: ft.FilePickerResultEvent):
            global file_path, selection
            file_path = "".join(map(lambda f: f.path, e.files)) if e.files else "Отменено"

            selected_file.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Отменено"
            )

            selection = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Отменено"
            )

            if file_path != "Отменено" and file_check(file_path, separator):
                selected_file.value += " - Выбранный файл"
                selected_file.color = "green"
                start_button.visible = True
                edit_button.visible = True
            elif file_path != "Отменено" and file_empty_check(file_path, separator):
                selected_file.value += " - Выбранный файл"
                selected_file.color = "green"
                edit_button.visible = True
            elif file_path == "Отменено":
                selected_file.value += " - Выберите файл"
                selected_file.color = "blue"
                start_button.visible = False
                edit_button.visible = False
            else:
                selected_file.value += " - Файл не подходит"
                selected_file.color = "red"
                start_button.visible = False
                edit_button.visible = False

            page.update()

        pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        selected_file = ft.Text("")

        page.overlay.append(pick_files_dialog)

        file_choosing_button = ft.ElevatedButton(
            "Выбрать курс",
            icon=ft.icons.UPLOAD_FILE,
            icon_color=maincolor,
            color=textcolor,
            bgcolor=backgroundcolor,
            expand=2,
            on_click=lambda _: pick_files_dialog.pick_files(
                allow_multiple=False,
                allowed_extensions=["txt"],
                dialog_title="Выберите *.txt файл с курсом"
            ),
        )

        page.add(
            ft.Row(
                [
                    ft.Container(expand=1),
                    file_choosing_button,
                    ft.Container(expand=1),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        # Кнопка для начала тестирования

        edit_button = ft.ElevatedButton(
            "Редактировать",
            icon=ft.icons.EDIT_OUTLINED,
            color=backgroundcolor,
            visible=False,
            expand=1,
            on_click=editing
        )

        start_button = ft.ElevatedButton(
            "Продолжить",
            icon=ft.icons.ARROW_FORWARD,
            color=backgroundcolor,
            visible=False,
            expand=1,
            on_click=preview_start
        )

        page.add(
            ft.Row(
                [
                    ft.Container(expand=1),
                    start_button,
                    edit_button,
                    ft.Container(expand=1)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        page.add(ft.Container(expand=1))  # Контейнер, заполняющий пространство

        # Кнопка настроек

        def register_switch(e):
            global register_check
            register_check = not register_check

        def reversing_switch(e):
            global reversing
            reversing = not reversing

        def close_settings(e):
            global separator, duration_user
            settings_dlg.open = False
            separator = separator_field.value
            duration_user = int(duration_field.value) * 1000 if duration_field.value.isdigit() else duration_user
            page.update()

        separator_field = ft.TextField(
            label=f"Разделитель",
            value=str(separator)
        )

        duration_field = ft.TextField(
            label=f"Время (в секундах)",
            value=str(duration_user//1000)
        )

        register_check_switcher = ft.Switch(
            label="Учитывать регистр",
            track_color=maincolor,
            thumb_color=backgroundcolor,
            value=register_check,
            on_change=register_switch
        )

        reversing_switcher = ft.Switch(
            label="Поменять местами вопрос и ответ",
            track_color=maincolor,
            thumb_color=backgroundcolor,
            value=reversing,
            on_change=reversing_switch
        )

        settings_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Настройки"),
            content=ft.Column(
                [
                    ft.Text(f"Данным параметром вы можете изменить разделитель между терминами"),
                    separator_field,
                    ft.Text(f"Данным параметром вы можете изменить время показа правильного ответа "
                            f"(по умолчанию - 2 секунды), необходимо указать целое количество секунд"),
                    duration_field,
                    register_check_switcher,
                    reversing_switcher
                ],
            ),
            actions=[
                ft.TextButton("Сохранить", on_click=close_settings),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def open_settings_dlg(e):
            page.dialog = settings_dlg
            settings_dlg.open = True
            page.update()

        settings_button = ft.IconButton(
            icon_color=maincolor,
            icon=ft.icons.SETTINGS,
            bgcolor=backgroundcolor,
            on_click=open_settings_dlg
        )

        # Кнопка вызова подсказки

        def close_hint(e):
            hint.open = False
            page.update()

        hint = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подсказка"),
            content=ft.Text("Чтобы начать пользоваться программой вам необходимо выбрать файл, "
                            "содержащий материал для изучения (Тип файла - .txt). "
                            "Вопрос и ответ в нём должны быть разделены последовательностью символов. "
                            "Например:\nrain  -  дождь\nУказать собственный разделитель можно в настройках "
                            "(По умолчанию:  -  ). Обратите внимание, что файл должен содержать не менее двух "
                            "пар вопрос-ответ.\nПары разделяются с помощью символа новой строки (Enter)"),
            actions=[
                ft.TextButton("Хорошо", on_click=close_hint),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=close_hint,
        )

        def open_hint(e):
            page.dialog = hint
            hint.open = True
            page.update()

        hint_button = ft.IconButton(
            icon=ft.icons.QUESTION_MARK,
            icon_color=maincolor,
            bgcolor=backgroundcolor,
            on_click=open_hint
        )

        page.add(
            ft.Row(
                [
                    settings_button,
                    ft.Container(expand=True),
                    selected_file,
                    ft.Container(expand=True),
                    hint_button
                ],
                alignment=ft.MainAxisAlignment.END
            ),
        )

        if file_path != "":
            selected_file.visible = True
            selected_file.value = selection + " - Выбранный файл"
            selected_file.color = "green"
            start_button.visible = True
            edit_button.visible = True
            page.update()

    starting_window()


ft.app(target=main, assets_dir="assets")
