from .models import Book, BookReview
from .forms import BookForm, BookReviewForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from django.urls import reverse, reverse_lazy



class BookListView(ListView):
    model = Book
    template_name = "book_list.html"

    # def get_queryset(self):
    #     queryset = Book.objects.all()

    #     if self.request.user.is_authenticated():
    #         queryset = queryset.exclude(owner=self.request.user)
    #     return queryset
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     if self.request.user.is_authenticated:
    #         context["books_user"] = Book.object.filter(owner=self.request.user)
    #     else:
    #         context["books_user"] = None
    #     return context


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
    model = Book
    form_class = BookForm
    template_name = "book_create.html"
    success_url = reverse_lazy('bookclub:book_list')
    required_role = "Book Contributor"

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = "book_edit.html"