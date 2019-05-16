import json
import os
import time
from ArticleManageSystem.settings import BASE_DIR
from ArticleManageSystem.celery import app


# @app.task
def write_video(request, name):
    try:
        # request = json.loads(request)
        file = request.FILES.get(name)
        file_name_li = file.name.split('.')
        file_type = file_name_li[-1]
        if len(file_name_li) > 2:
            file_name_li.pop()
        file_name = '_'.join(file_name_li)
        upload_time = str(time.time()).split('.')[0]
        mix_file_name = file_name+upload_time+'.'+file_type
        file_url = os.path.join(BASE_DIR, 'static/video', mix_file_name)
        with open(file_url, 'wb') as f:
            for line in file.chunks():
                f.write(line)
        return "/static" + file_url.split("/static")[1]
    except Exception as e:
        return None