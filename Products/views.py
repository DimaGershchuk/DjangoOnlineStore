from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import ProductProxy, Category
from .serializers import ProductSerializers
from .filters import ProductFilter
from .pagination import ProductPageNumberPagination
from .forms import ReviewForm


def home_view(request):
    categories = Category.objects.all()
    return render(request, 'home-page.html', {'categories': categories})


class ProductListView(ListView):
    model = ProductProxy
    template_name = 'products/product-list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('category', 'brand')

        slug = self.request.GET.get('category', '').strip()
        q = self.request.GET.get('q',      '').strip()

        if slug:
            qs = qs.filter(category__slug=slug)

        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(category__name__icontains=q) |
                Q(brand__name__icontains=q)
            )

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class ProductDetailView(FormMixin, DetailView):
    model = ProductProxy
    template_name = 'products/product-detail.html'
    slug_field = 'slug' # slug_url_kwarg — «де взяти» значення вхідного параметра з адреси (ключ у kwargs), slug_field — «по якому» полю моделі це значення шукати.
    slug_url_kwarg = 'slug'
    context_object_name = 'product'
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('product-detail', kwargs={'slug': self.object.slug})

    def get_queryset(self):
        return (
            ProductProxy.objects.select_related('category', 'brand')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        reviews_qs = product.reviews.select_related('user').order_by('-created_at')
        context['reviews'] = reviews_qs
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            reviews = form.save(commit=False)
            reviews.product = self.object
            reviews.user = request.user
            reviews.save()
            return redirect(self.get_success_url())
        return self.form_invalid(form)


class ProductListCreateAPIView(generics.ListAPIView):
    queryset = ProductProxy.objects.select_related('category', 'brand').all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = ProductPageNumberPagination


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductProxy.objects.select_related('category', 'brand').all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
