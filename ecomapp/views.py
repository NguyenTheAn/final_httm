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
        context['myname'] = "Banana"
        all_products = Item.objects.all().order_by("-id")
        paginator = Paginator(all_products, 8)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class AllProductsView(EcomMixin, TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class ProductDetailView(EcomMixin, TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Item.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


class AddToCartView(EcomMixin, TemplateView):
    template_name = "addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Item.objects.get(id=product_id)
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
        if request.user.is_authenticated and request.user.account:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Shoppingcart.objects.get(id=cart_id)
        else:
            cart_obj = None
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
            
            # if pm == "Khalti":
            #     return redirect(reverse("ecomapp:khaltirequest") + "?o_id=" + str(order.id))
            # elif pm == "Esewa":
            #     return redirect(reverse("ecomapp:esewarequest") + "?o_id=" + str(order.id))
        else:
            return redirect("ecomapp:home")
        return super().form_valid(form)


# class KhaltiRequestView(View):
#     def get(self, request, *args, **kwargs):
#         o_id = request.GET.get("o_id")
#         order = Order.objects.get(id=o_id)
#         context = {
#             "order": order
#         }
#         return render(request, "khaltirequest.html", context)


# class KhaltiVerifyView(View):
#     def get(self, request, *args, **kwargs):
#         token = request.GET.get("token")
#         amount = request.GET.get("amount")
#         o_id = request.GET.get("order_id")
#         print(token, amount, o_id)

#         url = "https://khalti.com/api/v2/payment/verify/"
#         payload = {
#             "token": token,
#             "amount": amount
#         }
#         headers = {
#             "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
#         }

#         order_obj = Order.objects.get(id=o_id)

#         response = requests.post(url, payload, headers=headers)
#         resp_dict = response.json()
#         if resp_dict.get("idx"):
#             success = True
#             order_obj.payment_completed = True
#             order_obj.save()
#         else:
#             success = False
#         data = {
#             "success": success
#         }
#         return JsonResponse(data)


# class EsewaRequestView(View):
#     def get(self, request, *args, **kwargs):
#         o_id = request.GET.get("o_id")
#         order = Order.objects.get(id=o_id)
#         context = {
#             "order": order
#         }
#         return render(request, "esewarequest.html", context)


# class EsewaVerifyView(View):
#     def get(self, request, *args, **kwargs):
#         import xml.etree.ElementTree as ET
#         oid = request.GET.get("oid")
#         amt = request.GET.get("amt")
#         refId = request.GET.get("refId")

#         url = "https://uat.esewa.com.np/epay/transrec"
#         d = {
#             'amt': amt,
#             'scd': 'epay_payment',
#             'rid': refId,
#             'pid': oid,
#         }
#         resp = requests.post(url, d)
#         root = ET.fromstring(resp.content)
#         status = root[0].text.strip()

#         order_id = oid.split("_")[1]
#         order_obj = Order.objects.get(id=order_id)
#         if status == "Success":
#             order_obj.payment_completed = True
#             order_obj.save()
#             return redirect("/")
#         else:

#             return redirect("/esewa-request/?o_id="+order_id)


class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        name = form.cleaned_data.get("full_name")
        address = form.cleaned_data.get("address")
        fullname = Fullname.objects.create(lastname = name)
        contact = Contactinfo.objects.create(email = email)
        user_ = User.objects.create_user(username = username, password = password)
        account = Account.objects.create(user = user_)
        addressid = Address.objects.create(description = address)
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

class SendReview(CreateView):
    template_name = "review.html"
    form_class = ReviewForm
    success_url = reverse_lazy("ecomapp:home")
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
            Q(name__icontains=kw) | Q(description__icontains=kw))
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


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductlist.html"
    queryset = Item.objects.all().order_by("-id")
    context_object_name = "allproducts"


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
        p = Product.objects.create(producerid = producer, manufacturingdate = manufacturingdate, expirydate = expirydate,
                                    type = prod_type, name = name)
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
        product.num += number
        product.save()
        staff = Staffs.objects.get(userid__accountid__user = self.request.user)
        date = datetime.datetime.now()
        form.instance.supplierid = supplier
        form.instance.productid = product
        form.instance.staffid = staff
        form.instance.date = date
        return super().form_valid(form)