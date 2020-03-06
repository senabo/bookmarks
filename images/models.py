from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name = 'images_created',
                             on_delete = models.CASCADE
                             )
    title = models.CharField(verbose_name = 'Заголовок', max_length = 200)
    slug = models.SlugField(verbose_name = 'Слаг', max_length = 200, blank = True)
    url = models.URLField(verbose_name = 'Посилання на оригінал')
    image = models.ImageField(verbose_name = 'Картинка', upload_to = 'images/%Y/%m/%d/')
    description = models.TextField(verbose_name = 'Опис', blank = True)
    created = models.DateField(verbose_name = 'Створено', auto_now_add = True, db_index = True)
    total_likes = models.PositiveIntegerField(db_index = True, default = 0)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name = 'images_liked',
                                        verbose_name = 'Лайки',
                                        blank = True,
                                        )


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        '''Автоматична генерація слага'''
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args = [self.id, self.slug])

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
