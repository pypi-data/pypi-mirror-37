from flask import Flask
import click
from caci.controler.Profiles import information_db

def create_app():

    @click.command('do_run')
    def do_run():
        print("HELLO from do work")
        information_db()
        # from caci.run import create_app
        # return create_app(os.environ['config'])


    app = Flask(__name__)
    # app.config.from_object(configuration)

    from caci.configuration.app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from caci.model.models import db
    db.init_app(app)
    app.cli.add_command(do_run)
    return app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
