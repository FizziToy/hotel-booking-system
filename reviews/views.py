from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from hotels.models import Hotel

from .forms import ReviewForm
from .models import Review


@login_required
def create_review(request, hotel_id):
    hotel = get_object_or_404(
        Hotel,
        id=hotel_id
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            Review.objects.create(
                hotel=hotel,
                user=request.user,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )

            return redirect(
                'hotels:hotel_detail',
                hotel.id
            )

    else:
        form = ReviewForm()

    return render(
        request,
        'reviews/create_review.html',
        {
            'hotel': hotel,
            'form': form
        }
    )