from django.http import HttpRequest
from django.shortcuts import render
import sweetify

# Create your views here.
from django.views.generic.base import View
from .fomrs import ContactUsForm
from .models import ContactUs


class ContactUsView(View):
    def get(self, request: HttpRequest):
        contact_form = ContactUsForm()
        user_exist = request.session.get('user_not_found_reset')
        if user_exist is not None:
            sweetify.sweetalert(request, title='اکانت شما یافت نشد', icon='error',
                                text='اگر مشکلی از سایت هست در این صفخه میتوتنید به ما اطلاع دهید.',
                                button='OK',
                                persistent=True
                                )
            del request.session['user_not_found']

        context = {
            'form': ContactUsForm
        }
        return render(request, 'contact_us/contact_us_page.html', context)

    def post(self, request: HttpRequest):
        contact_form = ContactUsForm(request.POST)
        if request.method == 'POST':
            if contact_form.is_valid():
                full_name = contact_form.cleaned_data.get('full_name')
                email = contact_form.cleaned_data.get('email')
                title = contact_form.cleaned_data.get('title')
                text_massege = contact_form.cleaned_data.get('text_massege')
                contact: ContactUs = ContactUs(full_name=full_name, email=email, title=title, text_massege=text_massege)
                contact.save()
                sweetify.sweetalert(request, 'عملیات موفق', icon='success',
                                    text='پیام شما در اسرع وقت چک می شود و به ایمیل شما پیام داده می شود .',
                                    button=True,
                                    persistent=True
                                    )
        context = {
            'form': contact_form
        }
        return render(request, 'contact_us/contact_us_page.html', context)
