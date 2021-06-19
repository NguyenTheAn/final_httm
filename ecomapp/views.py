from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from .utils import password_reset_token
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import *
import requests
from django.shortcuts import get_object_or_404


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart_obj = get_object_or_404(Shoppingcart, id=cart_id)
            if request.user.is_authenticated and request.user.account:
                cart_obj.customerid = Customer.objects.get(userid__accountid = self.request.user.account)
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class HomeView(EcomMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Item.objects.all().order_by("-id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            if Wishlist.objects.filter(customerid = customer).exists():
                wishlist = Wishlist.objects.get(customerid = customer)
                wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
                context['wishListItem'] = wishListItem
            else:
                wishList = Wishlist.objects.create(customerid = customer)
                wishList.save()
                context['wishListItem'] = []
        return context

class UpdateToWishList(EcomMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = self.request.GET.get("action")
        pro_id = self.kwargs["pro_id"]
        all_products = Item.objects.all().order_by("-id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            item = Item.objects.get(id = pro_id)
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            wishlist = Wishlist.objects.get(customerid = customer)
            if action == "add":
                wishlistline = Wishlistline.objects.create(wishlistid = wishlist, itemid = item)
                wishlistline.save()
            else:
                wishlistline = Wishlistline.objects.get(wishlistid = wishlist, itemid = item)
                wishlistline.delete()
            wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
            context['wishListItem'] = wishListItem

        return context


class AllProductsView(EcomMixin, TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context

class EditProfileView(View):
    template_name = "customerprofileedit.html"
    def get(self, request, *args, **kwargs):
        form = EditProfileForm()
        usr_id = kwargs['usr_id']
        user = Users.objects.get(id = usr_id)
        form.fields['username'].initial  = user.accountid.user.username
        form.fields['phonenumber'].initial  = user.contactinfoid.phonenumber
        form.fields['email'].initial  = user.contactinfoid.email
        form.fields['full_name'].initial  = user.fullnameid.fullname
        form.fields['city'].initial  = user.addressid.city
        form.fields['district'].initial  = user.addressid.district
        form.fields['town'].initial  = user.addressid.town
        form.fields['street'].initial  = user.addressid.street
        form.fields['description'].initial  = user.addressid.description
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(data=request.POST)
        if form.is_valid():
            usr_id = kwargs['usr_id']
            user = Users.objects.get(id = usr_id)
            username = form.cleaned_data.get("username")
            phonenumber = form.cleaned_data.get("phonenumber")
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("full_name")
            fn = name.split(" ")[0]
            ln = name.split(" ")[-1]
            mn = ""
            for i in name.split(" ")[1:-1]:
                mn = mn + i + " "
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            town = form.cleaned_data.get("town")
            street = form.cleaned_data.get("street")
            description = form.cleaned_data.get("description")
            user.accountid.user.username = username
            user.contactinfoid.phonenumber = phonenumber
            user.contactinfoid.email = email
            user.fullnameid.firstname = fn
            user.fullnameid.middlename = mn
            user.fullnameid.lastname = ln
            user.addressid.city = city
            user.addressid.district = district
            user.addressid.town = town
            user.addressid.street = street
            user.addressid.description = description
            
            user.accountid.user.save()
            user.contactinfoid.save()
            user.fullnameid.save()
            user.addressid.save()
            user.save()

            form.instance.userid = user
            context = {"customer" : Customer.objects.get(userid = user)}
        return render(request, "customerprofile.html", context)

class ShippingAddressListView(View):
    template_name = "shippingaddresslist.html"
    def get(self, request, *args, **kwargs):
        cus_id = kwargs['cus_id']
        customer = Customer.objects.get(id = cus_id)
        shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
        context = {"shippingaddresslist" : shippingaddresslist, "customer" : customer}
        return render(request, self.template_name, context)

class ShippingAddressDeleteView(View):
    template_name = "shippingaddresslist.html"
    def get(self, request, *args, **kwargs):
        addr_id = kwargs['addr_id']
        address = Address.objects.get(id = addr_id)
        address.delete()
        cus_id = kwargs['cus_id']
        customer = Customer.objects.get(id = cus_id)
        shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
        context = {"shippingaddresslist" : shippingaddresslist, "customer" : customer}
        return render(request, self.template_name, context)
        

class ShippingAddressCreateView(EcomMixin, View):
    template_name = "shippingaddresscreate.html"

    def get(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm()
        context = {"form":form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm(request.POST)
        if form.is_valid():
            cus_id = kwargs['cus_id']
            customer = Customer.objects.get(id = cus_id)
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            town = form.cleaned_data.get("town")
            street = form.cleaned_data.get("street")
            description = form.cleaned_data.get("description")
            address = Address.objects.create(city = city, district = district, town = town, street = street, description = description)
            shippingaddress = Shippingaddress.objects.create(addressid = address, note = "")
            form.instance.customerid = customer
            form.instance.shippingaddressid = shippingaddress
            form.save()
            shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
            context = {"form":form, "shippingaddresslist":shippingaddresslist, "customer" : customer}

        return render(request, "shippingaddresslist.html", context)

class ShippingAddressEditView(EcomMixin, View):
    template_name = "shippingaddressedit.html"

    def get(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm()
        addr_id = kwargs['addr_id']
        address = Address.objects.get(id = addr_id)
        form.fields['city'].initial  = address.city
        form.fields['district'].initial  = address.district
        form.fields['town'].initial  = address.town
        form.fields['street'].initial  = address.street
        form.fields['description'].initial  = address.description
        context = {"form":form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ShippingAddressCreateForm(request.POST)
        if form.is_valid():
            cus_id = kwargs['cus_id']
            addr_id = kwargs['addr_id']
            customer = Customer.objects.get(id = cus_id)
            city = form.cleaned_data.get("city")
            district = form.cleaned_data.get("district")
            town = form.cleaned_data.get("town")
            street = form.cleaned_data.get("street")
            description = form.cleaned_data.get("description")
            address = Address.objects.get(id = addr_id)
            address.city = city
            address.district = district
            address.town = town
            address.street = street
            address.description = description
            address.save()
            shippingaddresslist = [customeraddress.shippingaddressid for customeraddress in CustomerShippingaddress.objects.filter(customerid = customer)]
            context = {"form":form, "shippingaddresslist":shippingaddresslist, "customer" : customer}

        return render(request, "shippingaddresslist.html", context)

class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        url_slug = kwargs['slug']
        product = Item.objects.get(slug=url_slug)
        feedbacks = Feedback.objects.filter(itemid = product)
        context = {'form': form, "product": product, "feedbacks": feedbacks}
        return render(request, 'productdetail.html', context)

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(data=request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            rate = form.cleaned_data['rating']
            url_slug = kwargs['slug']
            product = Item.objects.get(slug=url_slug)
            customer = Customer.objects.get(userid__accountid__user = request.user)
            feedback = Feedback.objects.create(itemid = product, customerid = customer, content = content, rate = rate)
            feedback.save()
            feedbacks = Feedback.objects.filter(itemid = product)
            context = {'form': FeedBackForm(), "product": product, "feedbacks": feedbacks}
        return render(request, 'productdetail.html', context)

class AddToCartView(EcomMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Item.objects.get(id=product_id)
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            # check if cart exists
            cart_id = self.request.session.get("cart_id", None)
            if cart_id:
                cart_obj = Shoppingcart.objects.get(id=cart_id)
                this_product_in_cart = Cartline.objects.filter(itemid = product_obj)

                # item already exists in cart
                if this_product_in_cart.exists():
                    cartproduct = this_product_in_cart.last()
                    cartproduct.num += 1
                    cartproduct.save()
                    cart_obj.save()
                # new item is added in cart
                else:
                    cartproduct = Cartline.objects.create(
                        shoppingcartid=cart_obj, itemid=product_obj, num=1)
                    cart_obj.save()

            else:
                if Shoppingcart.objects.filter(customerid = customer).exists():
                    cart_obj = Shoppingcart.objects.get(customerid = customer)
                else:
                    cart_obj = Shoppingcart.objects.create(customerid = customer)
                self.request.session['cart_id'] = cart_obj.id
                cartproduct = Cartline.objects.create(
                    shoppingcartid=cart_obj, itemid=product_obj, num=1)
                cart_obj.save()
            context["error"] = False
        else:
            context["error"] = True
        return context


class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = Cartline.objects.get(id=cp_id)
        cart_obj = cp_obj.shoppingcartid

        if action == "inc":
            cp_obj.num += 1
            cp_obj.save()
            cart_obj.save()
        elif action == "dcr":
            cp_obj.num -= 1
            cp_obj.save()
            cart_obj.save()
            if cp_obj.num == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("ecomapp:mycart")


class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Shoppingcart.objects.get(id=cart_id)
            [cartline.delete() for cartline in Cartline.objects.filter(shoppingcartid = cart)]
            cart.save()
        return redirect("ecomapp:mycart")


class MyCartView(EcomMixin, TemplateView):
    template_name = "mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = self.request.user).exists():
            cart_id = self.request.session.get("cart_id", None)
            if cart_id:
                cart = Shoppingcart.objects.get(id=cart_id)
            else:
                customer = Customer.objects.get(userid__accountid__user = self.request.user)
                if Shoppingcart.objects.filter(customerid = customer).exists():
                    cart = Shoppingcart.objects.get(customerid = customer)
                else:
                    cart = Shoppingcart.objects.create(customerid = customer)
            cartline = Cartline.objects.filter(shoppingcartid = cart)
            context['cartline'] = cartline
            context['cart'] = cart
        return context


class CheckoutView(EcomMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomapp:home")
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.account):
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        cart_obj = Shoppingcart.objects.get(id=cart_id) if cart_id else None
        context['cart'] = cart_obj
        return context
    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            customer = Customer.objects.get(userid__accountid__user = self.request.user)
            cart_obj = Shoppingcart.objects.get(id=cart_id)
            cartlines = cart_obj.cartline_set.all()
            if Orderhistory.objects.filter(customerid__userid__accountid__user = self.request.user).exists():
                orderhistory = Orderhistory.objects.get(customerid__userid__accountid__user = self.request.user)
            else:
                orderhistory = Orderhistory.objects.create(customerid = customer)
            
            method = form.cleaned_data.get("paymentMethod")
            convert ={"1": "Cash",
                      "2": "Banking",
                      "3": "QRCode"}
            payment = Payment.objects.create(isComplete = False, method = convert[method])
            form.instance.customerid = customer
            form.instance.taxid = Tax.objects.get(id = 1)
            form.instance.voucherid = form.cleaned_data.get("voucherid")
            form.instance.paymentid = payment
            form.instance.addressid = form.cleaned_data.get("addressid")
            form.instance.status = "Order Received"
            form.instance.time = datetime.datetime.now()
            order = form.save()
            historyline = Historyline.objects.create(orderhistoryid = orderhistory, orderid = order)
            historyline.save()
            for cartline in cartlines:
                orderitem = Orderitem.objects.create(orderid = order, itemid = cartline.itemid, count = cartline.num)
                orderitem.save()
                cartline.delete()
        else:
            return redirect("ecomapp:home")
        return super().form_valid(form)


class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        phonenumber = form.cleaned_data.get("phonenumber")
        email = form.cleaned_data.get("email")
        name = form.cleaned_data.get("full_name")
        fn = name.split(" ")[0]
        ln = name.split(" ")[-1]
        mn = ""
        for i in name.split(" ")[1:-1]:
            mn = mn + i + " "
        city = form.cleaned_data.get("city")
        district = form.cleaned_data.get("district")
        town = form.cleaned_data.get("town")
        street = form.cleaned_data.get("street")
        description = form.cleaned_data.get("description")
        fullname = Fullname.objects.create(lastname = ln, firstname = fn, middlename = mn)
        contact = Contactinfo.objects.create(email = email, phonenumber = phonenumber)
        user_ = User.objects.create_user(username = username, password = password)
        account = Account.objects.create(user = user_)
        addressid = Address.objects.create(description = description, city = city, district= district, town =town, street=street)
        user = Users.objects.create(accountid = account, contactinfoid = contact, fullnameid = fullname, addressid = addressid)
        form.instance.userid = user
        login(self.request, user.accountid.user)
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")

class ReviewSuccessView(TemplateView):
    template_name = "reviewsuccess.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class SendReview(CreateView):
    template_name = "review.html"
    form_class = ReviewForm
    success_url = reverse_lazy("ecomapp:reviewsuccess")
    def form_valid(self, form):
        customer = Customer.objects.get(userid__accountid__user = self.request.user)
        content = form.cleaned_data.get("content")
        form.instance.customerid = customer
        form.instance.content = content
        form.instance.reviewtime = datetime.datetime.now()
        
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(userid__accountid__user = usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class AboutView(EcomMixin, TemplateView):
    template_name = "about.html"


class ContactView(EcomMixin, TemplateView):
    template_name = "contactus.html"


class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(userid__accountid = self.request.user.account)
        context['customer'] = customer
        orders = Order.objects.filter(customerid=customer).order_by("-id")
        context["orders"] = orders
        return context

class WishListView(TemplateView):
    template_name = "wishlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(userid__accountid = self.request.user.account)
        wishlist = Wishlist.objects.get(customerid = customer)
        wishListItem = [wishlistline.itemid for wishlistline in Wishlistline.objects.filter(wishlistid = wishlist)]
        context['wishListItem'] = wishListItem
        return context

class ReviewListView(TemplateView):
    template_name = "reviewlist.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(userid__accountid = self.request.user.account)
        reviews = Customerreview.objects.filter(customerid = customer)
        context['reviews'] = reviews
        return context

class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(userid__accountid__user = request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.account != order.customerid.userid.accountid:
                return redirect("ecomapp:customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Item.objects.filter(
            Q(productid__name__icontains=kw) | Q(description__icontains=kw))
        context["results"] = results
        return context


class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("ecomapp:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

# # admin pages


class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Staffs.objects.filter(userid__accountid__user = usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Staffs.objects.filter(userid__accountid__user = request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            status="Order Received").order_by("-id")
        return context

class AdminProductDetailView(View):
    template_name = "adminpages/adminproductdetail.html"

    def get(self, request, *args, **kwargs):
        form = EditProductForm()
        pro_id = kwargs['pro_id']
        product = Product.objects.get(id=pro_id)

        form.fields['producer'].initial  = product.producerid
        form.fields['name'].initial  = product.name
        form.fields['manufacturingdate'].initial  = product.manufacturingdate
        form.fields['expirydate'].initial  = product.expirydate
        convert = {
                "Clothes":"1",
                "Electronic":"2",
                "Book":"3"
            }
        form.fields['type'].initial  = convert[product.type]

        context = {'form': form, "product": product}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditProductForm(data=request.POST)
        if form.is_valid():
            producer = form.cleaned_data['producer']
            name = form.cleaned_data['name']
            manufacturingdate = form.cleaned_data['manufacturingdate']
            expirydate = form.cleaned_data['expirydate']
            type = form.cleaned_data['type']

            pro_id = kwargs['pro_id']
            product = Product.objects.get(id=pro_id)
            product.producer = producer
            product.name = name
            product.manufacturingdate = manufacturingdate
            product.expirydate = expirydate
            convert = {
                "1": "Clothes",
                "2": "Electronic",
                "3": "Book"
            }
            product.type = convert[type]
            product.save()

            form.fields['producer'].initial  = product.producerid
            form.fields['name'].initial  = product.name
            form.fields['manufacturingdate'].initial  = product.manufacturingdate
            form.fields['expirydate'].initial  = product.expirydate
            form.fields['type'].initial  = product.type

            context = {'form': form, "product": product}
        return render(request, self.template_name, context)

class AdminItemDetailView(View):
    template_name = "adminpages/adminitemdetail.html"

    def get(self, request, *args, **kwargs):
        form = EditItemForm()
        url_slug = kwargs['slug']
        product = Item.objects.get(slug=url_slug)
        form.fields['price'].initial  = product.price
        form.fields['description'].initial  = product.description
        context = {'form': form, "product": product}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = EditItemForm(data=request.POST)
        if form.is_valid():
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            url_slug = kwargs['slug']
            product = Item.objects.get(slug=url_slug)
            product.price = price
            product.description = description
            if request.POST.get("upload", "") == "true":
                product.isUpload = True
            else:
                product.isUpload = False
            product.save()
            form.fields['price'].initial  = price
            form.fields['description'].initial  = description
            context = {'form': form, "product": product}
        return render(request, self.template_name, context)

class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context

class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

class AdminReviewListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminreviewlist.html"
    queryset = Customerreview.objects.all().order_by("-id")
    context_object_name = "allreviews"

class AdminReviewDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminreviewdetail.html"
    model = Customerreview
    context_object_name = "rv_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session["review_id"] = context['rv_obj'].id
        return context

class AdminReplyReviewView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminreplyreview.html"
    form_class = ReplyReviewForm
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        staff = Staffs.objects.get(userid__accountid__user = self.request.user)
        review = Customerreview.objects.get(id = self.request.session['review_id'])
        review.isReply = True
        review.save()
        del self.request.session['review_id']
        message = form.cleaned_data.get("content")
        form.instance.customerreviewid = review
        form.instance.message = message
        form.instance.time = datetime.datetime.now()
        form.instance.staffid = staff

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomapp:adminorderdetail", kwargs={"pk": order_id}))

class AdminProductListView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminproductlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Product.objects.filter(
                Q(productid__name__icontains=kw) | Q(description__icontains=kw))
        else:
            queryset = Product.objects.all().order_by("-id")
        context["allproducts"] = queryset
        return context

class AdminItemListView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminitemlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        if kw is not None:
            queryset = Item.objects.filter(
                Q(productid__name__icontains=kw) | Q(description__icontains=kw))
        else:
            queryset = Item.objects.all().order_by("-id")
        context["allproducts"] = queryset
        return context

class AdminImprotingrecordListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminimportingrecordlist.html"
    queryset = Importingrecord.objects.all().order_by("-id")
    context_object_name = "allrecords"

class AdminProductDeleteView(AdminRequiredMixin, View):
    template_name = "adminpages/adminproductlist.html"
    def get(self, request, *args, **kwargs):
        pro_id = self.kwargs["pro_id"]
        product = Product.objects.get(id = pro_id)
        product.delete()
        queryset = Product.objects.all().order_by("-id")
        context = {"allproducts":queryset}
        return render(request, self.template_name, context)

class AdminItemDeleteView(AdminRequiredMixin, View):
    template_name = "adminpages/adminproductlist.html"
    def get(self, request, *args, **kwargs):
        queryset = Item.objects.all().order_by("-id")
        pro_id = self.kwargs["pro_id"]
        item = Item.objects.get(id = pro_id)
        item.productid.delete()
        context = {"allproducts":queryset}
        return render(request, self.template_name, context)


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomapp:adminproductlist")

    def form_valid(self, form):
        producer = form.cleaned_data.get("producer")
        manufacturingdate = form.cleaned_data.get("manufacturingdate")
        expirydate = form.cleaned_data.get("expirydate")
        name = form.cleaned_data.get("name")
        prod_type = form.cleaned_data.get("type")
        slug = form.cleaned_data.get("slug")
        price = form.cleaned_data.get("price")
        description = form.cleaned_data.get("description")
        convert = {
            "1": "Clothes",
            "2": "Electronic",
            "3": "Book"
        }
        p = Product.objects.create(producerid = producer, manufacturingdate = manufacturingdate, expirydate = expirydate,
                                    type = convert[prod_type], name = name)
        images = self.request.FILES.getlist("images")
        ProductCategory.objects.create(categoryid = Category.objects.get(id = int(prod_type)), productid = p)
            
        form.instance.productid = p
        form.instance.price = price
        form.instance.description = description
        form.instance.slug = slug
        form.instance.image = images[0]
        return super().form_valid(form)


class AdminImportProductView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminimportproduct.html"
    form_class = ImportProductForm
    success_url = reverse_lazy("ecomapp:adminimportproduct")

    def form_valid(self, form):
        supplier = form.cleaned_data.get("supplier")
        product = form.cleaned_data.get("product")
        number = form.cleaned_data.get("number")
        price = form.cleaned_data.get("price")
        product.num += number
        item = Item.objects.get(productid = product)
        item.price = price*(1+0.1)
        item.save()
        product.save()
        staff = Staffs.objects.get(userid__accountid__user = self.request.user)
        date = datetime.datetime.now()
        form.instance.supplierid = supplier
        form.instance.productid = product
        form.instance.staffid = staff
        form.instance.date = date
        form.instance.num = number
        form.instance.price = price
        return super().form_valid(form)