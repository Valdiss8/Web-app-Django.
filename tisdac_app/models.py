from django.db import models
from datetime import date, datetime, timedelta
from django.urls import reverse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404





class Resource(models.Model):
    name = models.CharField(max_length=100, null=True)
    summary = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    logo = models.FileField(upload_to='resource', null=True)
    webpage = models.CharField(max_length=1500, null=True)


class About(models.Model):  # https://www.adventist.org/who-are-seventh-day-adventists/
    title = models.CharField(max_length=300, default='')
    article = models.TextField(default='')
    image = models.FileField(upload_to='about', null=True, blank=True)




class Visitor(models.Model):
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return f'{self.name} - {self.email} - {self.phone}'


class Feedback(models.Model):
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True)
    feedback = models.TextField(max_length=1000, null=True)
    date = models.DateTimeField(null=True, blank=True)


class Service(models.Model):
    STATUS = [('Active', 'Active'),
              ('Inactive', 'Inactive')]
    name = models.CharField(max_length=100, null=True)
    summary = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Inactive')
    slug = models.SlugField(default='', null=False, db_index=True, blank=True)
    image = models.FileField(upload_to='service', null=True, blank=True)
    image2 = models.FileField(upload_to='service', null=True, blank=True)
    image3 = models.FileField(upload_to='service', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('service-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name}'


class Department(models.Model):
    STATUS = [('Active', 'Active'),
              ('Inactive', 'Inactive')]

    name = models.CharField(max_length=100, null=True)
    summary = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)
    leader = models.CharField(max_length=100, null=True, blank=True)
    leader_email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Inactive')
    slug = models.SlugField(default='', null=False, db_index=True, blank=True)
    image = models.FileField(upload_to='department', null=True)
    image2 = models.FileField(upload_to='service', null=True)
    image3 = models.FileField(upload_to='service', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('activity-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name}'


class News(models.Model):
    PUBLISH = [('YES', 'YES'),
               ('NO', 'NO'),
               ('ONLY FOR REGISTERED', 'FOR REGISTERED')]
    publish = models.CharField(max_length=19, choices=PUBLISH, default='YES')
    title = models.CharField(max_length=300, default='')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(null=True, blank=False)
    place = models.CharField(max_length=200, default='Mere pst. 3')
    summary = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True)
    slug = models.SlugField(default='', null=False, db_index=True, blank=True)
    image = models.FileField(upload_to='news', null=True,)
    image2 = models.FileField(upload_to='service', null=True, blank=True)
    image3 = models.FileField(upload_to='service', null=True, blank=True)
    video_youtube_link = models.CharField(max_length=300, null=True, blank=True)
    visitors = models.ManyToManyField(Visitor, blank=True)



    def get_url(self):
        return reverse('news-detail', args=[self.slug])

    def __str__(self):
        return f'{self.title} - {self.date}'


class Events(models.Model):
    General = 'General'
    Children = 'Children’s Ministries'
    Communication = 'Communication Department'
    Family = 'Family Ministries'
    Health = 'Health Ministries Department'
    Sabbath_School = 'Sabbath School'
    Small_Group = 'Small Group Ministry'
    Woman = 'Women’s Ministries'
    Youth = 'Youth Department'
    Pathfinder = 'Pathfinder Club'
    Adventurers = 'Adventurers Club'
    Music = 'Music Ministry'
    Treasure = 'Church Treasure'
    Deacon = 'Deacon Ministry'

    REPEATABLE = [('YES', 'YES'),
                  ('NO', 'NO')]
    title = models.CharField(max_length=300, default='')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    repeatable = models.CharField(max_length=3, choices=REPEATABLE, default='NO')
    date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    place = models.CharField(max_length=200, default='Mere pst. 3')
    summary = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True)
    slug = models.SlugField(default='', null=False, db_index=True, blank=True)
    image = models.FileField(upload_to='event', null=True, blank=True)
    image2 = models.FileField(upload_to='service', null=True, blank=True)
    image3 = models.FileField(upload_to='service', null=True, blank=True)
    visitors = models.ManyToManyField(Visitor, blank=True)

    def perdelta(self, start_date, end_date, delta=timedelta(days=7)):
        now = datetime.now()
        if end_date is None:
            end_date = now + delta
        if now.timestamp() < start_date.timestamp():
            return start_date
        if now.timestamp() > end_date.timestamp():
            return end_date

        if now.timestamp() <= end_date.timestamp():
            curr = start_date
            while curr.timestamp() < end_date.timestamp():
                curr += delta
                if curr.timestamp() > now.timestamp():
                    return curr
        return start_date

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        if self.repeatable == 'NO':
            self.start_date = None
            self.end_date = None
            if self.date:
                if self.date.timestamp() < datetime.now().timestamp():
                    if not News.objects.filter(title=self.title, date=self.date).first():
                        a = News(
                            publish='YES',
                            title=self.title,
                            department=self.department,
                            date=self.date,
                            place=self.place,
                            summary=self.summary,
                            description=self.description,
                            image=self.image,
                            image2=self.image2,
                            image3=self.image3
                        )
                        a.save()
                        super(Events, self).save(*args, **kwargs)
                        if self.visitors:
                            for visitor in self.visitors.all():
                                a.visitors.add(visitor)
                                a.save()

        if self.repeatable == 'YES':
            if self.start_date is None and self.date:
                self.start_date = self.date
            if self.date is None and self.start_date:
                self.date = self.start_date
            if self.date and self.start_date:
                if self.date.timestamp() < self.start_date.timestamp():
                    self.date = self.start_date
            if self.date and self.end_date:
                if self.date.timestamp() > self.end_date.timestamp():
                    self.date = self.end_date
            if self.start_date and self.end_date:
                if self.start_date.timestamp() > self.end_date.timestamp():
                    self.start_date = self.end_date

            if self.start_date:
                if self.date.timestamp() < datetime.now().timestamp():
                    if not News.objects.filter(title=self.title, date=self.date).first():
                        a = News(
                            publish='NO',
                            title=self.title,
                            department=self.department,
                            date=self.date,
                            place=self.place,
                            summary=self.summary,
                            description=self.description,
                            image=self.image,
                            image2=self.image2,
                            image3=self.image3
                            )
                        a.save()
                        super(Events, self).save(*args, **kwargs)
                        if self.visitors:
                            for visitor in self.visitors.all():
                                a.visitors.add(visitor)
                                a.save()
                        self.visitors.clear()

                self.date = self.perdelta(self.start_date, self.end_date)

        super(Events, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('event-detail', args=[self.slug])

    def __str__(self):
        return f'{self.title} - {self.date}'




