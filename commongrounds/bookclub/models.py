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
    contributor = models.ForeignKey(
        "accounts.Profile", on_delete=models.SET_NULL, null=True
    )
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


class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        "accounts.Profile", on_delete=models.CASCADE, blank=True, null=True
    )
    anon_reviewer = models.TextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    title = models.CharField(blank=False)
    comment = models.TextField(blank=False)

    def __str__(self):
        if self.request.user.is_authenticated:
            return f"Reviewed by {self.user_reviewer}"
        else:
            return f"Reviewed by Anonymous"


class Bookmark(models.Model):
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_bookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} bookmarked {self.book} on {self.date_bookmarked}"


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    name = models.CharField()
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        if self.request.user.is_authenticated:
            return f"Borrowed by {self.borrower}"
        else:
            return f"Borrowed by {self.name}"
