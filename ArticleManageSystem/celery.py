# celery worker -A ArticleManageSystem -l INFO

from celery import Celery

broker = 'redis://localhost:6379/1'
backend = 'redis://localhost:6379/2'
app = Celery('ArticleManageSystem', broker=broker, backend=backend)
