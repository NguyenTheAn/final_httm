# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# import flair
# from flair.models import TextClassifier
# from google_trans_new import google_translator  
# translator = google_translator()  
# flair_sentiment = TextClassifier.load('en-sentiment')


class Account(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(db_column='Usersname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)  # Field name made lowercase.
    # role = models.CharField(db_column='Role', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'account'


class Address(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=255, blank=True, null=True)  # Field name made lowercase.
    town = models.CharField(db_column='Town', max_length=255, blank=True, null=True)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'address'
    
    def __str__(self):
        return f"{self.description} {self.street} {self.town} {self.district} {self.city}"

    @property
    def address(self):
        return f"{self.description} {self.street} {self.town} {self.district} {self.city}"


class Author(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    fullnameid = models.OneToOneField('FullName', models.CASCADE, db_column='FullNameID', blank=True, null=True)
    bookproductid = models.ForeignKey('Book', models.CASCADE, db_column='BookProductID')  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'author'


class Banking(models.Model):
    banktransactioncode = models.CharField(db_column='BankTransactionCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paymentid = models.OneToOneField('Payment', models.CASCADE, db_column='PaymentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'banking'


class Book(models.Model):
    page = models.IntegerField(db_column='Page', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    productid = models.OneToOneField('Product', models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.
    genreid = models.ForeignKey('Genre', models.CASCADE, db_column='GenreID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'book'


class Businessstaff(models.Model):
    numproductprocessed = models.IntegerField(db_column='NumProductProcessed', blank=True, null=True)  # Field name made lowercase.
    staffid = models.OneToOneField('Staffs', models.CASCADE, db_column='StaffID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'businessstaff'


class Cartline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey('Item', models.CASCADE, db_column='ItemID')  # Field name made lowercase.
    num = models.IntegerField(db_column='Num', blank=True, null=True)  # Field name made lowercase.
    shoppingcartid = models.ForeignKey('Shoppingcart', models.CASCADE, db_column='ShoppingCartID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'cartline'

    @property
    def sumPrice(self):
        return (self.num * self.itemid.price)


class Cash(models.Model):
    recieve = models.IntegerField(db_column='Recieve', blank=True, null=True)  # Field name made lowercase.
    paymentid = models.OneToOneField('Payment', models.CASCADE, db_column='PaymentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'cash'


class Category(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'category'


class Clothes(models.Model):
    clothtype = models.CharField(db_column='ClothType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ages = models.IntegerField(db_column='Ages', blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=255, blank=True, null=True)  # Field name made lowercase.
    material = models.CharField(db_column='Material', max_length=255, blank=True, null=True)  # Field name made lowercase.
    productid = models.OneToOneField('Product', models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'clothes'


class Contactinfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'contactinfo'


class Customer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.OneToOneField("Users", models.CASCADE, db_column='CustomerID', blank=True, null=True)

    class Meta:
        
        db_table = 'customer'


class CustomerShippingaddress(models.Model):
    customerid = models.OneToOneField(Customer, models.CASCADE, db_column='CustomerID', primary_key=True)  # Field name made lowercase.
    shippingaddressid = models.ForeignKey('Shippingaddress', models.CASCADE, db_column='ShippingAddressID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'customer_shippingaddress'
        unique_together = (('customerid', 'shippingaddressid'))



class Customerreview(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    reviewtime = models.TimeField(db_column='ReviewTime', blank=True, null=True)  # Field name made lowercase.
    isReply = models.BooleanField(default=False)

    class Meta:
        
        db_table = 'customerreview'

    @property
    def sentiment(self):
        return "NEGATIVE"
        # translate_text = translator.translate(self.content, lang_tgt='en')  
        # sentence=flair.data.Sentence(translate_text)
        # flair_sentiment.predict(sentence)
        # total_sentiment = sentence.labels
        # return total_sentiment[0].value

class Electronic(models.Model):
    devicetype = models.CharField(db_column='DeviceType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=255, blank=True, null=True)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=255, blank=True, null=True)  # Field name made lowercase.
    material = models.CharField(db_column='Material', max_length=255, blank=True, null=True)  # Field name made lowercase.
    power = models.CharField(db_column='Power', max_length=255, blank=True, null=True)  # Field name made lowercase.
    voltage = models.CharField(db_column='Voltage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    electriccurrent = models.CharField(db_column='ElectricCurrent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    frequency = models.CharField(db_column='Frequency', max_length=255, blank=True, null=True)  # Field name made lowercase.
    productid = models.OneToOneField('Product', models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'electronic'


class Feedback(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey('Item', models.CASCADE, db_column='ItemID')  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    rate = models.IntegerField(db_column='Rate', validators = [MinValueValidator(0), MaxValueValidator(5)])  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'feedback'
    
    @property
    def relevant(self):
        text = self.content.lower()
        if "giao hàng" in text or "đóng gói" in text or "nhân viên" in text:
            return "non-relevant"
        return "relevant"


class Fullname(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'fullname'

    @property
    def fullname(self):
        return f"{self.lastname} {self.middlename} {self.firstname}"

    def __str__(self):
        return f"{self.lastname} {self.middlename} {self.firstname}"


class Genre(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'genre'


class Historyline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    orderhistoryid = models.ForeignKey('Orderhistory', models.CASCADE, db_column='OrderHistoryID')  # Field name made lowercase.
    orderid = models.ForeignKey('Order', models.CASCADE, db_column='OrderID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'historyline'


class Importingrecord(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplierid = models.ForeignKey('Supplier', models.CASCADE, db_column='SupplierID')  # Field name made lowercase.
    productid = models.ForeignKey('Product', models.CASCADE, db_column='ProductID')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    staffid = models.ForeignKey('Staffs', models.CASCADE, db_column='StaffID')  # Field name made lowercase.
    num = models.IntegerField(db_column='Num', blank=True, null=True)
    price = models.IntegerField(db_column='Price', blank=True, null=True)

    class Meta:
        
        db_table = 'importingrecord'

    @property
    def total(self):
        return self.price*self.num


class Item(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey('Product', models.CASCADE, db_column='ProductID')  # Field name made lowercase.
    price = models.BigIntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products/images/")
    isUpload = models.BooleanField(default=False)

    class Meta:
        
        db_table = 'item'
    
    def __str__(self) -> str:
        return self.productid.name


class Membershiptype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    condition = models.CharField(db_column='Condition', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'membershiptype'


class Message(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    messagesessionid = models.ForeignKey('Messagesession', models.CASCADE, db_column='MessageSessionID', blank=True, null=True)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=255, blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    senderid = models.IntegerField(db_column='SenderID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'message'


class Messagesession(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    salesstaffuserid = models.ForeignKey('Salesstaff', models.CASCADE, db_column='SalesStaffID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'messagesession'

class Orderitem(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    orderid = models.ForeignKey("Order", models.CASCADE, db_column='OrderID')  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    itemid = models.ForeignKey(Item, models.CASCADE, db_column='ItemID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'orderitem'

    @property
    def subTotal(self):
        return self.count*self.itemid.price

class Order(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    taxid = models.ForeignKey('Tax', models.CASCADE, db_column='TaxID')  # Field name made lowercase.
    voucherid = models.ForeignKey('Voucher', models.CASCADE, db_column='VoucherID')  # Field name made lowercase.
    paymentid = models.ForeignKey('Payment', models.CASCADE, db_column='PaymentID')  # Field name made lowercase.
    addressid = models.ForeignKey('Address', models.CASCADE, db_column='AddressID', blank=True, null=True)
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'order'

    @property
    def total(self):
        sum = 0
        for orderitem in Orderitem.objects.filter(orderid__id = self.id):
            sum += orderitem.count * orderitem.itemid.price
        return sum

ORDER_STATUS = (
    ("Đã tiếp nhận đơn hàng", "Đã tiếp nhận đơn hàng"),
    ("Đơn hàng đang được xử lý", "Đơn hàng đang được xử lý"),
    ("Đơn hàng đang đƯợc giao", "Đơn hàng đang đƯợc giao"),
    ("Đơn hàng đã hoàn thành", "Đơn hàng đã hoàn thành"),
    ("Đơn hàng đã bị huỷ", "Đơn hàng đã bị huỷ"),
)


class Orderhistory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'orderhistory'


class Payment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    isComplete = models.BooleanField(blank=True, null=True)
    method = models.CharField(db_column='Method', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'payment'

    def __str__(self):
        return self.method


class Prodimage(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey('Product', models.CASCADE, db_column='ProductID')  # Field name made lowercase.
    image = models.ImageField(upload_to="products/images/")  # Field name made lowercase.

    class Meta:
        
        db_table = 'prodimage'


class Producer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'producer'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    producerid = models.ForeignKey(Producer, models.CASCADE, db_column='ProducerID')  # Field name made lowercase.
    manufacturingdate = models.DateField(db_column='ManufacturingDate', blank=True, null=True)  # Field name made lowercase.
    expirydate = models.DateField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    num = models.IntegerField(db_column='Number', default=0)

    class Meta:
        
        db_table = 'product'

    def __str__(self) -> str:
        return self.name
    
    @property
    def category(self):
        return ProductCategory.objects.get(productid = self).categoryid.name


class ProductCategory(models.Model):
    productid = models.OneToOneField(Product, models.CASCADE, db_column='ProductID', primary_key=True)  # Field name made lowercase.
    categoryid = models.ForeignKey(Category, models.CASCADE, db_column='CategoryID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'product_category'
        unique_together = (('productid', 'categoryid'),)


class Promotion(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.CASCADE, db_column='ItemID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    percent = models.FloatField(db_column='Percent')  # Field name made lowercase.
    expirydate = models.DateField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'promotion'


class Qrcode(models.Model):
    code = models.CharField(db_column='Code', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paymentid = models.OneToOneField(Payment, models.CASCADE, db_column='PaymentID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'qrcode'


class Reviewreply(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=255, blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    customerreviewid = models.ForeignKey(Customerreview, models.CASCADE, db_column='CustomerreviewID', blank=True, null=True)  # Field name made lowercase.
    staffid = models.ForeignKey('Staffs', models.CASCADE, db_column='SalesStaffUsersID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'reviewreply'


class Salesstaff(models.Model):
    numorderprocessed = models.IntegerField(db_column='NumOrderProcessed', blank=True, null=True)  # Field name made lowercase.
    staffid = models.OneToOneField('Staffs', models.CASCADE, db_column='StaffID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'salesstaff'


class Shippingaddress(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    addressid = models.ForeignKey('Address', models.CASCADE, db_column='AddressID', blank=True, null=True)
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'shippingaddress'


class Shippinginfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey(Order, models.CASCADE, db_column='OrderID')  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cost = models.CharField(db_column='Cost', max_length=255, blank=True, null=True)  # Field name made lowercase.
    delaydate = models.CharField(db_column='DelayDate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'shippinginfo'


class Shoppingcart(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'shoppingcart'
    
    @property
    def total(self):
        s = 0
        for cartline in Cartline.objects.filter(shoppingcartid__id = self.id):
            s += cartline.sumPrice
        return s


class Staffs(models.Model):
    position = models.CharField(db_column='Position', max_length=255, blank=True, null=True)  # Field name made lowercase.
    salary = models.BigIntegerField(db_column='Salary', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    workingtime = models.IntegerField(db_column='WorkingTime', blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField('Users', models.CASCADE, db_column='UsersID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'staffs'


class Supplier(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'supplier'

    def __str__(self) -> str:
        return self.name


class Tax(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'tax'


class Users(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accountid = models.OneToOneField('Account', models.CASCADE, db_column='AccountID', blank=True, null=True)
    contactinfoid = models.OneToOneField('ContactInfo', models.CASCADE, db_column='ContactInfoID', blank=True, null=True)
    fullnameid = models.OneToOneField('FullName', models.CASCADE, db_column='FullNameID', blank=True, null=True)
    addressid = models.OneToOneField('Address', models.CASCADE, db_column='AddressID', blank=True, null=True)

    class Meta:
        
        db_table = 'users'


class Voucher(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discountpercent = models.FloatField(db_column='DiscountPercent', blank=True, null=True)  # Field name made lowercase.
    maxamount = models.IntegerField(db_column='MaxAmount', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'voucher'

    def __str__(self):
        return f"{self.name}"


class Warehousestaff(models.Model):
    numbills = models.IntegerField(db_column='NumBills', blank=True, null=True)  # Field name made lowercase.
    staffid = models.OneToOneField('Staffs', models.CASCADE, db_column='StaffID', primary_key=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'warehousestaff'


class Wishlist(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey(Customer, models.CASCADE, db_column='CustomerID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'wishlist'


class Wishlistline(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.CASCADE, db_column='ItemID', blank=True, null=True)
    wishlistid = models.ForeignKey(Wishlist, models.CASCADE, db_column='WishListID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'wishlistline'
