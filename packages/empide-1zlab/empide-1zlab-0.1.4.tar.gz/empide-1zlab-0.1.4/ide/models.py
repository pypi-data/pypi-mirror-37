from django.db import models
import datetime

# Create your models here.


class VisitCounts(models.Model):
    date = models.DateField(auto_now=True, verbose_name='日期')
    amount_of_day = models.IntegerField(default=0, verbose_name='单日访问量')

    def __str__(self):
        return '{0} {1}次'.format(self.date, self.amount_of_day)

    @classmethod
    def today_add_one(cls):
        try:
            counts_today = cls.objects.get(date=datetime.datetime.today())
            counts_today.amount_of_day += 1
        except:
            counts_today = VisitCounts()
            counts_today.amount_of_day += 1
        finally:
            counts_today.save()

    @classmethod
    def get_total_counts(cls):
        sum([i.amount_of_day for i in cls.objects.all()])


class Visitors(models.Model):
    ip = models.CharField(
        max_length=15, verbose_name='IP地址', default='unkown', blank=True)
    time = models.DateTimeField(auto_now=True, verbose_name='访问时间')
    url = models.SlugField(verbose_name='URL')

    def __str__(self):
        return 'IP:{0} TIME:{1} URL:{2}'.format(self.ip, self.time, self.url)


class EspIP(models.Model):
    ip = models.CharField(
        max_length=15, verbose_name='IP地址', default='unkown', blank=True)

    esp_ip = models.TextField(verbose_name='ESP 内网IP地址', default='')

    def set_esp_ip(self, esp_ip):
        if esp_ip in self.esp_ip.split(','):
            pass
        else:
            self.esp_ip += esp_ip

    def get_esp_ip(self):
        return self.esp_ip.split(',')