from .models import Book, BookReview, Borrow, Bookmark
from .forms import BookForm, BookUpdateForm, BookReviewForm, BookBorrowForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from django.urls import reverse, reverse_lazy
from datetime import timedelta
from django.shortcuts import redirect
from django.utils import timezone



class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books = Book.objects.all()
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            contributions = context['contributed_books'] = all_books.filter(contributor=profile)
            bookmarks = context['bookmarked_books'] = all_books.filter(bookmark__profile=profile)
            reviews = context['reviewed_books'] = all_books.filter(reviews__user_reviewer=profile)

            contributed = [book.pk for book in contributions]
            bookmarked = [book.pk for book in bookmarks]
            reviewed = [book.pk for book in reviews]

            user_books = contributed + bookmarked + reviewed

            context['all_books'] = all_books.exclude(pk__in=user_books)

        else:
            context['all_books'] = all_books

        return context


class BookDetailView(DetailView):
    model = Book
    form = BookReviewForm
    template_name = "book_detail.html"
    success_url = reverse_lazy('bookclub:book_detail')
    reviews = BookReview.objects.all()
    reviewgroups = Book.objects.all()
    ctx = {
        "bookreview_list": reviews, "reviewgroup": reviewgroups
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        user = self.request.user

        #for reviews
        context["review"] = BookReviewForm()
        context["reviews"] = book.reviews.all()

        #for bookmarks
        context["bookmark_count"] = Bookmark.objects.filter(book=book).count()

        if user.is_authenticated:
            context["bookmarked"] = Bookmark.objects.filter(book=book, profile=user.profile).exists()

        return context
    
    def post(self, request, *args, **kwargs):
        book = self.get_object()

        #for bookmarks
        if self.request.user.is_authenticated:
            if request.POST.get('to_bookmark') == 'bookmark':
                bookmarked_book = Bookmark.objects.filter(book=book, profile=self.request.user.profile)

                if bookmarked_book.exists():
                    bookmarked_book.delete()
                else:
                    Bookmark.objects.create(book=book, profile=self.request.user.profile, date_bookmarked=timezone.now())
                return redirect('bookclub:book_detail', pk=book.pk)
        else:
            return redirect('/accounts/login/')

        #for reviews
        form = BookReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            if request.user.is_authenticated:
                review.user_reviewer = request.user.profile
            else:
                review.anon_reviewer = "Anonymous"
            review.save()
            

        return self.get(request, *args, **kwargs)


class BookCreateView(RoleRequiredMixin, CreateView):
    model = Book
    required_role = "Book Contributor"
    template_name = "book_create.html"
    form_class = BookForm
    success_url = reverse_lazy('bookclub:book_list')

    def form_valid(self, form):
        form.instance.contributor = self.request.user.profile
        return super().form_valid(form)


class BookUpdateView(RoleRequiredMixin, UpdateView):
    model = Book
    required_role = "Book Contributor"
    template_name = "book_edit.html"
    form_class = BookUpdateForm

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)
    

class BookBorrowView(UpdateView):
    model = Borrow
    form_class = BookBorrowForm
    template_name = "book_borrow.html"

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        form = BookBorrowForm(request.POST)
        book = self.get_object()

        if form.is_valid():
            date_borrowed = form.cleaned_data["date_borrowed"]
            date_to_return = date_borrowed + timedelta(days=14)
            
            if request.user.is_authenticated:
                Borrow.objects.create(book=book, borrower = request.user.profile, name = request.user.profile.display_name,
                                      date_borrowed=date_borrowed, date_to_return=date_to_return)
            else:
                Borrow.objects.create(book=book, name = form.cleaned_data['name'],
                                      date_borrowed=date_borrowed, date_to_return=date_to_return)
            book.available_to_borrow = False
            book.save()

            return redirect('bookclub:book_detail', pk=book.pk)

        return self.get(request, *args, **kwargs)

