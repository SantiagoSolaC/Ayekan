from flask import render_template
from app import create_app
# from app.src.substraction import substract_from_breakfast, substract_from_lunch, substract_from_tea, substract_from_dinner
from apscheduler.schedulers.background import BackgroundScheduler
import unittest
import atexit


app = create_app()


# @app.before_first_request
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(substract_from_breakfast, "cron", hour="9")
#     scheduler.add_job(substract_from_lunch, "cron", hour="12")
#     scheduler.add_job(substract_from_tea, "cron", hour="17")
#     scheduler.add_job(substract_from_dinner, "cron", hour="21")
#     scheduler.start()
#     atexit.register(lambda: scheduler.shutdown())


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html", error=error)


if __name__ == "__main__":
    app.run(port=5000)
