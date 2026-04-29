from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'shypilova_math_key'

USERS = {
    "admin": "12345",
    "student": "2026"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USERS.get(username) == password:
            session['user'] = username
            return redirect(url_for('menu'))
        error = "Невірний логін або пароль"
    return render_template('login.html', error=error)


@app.route('/menu')
def menu():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')


@app.route('/task4', methods=['GET', 'POST'])
def task4():
    if 'user' not in session: return redirect(url_for('login'))

    if 'task4_state' not in session:
        session['task4_state'] = {'count': 0, 'last_num': None, 'history': [], 'finished': False}

    result = None
    if request.method == 'POST':
        try:
            num = int(request.form.get('number'))
            state = session['task4_state']

            if num == 0:
                state['finished'] = True
                result = state['count']
            else:
                if state['last_num'] is not None:
                    if num * state['last_num'] < 0:
                        state['count'] += 1

                state['last_num'] = num
                state['history'].append(num)

            session.modified = True
        except (ValueError, TypeError):
            pass

    return render_template('task4.html', state=session['task4_state'], result=result)


@app.route('/task4_reset')
def task4_reset():
    session.pop('task4_state', None)
    return redirect(url_for('task4'))


@app.route('/task10_step1', methods=['GET', 'POST'])
def task10_step1():
    if 'user' not in session: return redirect(url_for('login'))

    if request.method == 'POST':
        session['m_dims'] = {
            'n': int(request.form.get('n')),
            'm': int(request.form.get('m')),
            'k': int(request.form.get('k'))
        }
        return redirect(url_for('task10_step2'))
    return render_template('task10_step1.html')


@app.route('/task10_step2', methods=['GET', 'POST'])
def task10_step2():
    if 'user' not in session: return redirect(url_for('login'))
    dims = session.get('m_dims')

    if request.method == 'POST':
        n, m, k = dims['n'], dims['m'], dims['k']
        A = [[int(request.form.get(f'A_{i}_{j}')) for j in range(m)] for i in range(n)]
        B = [[int(request.form.get(f'B_{i}_{j}')) for j in range(k)] for i in range(m)]

        C = [[sum(A[i][l] * B[l][j] for l in range(m)) for j in range(k)] for i in range(n)]

        return render_template('task10_result.html', A=A, B=B, C=C)

    return render_template('task10_step2.html', dims=dims)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)