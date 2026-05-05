from .models import Book, BookReview
from .forms import BookForm, BookUpdateForm, BookReviewForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from django.urls import reverse, reverse_lazy



class BookListView(ListView):
    model = Book
    template_name = "book_list.html"


class BookDetailView(DetailView):
    model = Book
    form = BookReviewForm
    template_name = "book_detail.html"
    #success_url = reverse_lazy('bookclub:book_detail')
    reviews = BookReview.objects.all()
    reviewgroups = Book.objects.all()
    ctx = {
        "bookreview_list": reviews, "reviewgroup": reviewgroups
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review"] = BookReviewForm()
        return context
    
    def post(self, request, *args, **kwargs):
        review = BookReviewForm(request.POST)
        if review.is_valid():
            #review.instance.review_id = self.kwargs["pk"]
            review.save()
        return self.get(request, *args, **kwargs)


class BookCreateView(RoleRequiredMixin, CreateView):
    #TO-DO: Contributor field is set to the logged in user that is not editable.
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
        book = form.save(commit=False)
        return super().form_valid(form)