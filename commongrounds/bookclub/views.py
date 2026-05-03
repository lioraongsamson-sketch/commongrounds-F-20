from .models import Book, BookReview
from .forms import BookForm, BookReviewForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



class BookListView(ListView):
    model = Book
    template_name = "book_list.html"



class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"
    reviews = BookReview.objects.all()
    reviewgroups = Book.objects.all()
    ctx = {
        "bookreview_list": reviews, "reviewgroup": reviewgroups
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Book.objects.all()
        context["review"] = BookReviewForm()
        return context
    
    def post(self, request, *args, **kwargs):
        review = BookReviewForm(request.POST)
        if review.is_valid():
            review.instance.book_id = self.kwargs["pk"]
            review.save()
        return self.get(request, *args, **kwargs)
