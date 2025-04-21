from flask import Flask, render_template, request, redirect, session, url_for
from auth import validate_ipa_user, validate_secondary_auth

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # поменяй на что-то безопасное

@app.route('/')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login_step1'))
    return render_template('main.html')

@app.route('/login/step1', methods=['GET', 'POST'])
def login_step1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_ipa_user(username, password):
            session['ipa_user'] = username
            return redirect(url_for('login_step2'))
        else:
            return render_template('login_step1.html', error="Неверные IPA данные.")
    return render_template('login_step1.html')

@app.route('/login/step2', methods=['GET', 'POST'])
def login_step2():
    if 'ipa_user' not in session:
        return redirect(url_for('login_step1'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_secondary_auth(username, password):
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login_step2.html', error="Ошибка авторизации.")
    return render_template('login_step2.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_step1'))


@app.route('/scripts')
def snos_scripts():
    # В будущем: тянуть из БД
    scripts = [
        {"id": 1, "name": "Обновление пакетов", "description": "Обновляет системные пакеты на всех узлах кластера."},
        {"id": 2, "name": "Проверка статуса HDFS", "description": "Выполняет health-check сервисов HDFS и логирует результат."},
        {"id": 3, "name": "Очистка временных директорий", "description": "Удаляет устаревшие временные файлы на серверах Hadoop."},
        {"id": 4, "name": "Обновление пакетов", "description": "Обновляет системные пакеты на всех узлах кластера."},
        {"id": 5, "name": "Проверка статуса HDFS",
         "description": "Выполняет health-check сервисов HDFS и логирует результат."},
        {"id": 6, "name": "Очистка временных директорий",
         "description": "Удаляет устаревшие временные файлы на серверах Hadoop."},
    ]
    return render_template('snos_scripts.html', scripts=scripts)

# 🔧 Заглушка: страница запуска скрипта
@app.route('/scripts/run/<int:script_id>')
def run_script(script_id):
    return f"Заглушка: запуск скрипта с ID {script_id}"


@app.route('/master-script', methods=['GET', 'POST'])
def master_script():
    checklist_items = [
        "Обновить пакеты на всех нодах",
        "Перезапустить все демоны Hadoop",
        "Раскатать параметры Ambari",
        "Проверить статус NameNode",
        "Очистить временные директории",
        "Проверить cron задачи",
        "Проверить свободное место на дисках",
        "Выполнить тестовую запись в HDFS",
        "Синхронизировать часы на всех узлах",
        "Проверить подключение к метрикам Prometheus"
    ]

    if request.method == 'POST':
        selected = request.form.getlist('checklist')
        ambari_url = request.form.get('ambari_url', '')
        return f"Ambari: {ambari_url}<br>Выбраны шаги: {', '.join(selected)}"

    return render_template('master_script.html', checklist=checklist_items)




if __name__ == '__main__':
    app.run(debug=True)
