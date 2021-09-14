from django.db import models
from django.contrib.auth.models import User

article = "ART"
news = "NEW"

POST_TYPES = [
    (article, 'статья'),
    (news, 'новость')
]


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def update_rating(self):
        my_post_ratings = Post.objects.filter(author=self).values("rating")
        total_post_ratings = 0
        for rating in my_post_ratings:
            total_post_ratings += int(rating['rating'])*3

        my_comment_ratings = Comment.objects.filter(user=self.user).values("rating")
        total_comment_ratings = 0
        for rating in my_comment_ratings:
            total_comment_ratings += int(rating['rating'])

        my_posts = Post.objects.filter(author=self)
        total_post_comment_rating = 0
        for my_post in my_posts:
            comments = Comment.objects.filter(post=my_post).values("rating")
            for rate in comments:
                total_post_comment_rating += int(rate['rating'])

        return total_post_comment_rating + total_comment_ratings + total_post_ratings


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=POST_TYPES, default=article)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    name = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[0: 123] + "..."

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating - 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def present(self):
        print("Comment by " + self.user.username)
        print(self.text)
        print('Date:' + str(self.date))
        print('Rating: ' + str(self.rating) + "\n")