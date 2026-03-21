from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models
from django.db.models import Sum
from django.urls import reverse_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        pr = sum(p.rating for p in Post.objects.filter(author=self)) * 3
        ur = sum(c.rating for c in Comment.objects.filter(user=self.user))
        cr = sum(c.rating for c in Comment.objects.filter(post_author=self))
        self.rating = pr + ur + cr
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    news = "NW"
    articles = "AR"
    TYPE_CHOICES = ((news,"Новость") , (articles,"Статья"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default=news)
    category = models.ManyToManyField(Category, through="PostCategory")
    created_ad = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) <= 124:
            return self.text
        else:
            return self.text[:124] + "..."

    def get_absolute_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.pk})



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.groups.filter(name='common').exists():
            try:
                group = Group.objects.get(name='common')
                self.groups.add(group)
            except Group.DoesNotExist:
                group = Group.objects.create(name='common')
                self.groups.add(group)