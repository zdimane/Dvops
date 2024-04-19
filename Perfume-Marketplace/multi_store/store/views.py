from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from store.models import Product,Order,Category,Rate,Product,Customer,Brand
from django.conf import settings
from django.core.mail import send_mail
import random
import math

# Cart
class Cart(View):
    def get(self, request):
        c = request.session.get("cart")
        if (c):
            id = list(request.session.get("cart").keys())
            products = Product.get_product_by_id(id)
            return render(request, "cart.html", {"cart": products})
        else:
            noprd = "There no products in the cart. Let's add some products"
            return render(request, "cart.html", {"noprd": noprd})
    
    def post(self, request):
        c = request.session.get("cart")
        prdid = request.POST.get("prdid")
        c.pop(prdid)
        request.session["cart"] = c
        id = list(c.keys())
        if (id == []):
            noprd = "There no products in the cart. Let's add some products"
            return render(request, "cart.html", {"noprd": noprd})
        else:
            products = Product.get_product_by_id(id)
            return render(request, "cart.html", {"cart": products})
    # Checkout
class CheckOut(View):
    def post(self, request):
        status = " "
        adress = request.POST.get("adress")
        total = request.POST.get("total")
        cart = request.session.get("cart")
        product_id = Product.get_product_by_id(list(cart.keys()))
        
        if (adress == ""):
            status = "please enter your adress for placing the order"
            return render(request, "cart.html", {"status": status, "type": False, "cart": product_id})
        else:
            customer = request.session.get("customer_id")
            customer_info = Customer.customer_info(str(customer))
            
            for p in product_id:
                info = Order(
                    product = p,
                    customer =  customer_info,
                    quantity =  cart.get(str(p.id)),
                    price =  p.price,
                    adress =  adress,
                    phone =  customer_info.phone,
                )
                Order.place_order(info)
           
            request.session["cart"] = {}
            return render(request, 'pay.html',{"p":product_id, "total":int(total)}) 
        # Forgotpass
class Forgotpass(View):

    def get(self, request):
        return render(request, "forgotpass.html", {"flag":False})

    def post(self, request):
        email = request.POST.get("email")
        otp = random.randint(1111,9999)
        subject = 'OTP'
        message = f"this is your OTP(one time password). Do not share this with anyone.{otp}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        return render(request, "forgotpass.html", {"flag":True, "otp":otp, "email":email})
# Index
class Index(View):
    def post(self, request):
        amt = request.POST.get("amount")
        prd_id = request.POST.get("prdid")
        if (prd_id != None):
            cart = request.session.get("cart")  
            if cart:
                q = cart.get(prd_id)
                if q:
                    q = int(q) + int(amt)
                else:
                    q = amt
                cart[prd_id] = q
            else:
                cart = {} 
                cart[prd_id] = amt
            
            request.session["cart"] = cart
            return redirect("index")
        
        applied_filters = []
        prds = Product.get_all_products()
        cat_ty = Category.get_category_type()
        brands = Product.get_brands()
        b = list()
        for br in brands:
            b.append(br["brand"])
        sort = ["Low To High", "High To Low"]
        gender = ["Male", "Female"]
        
        genderr = request.POST.get("gender")
        if (genderr):
            applied_filters.append(genderr)
            prds = Product.gen_filter(genderr, prds)
        sorting = request.POST.get("sort")
        if (sorting):
            applied_filters.append(sorting)
            prds = Product.sorting(sorting, prds)
        brands = request.POST.getlist("brands")
        if (brands):
            applied_filters.append(brands)
            prds = Product.brandfilter(brands, prds)
        category = request.POST.getlist("category")
        if (category):
            applied_filters.append(category)
            prds = self.filter_category(prds, category)
        search = request.POST.get("search")
        if (search):
            s = []
            s.append(search)
            prds = Product.get_all_products()
            prds1 = self.filter_category(prds, s)
            if (prds1):
                return render(request, "index.html", {"products": prds1, "gender":gender, "sort":sort, "category":cat_ty, "brands":b})
            else:
                prds2 = Product.brandfilter(s, prds)
                if (prds2):
                    return render(request, "index.html", {"products": prds2, "gender":gender, "sort":sort, "category":cat_ty, "brands":b})
                else:
                    prds3 = Product.gen_filter(search, prds)
                    if (prds3):
                        print("c")
                        return render(request, "index.html", {"products": prds3, "gender":gender, "sort":sort, "category":cat_ty, "brands":b})
                    else:
                        pass
        return render(request, "index.html", {"products": prds, "gender":gender, "sort":sort, "category":cat_ty, "brands":b, "applied_filters":applied_filters})

    def get(self, request):
        cart = request.session.get("cart")  
        if cart == False:
            cart = {}

        prds = Product.get_all_products()
        self.add_rating(prds)
        cat_ty = Category.get_category_type()
        brands = Product.get_brands()
        b = list()
        for br in brands:
            b.append(br["brand"])
        sort = ["Low To High", "High To Low"]
        gender = ["Male", "Female"]
        return render(request, "index.html", {"products": prds, "gender":gender, "sort":sort, "category":cat_ty, "brands":b})

    def filter_category(self, prds, category):
        num = []
        for c in category:
            cat_num = Category.get_cat_num(c)
            num.append(cat_num)
        flatten_list = sum(num, [])
        prds = Product.typee(flatten_list, prds)
        return prds
    
    def add_rating(self, prds):
        for p in prds:
            pr = Rate.objects.filter(product = p)
            len = pr.count()
            if(len != 0):
                prate = 0
                for p_obj in pr:
                    prate = prate + p_obj.rating
                p.rating = math.floor(prate / len)
                p.save()
            else:
                p.rating = 0
                p.save()
# Login
class Login(View):
    def get(self, request):
         return render(request, "login.html")

    def post(self, request):
        user = request.POST.get("user")
        password = request.POST.get("password")

        x = user.find("@")
        flag = "email"
        if (x == -1):
            flag = "phone"
        userdata = Customer.checkk(user, flag)

        error = None
        if (not user):
            error = "Enter either phone or email"
        elif (not password):
            error = "enter the password"
        elif (userdata == None):
            error = "enter correct " + flag
        elif (check_password(password, userdata.password) == False):
            error = "enter the correct password"
        
        if (error == None):
            request.session["customer_id"] = userdata.id
            if (flag == "email"):
                request.session["customer_user"] = userdata.email
            elif (flag == "phone"):
                request.session["customer_user"] = userdata.phone

            return redirect("main") 
        else:
            data = {
                "error": error,
                "user": user
            }
            return render(request, "login.html", data)

def logout(request):
    request.session.clear()
    return  redirect("login")
class Main(View):
    def get(self, request):
        prds = Product.get_all_products()
        p_show = []
        count = 0
        for p in prds:
            if (count < 9):
                p_show.append(p)
                count = count + 1
        brands = []
        celeb_brand = []

        br = Brand.get_all_brands()
        for b in br:
            if (b.category == "normal"):
                brands.append(b)
            else:
                celeb_brand.append(b)
        return render(request, "main.html", {"prds": p_show, "brands":brands, "celeb_brand": celeb_brand})
    def post(self, request):
        pass
# Ordermanage
class Ordermanage(View):
    def get(self, request):
        orders = Order.get_all_orders()
        return render(request, "ordermanage.html", {"order":orders})
    
    def post(self, request):
        status = request.POST.get("status")
        id = request.POST.get("id")
        orders = Order.get_all_orders()
        Order.status_update(id, status)
        return render(request, "ordermanage.html", {"order":orders})
# Orders
class OrderView(View):
    def get(self, request):
        customer = request.session.get("customer_id")
        order = Order.by_customer(customer)
        o = []
        for od in order:
            chk_rate = Rate.check_order_id(od)
            if (chk_rate):
                pass
            else:
                o.append(od)
        return render(request, "orders.html", {"order":o})
    
    def post(self, request):
        o_idd = request.POST.get("o_idd")
        p_idd = request.POST.get("p_idd")
        rating1 = request.POST.get("rate1")
        rating2 = request.POST.get("rate2")
        rating3 = request.POST.get("rate3")
        rating4 = request.POST.get("rate4")
        rating5 = request.POST.get("rate5")
        val = request.POST.get("sub_btn")
        
        customer = request.session.get("customer_id")
        order = Order.get_order_by_id(o_idd)
        orders = Order.by_customer(customer)
        o = []
        for od in orders:
            chk_rate = Rate.check_order_id(od)
            if (chk_rate):
                pass
            else:
                o.append(od)

        if (val == "RATE"):
            flag = 0
            if (rating1 != None):
                flag = 1
            elif (rating2 != None):
                flag = 2
            elif (rating3 != None):
                flag = 3
            elif (rating4 != None):
                flag = 4
            elif (rating5 != None):
                flag = 5
        
            p = Product.get_product(p_idd)
            c = Customer.customer_info(str(customer))
    
            for i in p:
                rate = Rate (
                    rating = flag,
                    product = i,
                    customer = c,
                    order = order
                )
            Rate.place_order(rate)
            Order.rating_update(o_idd, flag)
            return redirect("orders")

        elif (val == "NOT NOW"):
            return render(request, "orders.html", {"order":o, "my_class":"hide_class"}) 
# Otp
class Otp(View):

    def post(self, request):
        otp_given = request.POST.get("otp_given")
        otp = request.POST.get("otp")
        email = request.POST.get("email")

        if (int(otp_given) == int(otp)):
            userdata = Customer.info(email)
            request.session["customer_id"] = userdata.id
            request.session["customer_user"] = userdata.email
            return redirect("index")
        else:
            status = "the OTP you entered was incorrect. Please try again"
            return render(request, "forgotpass.html", {"flag":False, "status":status})
# Products
class Products(View):
    def post(self, request):
        amt = request.POST.get("amount")
        prd_id = request.POST.get("prdid")
        if (prd_id != None):
            p_obj = Product.get_product(prd_id)
            cat = p_obj[0].category
            type2 = Category.get_category_type2(cat)

            cart = request.session.get("cart")  
            if cart:
                q = cart.get(prd_id)
                if q:
                    q = int(q) + int(amt)
                else:
                    q = amt
                cart[prd_id] = q
            else:
                cart = {} 
                cart[prd_id] = amt
            
            request.session["cart"] = cart
        return render(request, "products.html", {"product":p_obj[0], "cat_type":type2})
        
    def get(self, request):
        product_id = request.GET.get("product_id")
        if (product_id != None):
            p_obj = Product.get_product(product_id)
            cat = p_obj[0].category
            type2 = Category.get_category_type2(cat)
        return render(request, "products.html", {"product":p_obj[0], "cat_type":type2})
# Profile
class Profile(View):
    def get(self, request):
        info = request.GET.get("info")

        idd = request.session.get("customer_id")
        c_info = Customer.customer_info(idd)

        if (info == "personal"):
            return render(request, "profile.html", {"information":c_info, "type":"personal"})
        elif (info == "order"):
            o_info = Order.by_customer(c_info)
            return render(request, "profile.html", {"orders":o_info, "type":"order"})
        elif (info == "purchased"):
            o_info = Order.by_customer(c_info)
            p_o = []
            for o in o_info:
                if (o.status == "delivered"):
                    p_o.append(o)
                    r = Rate.check_order_id(o)
            return render(request, "profile.html", {"purchased":p_o, "type":"purchased"})
        return render(request, "profile.html")

    def post(self, request):
        o_idd = request.POST.get("o_idd")
        p_idd = request.POST.get("p_idd")
        rating1 = request.POST.get("rate1")
        rating2 = request.POST.get("rate2")
        rating3 = request.POST.get("rate3")
        rating4 = request.POST.get("rate4")
        rating5 = request.POST.get("rate5")
        
        customer = request.session.get("customer_id")
        orders = Order.by_customer(customer)
        order = Order.get_order_by_id(o_idd)

        flag = 0
        if (rating1 != None):
            flag = 1
        elif (rating2 != None):
            flag = 2
        elif (rating3 != None):
            flag = 3
        elif (rating4 != None):
            flag = 4
        elif (rating5 != None):
            flag = 5
        
        p = Product.get_product(p_idd)
        c = Customer.customer_info(str(customer))
    
        for i in p:
            rate = Rate (
                rating = flag,
                product = i,
                customer = c,
                order = order
            )
        Rate.place_order(rate)
        Order.rating_update(o_idd, flag)
        return redirect("profile")
# Sign
class Signup(View):
    def get(self, request):
        return render(request, "signup.html")
    def post(self, request):

        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        pnum = request.POST.get("pnum")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        checkbox = request.POST.get("checkbox")
    
        value = {
            "fname": fname, "lname": lname,
            "pnum": pnum, "email": email }

        error = self.validatemethod(fname, lname, pnum, email, gender, password1, password2, checkbox)
        
        if (error == None):
            customer = Customer(first_name=fname, last_name=lname, email=email, phone=pnum,  gender=gender, password=password1)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect("login")
        else:
            data = {
                "error": error,
                "values": value
            }
            return render(request, "signup.html", data)
    
    def validatemethod(self, fname, lname, pnum, email, gender, password1, password2, checkbox):
        error = None 

        if (not fname):
            error = "first name required"
        elif (not lname):
            error = "last name required"
        elif (not pnum):
            error = "phone number is required"
        elif (len(pnum) != 10):
            error = "phone number is invalid"
        elif (not email):
                error = "email is required"
        elif (not gender):
                error = "gender is required"
        elif(not password1):
            error = "password is must"
        elif(password1 != password2):
            error = "passwords do not match"
        elif (len(password1) < 7):
            error = "password needs to be of 7 characters or more"
        elif(checkbox == None):
            error = "agree to the terms and conditions"
        elif (pnum):
            p = Customer.objects.filter(phone=pnum)
            if (p):
                error = "An account already exists with this phone number"
        elif (email):
            e = Customer.objects.filter(email=email)
            if (e):
                error = "An account already exists with this email"
        return error