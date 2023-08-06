from flask import Flask, render_template, send_from_directory, send_file
import json
from movielst import config, database
from web.forms import SettingsForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'not really secret but still a really useless secret key for this use case'


def main():
    app.run(host=config.get_setting('Web', 'host'), port=config.get_setting('Web', 'port'), debug=False)


@app.route('/')
def index():
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
    if form.validate_on_submit():
        config.update_config('General', 'log_level', form.log_level_field.data)
        config.update_config('General', 'log_location', form.log_location_field.data)
        config.update_config('Index', 'location', form.location_field.data)
        config.update_config('API', 'use_external_api', form.use_external_api_field.data)
        config.update_config('API', 'OMDb_API_key', form.omdb_api_key_field.data)
        config.update_config('API', 'TMdb_API_key', form.tmdb_api_key_field.data)
    form.process()
    return render_template('settings.html', form=form)


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


@app.route('/login')
def login():
    form = LoginForm()
    form.process()
    return render_template('login.html', form=form)


if __name__ == '__main__':
    main()
