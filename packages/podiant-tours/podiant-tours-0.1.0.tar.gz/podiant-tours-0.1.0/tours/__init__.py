__version__ = '0.1.0'


def get_tour_data(request):
    a = request.user.is_anonymous
    if callable(a):
        a = a()

    if a:
        return {}

    from .models import TourData
    for view in TourData.objects.filter(user=request.user):
        return view.get_data()

    return {}


def save_tour_data(request, data):
    a = request.user.is_anonymous
    if callable(a):
        a = a()

    if a:
        return False

    from .models import TourData
    for view in TourData.objects.filter(user=request.user):
        view.set_data(data, commit=True)
        return True

    view = TourData(user=request.user)
    view.set_data(data, commit=True)
    return True
