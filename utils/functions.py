import datetime
import hashlib
import os
import time

from django.core.cache import cache

from ArticleManageSystem.settings import SECRET_KEY, BASE_DIR
from common.models import FeedBack


def my_md5(flag, user_id=0, password=''):
    '''
    :param flag: 0-获取token 1-加密密码
    :param user_id: 管理员id
    :param password: 密码
    :return:
    '''
    if flag == 0:
        md5_str = SECRET_KEY + str(user_id) + str(time.time())
    elif flag == 1:
        md5_str = SECRET_KEY + password
    m = hashlib.md5()
    m.update(md5_str.encode("utf-8"))
    secret = m.hexdigest()
    return secret


def write_file(request, name):
    try:
        file = request.FILES.get(name)
        file_name_li = file.name.split('.')
        file_type = file_name_li[-1]
        if len(file_name_li) > 2:
            file_name_li.pop()
        file_name = '_'.join(file_name_li)
        upload_time = str(time.time()).split('.')[0]
        mix_file_name = file_name+upload_time+'.'+file_type
        dirs = os.path.join(BASE_DIR, 'static/img', str(datetime.datetime.now().month),
                            str(datetime.datetime.now().day))
        if not os.path.exists(dirs):
            os.makedirs(os.path.join(BASE_DIR, 'static/img', dirs))
        file_url = os.path.join(BASE_DIR, 'static/img', dirs, mix_file_name)
        with open(file_url, 'wb') as f:
            for line in file.chunks():
                f.write(line)
        return "/static" + file_url.split("/static")[1]
    except Exception as e:
        return None


# def dian_zan():
#     try:
#         old = cache.get("dianzan")
#         for each in old:
#             article, user, view = each
#             check = FeedBack.objects.filter(article_id=article, user_id=user)
#             if check:
#                 obj = check.first()
#                 obj.feed_back = view
#                 obj.save()
#             else:
#                 FeedBack.objects.create(article_id=article, user_id=user, feed_back=view)
#         cache.set("dianzan", None)
#     except Exception:
#         pass


def model_to_zh(model):
    src_dict = {
        "Admin": "管理员",
        "User": "用户",
        "Position": "职位",
        "Article": "文章",
        "Tag": "标签",
        "Category": "分类",
        "Comment": "评论",
    }
    return src_dict[model]


def get_page(self, request, query_set):
    page = request.GET.get('page', '')
    size = request.GET.get('size', '')
    if not page:
        page = 1
    if not size:
        size = 10
    page = int(page)
    size = int(size)
    self.count = len(query_set)
    self.page = page
    if self.count:
        page_num = self.count // size if self.count % size == 0 else self.count//size+1
        if page_num <= 9:
            show_page = {"show_page": [i+1 for i in range(page_num)]}
        elif self.page < 5:
            show_page = {"show_page": [i+1 for i in range(9)]}
        elif page_num - self.page < 5:
            show_page = {"show_page": [i+1 for i in range(page_num)[-9:]]}
        else:
            show_page = {"show_page": [i for i in range(self.page-4, self.page+5)]}
        self.context.update(show_page)
        self.context.update({"cur_page": self.page})
        self.context.update({"count": self.count})
        self.context.update({"page_num": page_num})
    else:
        self.context.update({"count": 0})
    count = 0
    res = {}
    start = (self.page-1)*size
    end = (self.page - 1) * size + size
    for k, v in query_set.items():
        if count >= start:
            res.update({k: v})
        count += 1
        if count >= end:
            break
    return res