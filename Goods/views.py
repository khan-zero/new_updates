from django.shortcuts import render, get_object_or_404
from . import models
from . import forms
from django.contrib.auth.models import User

def main(request):
    guest = request.user
    if guest.is_authenticated:
        user_id = guest.id
    else:
        user_id = None
        

    banners = models.Banner.objects.filter(is_active = True)[:5]
    user = get_object_or_404(User, pk=user_id)
    navbar = models.NavbarTop.objects.all()
    footer = models.Footer.objects.all()
    footer_images = models.FooterImages.objects.all()
    categories = models.Category.objects.all()

    context = {}
    context['banners'] = banners
    context['user'] = user
    context['nav_top'] = navbar
    context['categories'] = categories
    context['footer'] = footer
    context['footer_images'] = footer_images

    return render(request, 'index.html', context)
    
def product_enter_list(request):
    entries = models.ProductEnter.objects.all() #product -> enters
    return render(request, 'product_enter_list.html', {'entries': entries})


def product_enter_create(request):
    if request.method == 'POST':
        form = ProductEnterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product entry created successfully.')
            return redirect('product_enter_list')
    else:
        form = forms.ProductEnterForm()
    return render(request, 'product_enter_form.html', {'form': form})


def product_enter_update(request, pk):
    entry = get_object_or_404(models.ProductEnter, pk=pk)
    if request.method == 'POST':
        form = ProductEnterForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product entry updated successfully.')
            return redirect('product_enter_list')
    else:
        form = ProductEnterForm(instance=entry)
    return render(request, 'product_enter_form.html', {'form': form})


def product_enter_delete(request, pk):
    entry = get_object_or_404(ProductEnter, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Product entry deleted successfully.')
        return redirect('product_enter_list')
    return render(request, 'product_enter_confirm_delete.html', {'entry': entry})
