from app import create_app
from celery import Celery
from services.Crawler import Crawler


def make_celery(app):
    celery = Celery(app.import_name)

    celery.conf.update(app.config['CELERY_CONFIG'])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(create_app())


@celery.task(name='crawler')
def crawler(keyword):
    print('task celery', keyword)
    Crawler.crawler(keyword)
    return {'status': 'OK'}
