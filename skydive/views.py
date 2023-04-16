import random
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import send_mail
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import NewUserForm, ApplicantForm, PassengerForm, SubscribeForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from .models import Destination, Destination_desc, Applicant, Booking, Cards, Transactions, Passenger, Reservation


# Create your views here.

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'skydive/reset.html'
    email_template_name = 'skydive/password_reset_email.html'
    subject_template_name = 'skydive/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('skydive:login')


def index(request):
    loc_list = Destination.objects.all()
    return render(request, "index.html", {'loc_list': loc_list})


def search(request):
    try:
        loc_list = Destination.objects.all()
        if request.method == 'POST':
            place_user = request.POST['place']
            try:
                get_object_or_404(Destination_desc, province=place_user)
                # loc_desc_list = Destination_desc.objects.get()
            except MultipleObjectsReturned:
                loc_desc_list = Destination_desc.objects.filter(province=place_user)
                available_list = Reservation.objects.filter(destination__province=place_user)
                return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                               'available_list': available_list,
                                                               'search_item': 'province'})
        else:
            price_selected = request.GET.get("price")
            available_list = Reservation.objects.all()
            print(price_selected)
            if price_selected == "2":
                loc_desc_list = Destination_desc.objects.filter(price__range=(0, 1000))
            elif price_selected == "3":
                loc_desc_list = Destination_desc.objects.filter(price__range=(1001, 2000))
            elif price_selected == "4":
                loc_desc_list = Destination_desc.objects.filter(price__gt=2000)
            return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                           'available_list': available_list, 'search_item': 'price'})

    except Exception as err:
        print(err)
        messages.info(request, 'Location not available')
        return redirect('skydive:index')


def search_loc(request, destination):
    loc_desc_list = Destination_desc.objects.filter(province=destination)
    loc_list = Destination.objects.all()
    available_list = Reservation.objects.filter(destination__province=destination)
    return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                   'available_list': available_list, 'search_item': 'province'})


def type_skydive(request, skydive_type, desc_id):
    try:
        loc_desc_list = Destination_desc.objects.filter(type_skydive=skydive_type)
        loc_list = Destination.objects.all()
        available_list = Reservation.objects.filter(type_skydive=skydive_type)
        print(skydive_type)
        return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                       'available_list': available_list, 'search_item': 'type_skydive'})
    except Exception as err:
        print(err)
        return render(request, 'skydive/search.html', {'loc_desc_list': loc_desc_list, 'loc_list': loc_list,
                                                       'search_item': 'type_skydive'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials...')
            return redirect('/skydive/login')
    else:
        return render(request, 'skydive/login.html')


def logout(request):
    auth.logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect('..')


@login_required(login_url='/skydive/login')
def booking(request, dest_id):
    passengerformset = formset_factory(PassengerForm, extra=1)
    if request.method == 'POST':
        formset = passengerformset(request.POST)
        if formset.is_valid():
            # selected_item_id = int(request.GET.get('desc_id'))
            date_selected = datetime.strptime(request.POST['booking_date'], "%Y-%m-%d").date()
            loc_desc = Destination_desc.objects.get(dest_id=dest_id)
            user = request.user
            total_fare = formset.total_form_count() * loc_desc.price
            # request.session['n'] = formset.total_form_count()
            booking_item = Booking.objects.create(user=user, booking_date=date_selected, total_fare=total_fare,
                                                  type_skydive=loc_desc.type_skydive, destination_desc=loc_desc)
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]
                passenger_detail = Passenger(first_name=form.cleaned_data['first_name'],
                                             last_name=form.cleaned_data['last_name'],
                                             age=form.cleaned_data['age'])
                passenger_detail.save()

                booking_item.passengers.add(passenger_detail)
                # booking_item = Booking(user=user, passengers=passenger_detail,
                #                       booking_date=date_selected, total_fare=total_fare,
                #                       type_skydive=loc_desc.type_skydive, destination_desc=loc_desc
                #                       )
            booking_item.status = 'confirmed'
            booking_item.save()
            print("date", date_selected)
            print("type_skydive", type_skydive)
            reservation = Reservation.objects.get(
                Q(destination__province=loc_desc.province) & Q(type_skydive=loc_desc.type_skydive) & Q(
                    date_available=date_selected))
            reservation.spots_free = reservation.spots_total - formset.total_form_count()
            reservation.save(update_fields=["spots_free"])

            HST = total_fare * 0.13
            HST = float("{:.2f}".format(HST))
            final_total = HST + total_fare
            request.session['pay_amount'] = final_total
            return render(request, 'skydive/payment.html', {'person_count': formset.total_form_count(),
                                                            'total_fare': total_fare, 'HST': HST,
                                                            'final_total': final_total, 'province': loc_desc.province,
                                                            'bookingid': booking_item.booking_id})
        else:
            messages.error(request, "Data filled in form is Invalid. Check for age limit")
            formset = passengerformset()
            return render(request, 'skydive/booking.html', {'formset': formset, 'dest_id': dest_id})

    else:
        destin = Destination_desc.objects.get(dest_id=dest_id)
        list_reserv = Reservation.objects.filter(
            Q(destination__province=destin.province) & Q(type_skydive=destin.type_skydive))
        formset = passengerformset()
        return render(request, 'skydive/booking.html',
                      {'formset': formset, 'dest_id': dest_id, 'list_reserv': list_reserv})


def about(request):
    return render(request, 'skydive/about.html')


class JoinUs(View):

    def get(self, request):
        form = ApplicantForm()
        return render(request, 'skydive/join_us.html', {'form': form})

    def post(self, request):
        form = ApplicantForm(request.POST, request.FILES)
        form.save()
        messages.success(request, 'Application Successful Submitted')
        return redirect('skydive:joinus')

class Register(View):

    def get(self, request):
        form = NewUserForm()
        return render(request, 'skydive/register.html', context={"register_form": form})

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Username already exists.")
                return redirect('skydive:register')
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, "Email already exists.")
                return redirect('skydive:register')
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                messages.error(request, "Passwords do not match.")
                return redirect('skydive:register')
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user = user.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('skydive:login')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return redirect('skydive:register')


@login_required(login_url='/skydive/login')
def card_payment(request, booking_id):
    card_no = request.POST.get('card_number')
    pay_method = 'Debit card'
    mm = request.POST['MM']
    yy = request.POST['YY']
    cvv = request.POST['cvv']
    print("mm yy cvv", mm, yy, cvv)
    request.session['dcard'] = card_no
    try:
        balance = Cards.objects.get(Card_number=card_no, Ex_month=mm, Ex_Year=yy, CVV=cvv).Balance
        print("balance", balance)
        request.session['total_balance'] = balance
        # mail1 = Cards.objects.get(Card_number=card_no, Ex_month=mm, Ex_Year=yy, CVV=cvv).email

        if int(balance) >= int(request.session['pay_amount']):
            rno = random.randint(100000, 999999)
            request.session['OTP'] = rno

            amt = request.session['pay_amount']
            user = request.user
            # print(username)
            # user = User.objects.get(username=username)
            mail_id = user.email
            print([mail_id])
            msg = 'Your OTP For Payment of ₹' + str(amt) + ' is ' + str(rno)
            # print(msg)
            # print([mail_id])
            # print(amt)
            send_mail('OTP for Debit card Payment',
                      msg,
                      'test@gmail.com',
                      [mail_id],
                      fail_silently=False)
            return render(request, 'skydive/OTP.html')
        error_message = 'Payment failed. Your booking has been deleted.'
        return render(request, 'skydive/wronginfo.html', {'error_message': error_message})

    except:
        booking = get_object_or_404(Booking, pk=booking_id)
        reservation = Reservation.objects.get(Q(destination__province=booking.destination_desc.province) &
                                              Q(type_skydive=booking.type_skydive) &
                                              Q(date_available=booking.booking_date))
        reservation.spots_free = reservation.spots_free + booking.passengers.count()
        booking.delete()
        reservation.save(update_fields=["spots_free"])
        error_message = 'Payment failed. Your booking has been deleted.'
        return render(request, 'skydive/wronginfo.html', {'error_message': error_message})


@login_required(login_url='/skydive/login')
def otp_verification(request):
    otp1 = int(request.POST['otp'])
    username = request.user.get_username()
    amt = int(request.session['pay_amount'])
    pay_method = 'Debit card'
    if otp1 == int(request.session['OTP']):
        del request.session["OTP"]
        total_balance = int(request.session['total_balance'])
        rem_balance = int(total_balance - int(request.session["pay_amount"]))
        c = Cards.objects.get(Card_number=request.session['dcard'])
        c.Balance = rem_balance
        c.save(update_fields=['Balance'])
        c.save()
        t = Transactions(username=username, Amount=amt, Payment_method=pay_method,
                         Status='Success')
        t.save()

        return render(request, 'skydive/confirmation_page.html')
    else:
        t = Transactions(username=username, Amount=amt, Payment_method=pay_method, Status='Failed')
        t.save()
        return render(request, 'skydive/wrong_OTP.html')


@login_required(login_url='/skydive/login')
def mybookings(request):
    user = request.user
    booking_list = Booking.objects.filter(user=user)
    return render(request, 'skydive/mybookings.html', {'booking_list': booking_list})


@csrf_exempt
def cancel_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            print(ref)
            try:
                book = Booking.objects.get(booking_id=ref)
                reservation = Reservation.objects.get(Q(destination__province=book.destination_desc.province) &
                                                      Q(type_skydive=book.type_skydive) &
                                                      Q(date_available=book.booking_date))
                reservation.spots_free = reservation.spots_free + booking.passengers.count()
                if book.user == request.user:
                    book.status = 'cancelled'
                    book.save()
                    reservation.save(update_fields=["spots_free"])

                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'error': "User unauthorised"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': e
                })
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'skydive/subscribe_success.html')
