from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ["name"]


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, related_name="books"
    )
    contributor = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True)
    author = models.CharField()
    synopsis = models.TextField()
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("bookclub:book_detail", args=[str(self.pk)])

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["-publication_year"]

class BookReview(models.Model): #TO-DO: Fix when logged in/not
    user_reviewer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE) #set when logged in
    anon_reviewer = models.TextField(blank=False) #set when not logged in
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(blank=False)
    comment = models.TextField(blank=False)

class Bookmark(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_bookmarked = models.DateField()

class Borrow(models.Model): #TO-DO: Fix when logged in/not
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE) #set when logged in
    name = models.CharField() #set when not logged in
    date_borrowed = models.DateField()
    date_to_return = models.DateField()