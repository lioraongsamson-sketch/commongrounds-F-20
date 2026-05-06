from .models import Book, BookReview, Borrow, Bookmark
from .forms import BookForm, BookUpdateForm, BookReviewForm, BookBorrowForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from django.urls import reverse, reverse_lazy



class BookListView(ListView):
    model = Book
    context_object_name = "book"
    template_name = "book_list.html"
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.user.is_authenticated:
    #         profile = self.request.user.profile
    #         context['contributed'] = Book.objects.filter(contributor=profile)
    #         context['bookmarks'] = Book.objects.filter(bookmark=profile)
    #         context['reviewed'] = Book.object.filter(reviews=profile)
    #     return context


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
        context["review"] = BookReviewForm()
        context["reviews"] = book.reviews.all()
        return context
    
    def post(self, request, *args, **kwargs):
        book = self.get_object()
        
        #if self.request.user.is_authenticated:
            

        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
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