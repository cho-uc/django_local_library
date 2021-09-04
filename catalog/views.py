from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
	"""View function for home page of site."""

	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# The 'all()' is implied by default.
	num_authors = Author.objects.count()

	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_visits': num_visits,
	}

	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
	model = Book
	paginate_by = 10

class BookDetailView(generic.DetailView):
	model = Book

	def book_detail_view(request, primary_key):
		try:
			book = Book.objects.get(pk=primary_key)
		except Book.DoesNotExist:
			raise Http404('Book does not exist')

		return render(request, 'catalog/book_detail.html', context={'book': book})

#----------------------------------------------

class AuthorListView(generic.ListView):
	model = Author

class AuthorDetailView(generic.DetailView):
	model = Author

	def author_detail_view(request, primary_key):
		try:
			author = Author.objects.get(pk=primary_key)
		except Author.DoesNotExist:
			raise Http404('Author does not exist')

		return render(request, 'catalog/author_detail.html', context={'author': author})

#----------------------------------------------
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
	"""Generic class-based view listing books on loan to current user."""
	model = BookInstance
	template_name ='catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

#----------------------------------------------

def about(request):
	return render(request, 'catalog/about.html', {'title': 'About'})

def news(request):
	return render(request, 'catalog/news.html', {'title': 'News'})