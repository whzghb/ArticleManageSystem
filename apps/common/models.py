from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class ActionGroup(models.Model):
    group = models.CharField(max_length=32, verbose_name='动作组名')

    class Meta:
        verbose_name = "动作组表"
        verbose_name_plural = verbose_name


class Right(models.Model):
    url = models.CharField(max_length=32, verbose_name='路由')
    action = models.CharField(max_length=32, verbose_name='名称')
    type = models.CharField(max_length=8, verbose_name='请求方式')
    action_group = models.ForeignKey(ActionGroup, verbose_name='动作组', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = verbose_name


class Position(models.Model):
    name = models.CharField(max_length=40, verbose_name='职位名称')
    rights = models.ManyToManyField(Right, null=True, blank=True, verbose_name='权限')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='是否已删除', help_text='0-未删除 1-已删除')

    class Meta:
        verbose_name = "职位表"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]


class Admin(models.Model):
    email = models.CharField(default="", max_length=32, verbose_name='邮箱')
    password = models.CharField(max_length=100, verbose_name='密码')
    name = models.CharField(default="", max_length=32, verbose_name='用户名')
    position = models.ForeignKey(Position, null=True, blank=True, verbose_name='职位', on_delete=models.CASCADE)
    rights = models.ManyToManyField(Right, null=True, blank=True, verbose_name='权限')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    last_log_time = models.DateTimeField(default='1970-01-01 00:00:00', verbose_name='最后登录时间')
    last_log_ip = models.CharField(max_length=32, default='127.0.0.1', verbose_name='最后登录ip')
    log_times = models.IntegerField(default=0, verbose_name='登录次数')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='是否已删除')
    is_sysop = models.SmallIntegerField(default=0, verbose_name='是否超级管理员', help_text='0-否 1-是')

    class Meta:
        verbose_name = "管理员表"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='类名')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name = "分类表"
        verbose_name_plural = verbose_name
        ordering = ["-id"]


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='是否已删除')

    class Meta:
        verbose_name = "标签表"
        verbose_name_plural = verbose_name
        ordering = ["-id"]


class Article(models.Model):
    title = models.CharField(max_length=120, verbose_name='标题')
    author = models.CharField(max_length=32, verbose_name='作者')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, null=True, blank=True, verbose_name='标签')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    pub_time = models.DateTimeField(default='1970-01-01 00:00:00', verbose_name='发布时间')
    adder = models.ForeignKey(Admin, verbose_name='添加人', on_delete=models.CASCADE)
    read_times = models.IntegerField(default=0, verbose_name='阅读次数')
    last_read_time = models.DateTimeField(default='1970-01-01 00:00:00', verbose_name='最后阅读时间')
    reject_reason = models.CharField(max_length=50, default='', verbose_name='驳回理由')
    status = models.SmallIntegerField(default=1, verbose_name='状态',
                                      help_text='1-草稿箱 2-待审核 3-待发布 4-已发布 5-已驳回')
    is_deleted = models.SmallIntegerField(default=0, verbose_name='是否已删除',
                                          help_text='0-未删除 1-已删除')
    img = models.CharField(max_length=100, default="", verbose_name="封面路径")

    class Meta:
        verbose_name = "文章表"
        verbose_name_plural = verbose_name
        ordering = ["-pub_time", "-add_time"]


class Content(models.Model):
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='内容')
    is_deleted = models.SmallIntegerField(default=0)


class User(models.Model):
    name = models.CharField(max_length=32, verbose_name="用户名", unique=True)
    password = models.CharField(max_length=100, verbose_name="密码")
    email = models.CharField(max_length=40, verbose_name="邮箱")
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    last_log_time = models.DateTimeField(default="1970-01-01 00:00:00", verbose_name="最后登录时间")
    log_times = models.IntegerField(default=0, verbose_name="登录次数")
    last_log_ip = models.CharField(max_length=32, default="127.0.0.1", verbose_name="最后登录ip")
    is_deleted = models.SmallIntegerField(default=0, verbose_name="是否已删除")

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ["-register_time"]


class FeedBack(models.Model):
    article = models.ForeignKey(Article, verbose_name="文章id", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="用户id", on_delete=models.CASCADE)
    feed_back = models.SmallIntegerField(verbose_name="反馈", help_text="0-未评 1-好评 2-差评")
    add_time = models.DateTimeField(auto_now=True, verbose_name="添加时间")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论者id")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="文章id")
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, verbose_name="父评论")
    content = models.TextField(verbose_name="评论内容")
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    is_deleted = models.SmallIntegerField(default=0, verbose_name="是否已删除")

    class Meta:
        ordering = ["-comment_time"]


class Log(models.Model):
    admin = models.CharField(default="", max_length=30, verbose_name="管理员姓名")
    model = models.CharField(default="", max_length=40, verbose_name="表名")
    method = models.CharField(default="", max_length=10, verbose_name="操作方式")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    name = models.CharField(default="", max_length=100, verbose_name="名称")

    class Meta:
        ordering = ["-id"]


class Menu(models.Model):
    name = models.CharField(max_length=20, verbose_name="名称")
    url = models.CharField(default="", max_length=30, verbose_name="路径")
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, verbose_name="点击者")
    click_time = models.IntegerField(default=1, verbose_name="点击次数")


class CommentFeedBack(models.Model):
    comment = models.ForeignKey(Comment, verbose_name="评论id", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="用户id", on_delete=models.CASCADE)
    feed_back = models.SmallIntegerField(verbose_name="反馈", help_text="0-未评 1-好评 2-差评")




