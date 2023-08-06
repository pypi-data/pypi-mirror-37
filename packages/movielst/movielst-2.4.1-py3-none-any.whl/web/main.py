from flask import Flask, render_template, send_from_directory, send_file, session, request, redirect
import json
from movielst import config, database
from web.forms import SettingsForm, LoginForm, AddUserForm
from web.dependency import check_for_dep

app = Flask(__name__)
app.config['SECRET_KEY'] = 'not really secret but still a really useless secret key for this use case'
app.config['DEP_FOLDER'] = config.CONFIG_PATH + 'dep/'


def main():
    check_for_dep()
    app.run(host=config.get_setting('Web', 'host'), port=config.get_setting('Web', 'port'), debug=True)


@app.route('/api/v1/dep/<path:filename>', methods=["GET"])
def dep_files(filename):
    return send_from_directory(app.config['DEP_FOLDER'], filename=filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in') and config.get_setting('Web', 'require_login') == "True":
        return login()
    else:
        data = database.db_to_json()
        return render_template('home.html', movie_list=data)


@app.route('/movie/<variable>')
def movie(variable):
    data = database.db_to_json()
    i = 0
    list = {}
    for datas in data:
        if datas["title"] == variable:
            list["title"] = datas["title"]
            list["genre"] = datas["genre"]
            list["imdb"] = datas["imdb"]
            list["runtime"] = datas["runtime"]
            list["tomato"] = datas["tomato"]
            list["year"] = datas["year"]
            list["awards"] = datas["awards"]
            list["cast"] = datas["cast"]
            list["director"] = datas["director"]
            list["poster"] = datas["poster"]
            list["description"] = datas["description"]
        i += 1
    return render_template('movie.html', list=list)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    form.log_level_field.default = config.get_setting('General', 'log_level')
    form.log_location_field.default = config.get_setting('General', 'log_location')
    form.location_field.default = config.get_setting('Index', 'location')
    form.use_external_api_field.default = config.get_setting('API', 'use_external_api')
    form.omdb_api_key_field.default = config.get_setting('API', 'OMDb_API_key')
    form.tmdb_api_key_field.default = config.get_setting('API', 'TMdb_API_key')
    form.web_host_field.default = config.get_setting('Web', 'host')
    form.web_port_field.default = config.get_setting('Web', 'port')
    form.web_require_login_field.default = config.get_setting('Web', 'require_login')
    if form.validate_on_submit():
        config.update_config('General', 'log_level', form.log_level_field.data)
        config.update_config('General', 'log_location', form.log_location_field.data)
        config.update_config('Index', 'location', form.location_field.data)
        config.update_config('API', 'use_external_api', form.use_external_api_field.data)
        config.update_config('API', 'OMDb_API_key', form.omdb_api_key_field.data)
        config.update_config('API', 'TMdb_API_key', form.tmdb_api_key_field.data)
        config.update_config('Web', 'host', form.web_host_field.data)
        config.update_config('Web', 'port', form.web_port_field.data)
        config.update_config('Web', 'require_login', form.web_require_login_field.data)
    form.process()
    return render_template('settings/settings.html', form=form)


@app.route('/settings/users', methods=['GET', 'POST'])
def settings_user():
    form = AddUserForm()
    choices_list = [(i[0], i[0]) for i in database.get_users()]
    form.user_list_field.choices = choices_list

    if form.validate_on_submit():
        if form.submit.data:
            # Add user to database
            database.add_user(form.username_field.data, form.password_field.data)
        if form.delete.data:
            database.delete_user(form.user_list_field.data)
    form.process()
    return render_template('settings/users.html', form=form)


@app.route('/export/<type>/<name>')
def export(type, name):
    if type == 'csv':
        database.export_to_csv(config.CONFIG_PATH + name)
        return send_file(config.CONFIG_PATH + name, as_attachment=True)
    elif type == 'xlsx':
        database.export_to_xlsx(config.CONFIG_PATH + name)
        return send_file(config.CONFIG_PATH + name, as_attachment=True)
    else:
        return "File type not supported"


@app.route('/movie/play/<variable>')
def play(variable):
    return send_from_directory('/', variable)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if  database.verify_user(form.username_field.data, form.password_field.data):
                session['logged_in'] = True
                return redirect('/')
            else:
                print("login failed")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')


if __name__ == '__main__':
    main()
