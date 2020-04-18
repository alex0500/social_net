from django.utils.timezone import now
from django.db import models


class Post(models.Model):
    aPost_text = models.TextField(verbose_name='Post')
    nUser_id = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE, verbose_name='username')
    def __str__(self):
        return self.nUser_id.username

class Like(models.Model):
    nUser_id = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, verbose_name='username')
    aAction = models.CharField(choices=(('like','like'), ('unlike', 'unlike')), max_length=6, verbose_name='like/unlike')
    oDate = models.DateField(default=now().date())
    nPost_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, verbose_name='post')
    def __str__(self):
        return self.nPost_id.aPost_text

class Logger(models.Model):
    nUser_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='username')
    oDate = models.DateField(default=now().date())
    aAction = models.CharField(choices=(('login','login'), ('request', 'request')), max_length=7, verbose_name='action')
    def __str__(self):
        return self.nUser_id.username


