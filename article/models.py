from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import MinLengthValidator

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name = "Yazar")
    title = models.CharField(max_length=50, verbose_name = "Bashliq", validators=[MinLengthValidator(10)])
    content = RichTextField()
    article_image = models.FileField(blank=True, null=True, verbose_name= "Meqaleye shekil elave edin")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name= "Yarandigi tarix")
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE, verbose_name = "Meqale", related_name = "comments")
    comment_author = models.CharField(max_length = 50, verbose_name = "Ad")
    comment_content = models.CharField(max_length = 200, verbose_name = "Sherh")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content
    
    class Meta:
        ordering = ['-comment_date']