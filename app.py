from flask import *
import pymysql
# create app
app=Flask(__name__)
app.secret_key="jddaidadaody734826847dads$^&#*"
# define connection
connection=pymysql.connect(host="localhost",user="root",password="",database="maxwell_projectdb")
# home page
@app.route('/')
def main():
    return render_template('index.html')

# create save vendor route
@app.route("/save_vendor" ,methods=['POST','GET'])
def Save_vendor():
    # check if user has posted any data  
        if request.method=='POST':
            #TODO commit
            # get data from the form
            name=request.form['name']
            email=request.form['email']
            password=request.form['password']
            phone=request.form['phone']
            location=request.form['location']
            desc=request.form['desc']
            
            # get the image
            # check if image has been uploaded
            if 'image' not in request.files:
                return render_template("signup.html",message="Image not uploaded")
        
            image=request.files['image'] #get image from the form
            # store the image inside static folder
            image.save('static/images/'+image.filename)
            img_name=image.filename
            if not name or not email or not password or not phone or not location or not desc:
                return render_template("signup.html",message="Please fill in all the records")
            # create the cursor
            cursor=connection.cursor()
            sql='insert into vendors(vendor_name,vendor_email,vendor_password,vendor_contact,vendor_location,profile_image,vendor_desc) values(%s,%s,%s,%s,%s,%s,%s)'
            try:
                # execute
                cursor.execute(sql,(name,email,password,phone,location,img_name,desc))
                connection.commit()
                cursor.close()
                return render_template("signup.html",message="Vendor saved successfully")
            except:
                return render_template("signup.html",message="Failed: Vendor not saved")
        else:
            return render_template("signup.html")
    
# signinroute
@app.route("/signin",methods=['POST','GET'])
def Signin():
    # check if the user has posted any records
    if 'key' in session:
        
        return render_template("vendor.html")
    else:
        if request.method=='POST':
            # get data from the form
            username=request.form['username']
            password=request.form['password']
            # create a cursor function
            cursor=connection.cursor()
            # sql
            sql='select * from vendors where vendor_name=%s and vendor_password=%s'
            # execute the sql query
            values=(username,password)
            cursor.execute(sql,values)
            # check if vendor exists
            if cursor.rowcount==0:
                return render_template("signup.html",message="Wrong credentials \n User Does Not exist")
            else:
                session['key']=username
                # fetch the records of the vendor
                data=cursor.fetchone()
                # other sessions
                session['id']=data[0]
                session['email']=data[2]
                session['desc']=data[5]
                session['location']=data[6]
                session['image']=data[7]
                print(data)
                return render_template("vendor.html",vendor=data)
        
        else:
            return render_template("signup.html")
    
  
#   logout route vendor
@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/signin")  
  
  #   logout route vendor
@app.route("/logout/user")
def Logout_user():
    session.clear()
    return redirect("/login")  

# add product route
@app.route("/add_product",methods=['POST','GET'])
def Add_product():
    if 'key' not  in session:
        
        return redirect("/signin")
    else: 
        if request.method =='POST':
            #TODO
            # get data from form
            name=request.form['product_name']
            vendor_id=request.form['vendor_id']
            category=request.form['product_category']
            brand=request.form['product_brand']
            cost=request.form['product_cost']
            discount=request.form['product_discount']
            desc=request.form['product_desc']
            
            # input validation
            if not name or not vendor_id or not category or not brand or not cost or not discount or not desc:
                return "Please provide all the product details"
            # get the image
            image=request.files['product_image']
            image.save('static/images/'+image.filename)
            image_url=image.filename
            # create cursor function
            cursor=connection.cursor()
            sql='insert into products (vendor_id,product_name,product_desc,product_cost,product_discount,product_category,product_brand,image_url) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            # execute sql wuery
            cursor.execute(sql,(vendor_id,name,desc,cost,discount,category,brand,image_url))
            connection.commit()
            return 'Product saved \n <a href="/signin" >Go Back</a>'
        else:
            return render_template("add_product.html")

# getproducts route
@app.route('/getproducts',methods=['GET'])
def GetProducts():
    # create the cursor
    # Electronics
    cursor_electronics=connection.cursor()
    # Shoes
    cursor_shoes=connection.cursor()
    sql_electronics='select * from products where product_category="Electronics"'
    # Shoes sql
    sql_shoes='select * from products where product_category="Shoes"'
    # execute the sql query
    cursor_electronics.execute(sql_electronics)
    # shoes execute
    cursor_shoes.execute(sql_shoes)
    # fetch all the products
    electronics=cursor_electronics.fetchall()
    # fetch shoes
    shoes=cursor_shoes.fetchall()
    # check if there are products to display
    if cursor_electronics.rowcount==0:
        return render_template('getproducts.html',message='No Products to display')
    else:
        
        # products=jsonify(products) #convert products into json format
        # return products
        return render_template('getproducts.html',data=electronics,shoes=shoes)
    
        
# fetch products by vendor_id
@app.route("/vendor_products/<vendor_id>",methods=['GET'])
def Vendor_products(vendor_id):
    if 'key' not in  session:
        return redirect("/signin")
    else:
        
        sql='select * from products where vendor_id =%s'
        cursor=connection.cursor()
        # execute the sql query
        cursor.execute(sql,vendor_id)
        # fetch the products
        vendor_products=cursor.fetchall()
        # check if there are products to display
        if cursor.rowcount==0:
            return render_template("vendor_products.html",error="No products Available")
        else:
            # return jsonify(vendor_products)
            return render_template("vendor_products.html",data=vendor_products)
        
# delete product 
@app.route("/delete/<product_id>",methods=['POST','GET','DELETE'])
def Delete_product(product_id):
    if 'key' not in session:
        return redirect("/signin")
    else:
        sql='delete from products where product_id=%s'
        # cursor
        cursor=connection.cursor()
        # execute
        cursor.execute(sql,product_id)
        connection.commit()
        return "Product Deleted "
    

# view product based on categories

# create another route for user to signin
@app.route("/login",methods=['POST','GET'])
def Login():
    if request.method =='POST':
        #TODO
        # get the posted data
        data=request.form['name']
        password=request.form['password']
        # create cursor
        cursor=connection.cursor()
        # sql 
        sql='select * from users where (username=%s or email=%s or phone=%s) and password=%s'
        # execute the sql query
        values=(data,data,data,password)
        cursor.execute(sql,values)
        # check if user exists
        if cursor.rowcount==0:
            return render_template("signin.html",message="Wrong login Credentials")
        else:
            # fetch
            user=cursor.fetchone()
            username=user[0]
            session['user']=username
            return redirect("/getproducts")
        
    else:
        return render_template("signin.html")
    
# single item route
@app.route("/single_item/<product_id>",methods=['POST','GET'])
def Single_item(product_id):
    sql='select * from products where product_id=%s'
    # cursor
    cursor=connection.cursor()
    cursor.execute(sql,product_id)
    # fetch the product
    product=cursor.fetchone()
    print(product)
    category=product[6]
    print(category)
    sql_similar='select * from products where product_category=%s'
    cursor_similar=connection.cursor()
    cursor_similar.execute(sql_similar,category)
    similar_product=cursor_similar.fetchall()
    print(similar_product)
    return render_template("single_item.html",product=product,similar=similar_product)
#justpaste.it/a4lzc

@app.route("/register",methods=['POST','GET'])
def Register():
    return render_template("register.html")

# mpesa integration route
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
@app.route("/mpesa_payment",methods=['POST','GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "u5fdN03MHa698AzeW3rZWzMFlwkPFHGj"
        consumer_secret = "vaoNoGPXaS4qelsP"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379" #test paybil
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount":amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href="/getproducts" class="btn btn-dark btn-sm">Back to Products</a>'
    else:
        return render_template("single_html.html")

@app.route("/edit/<username>",methods=['POST','GET'])
def Edit(username):
    if request.method =='POST':
        # TODO
        name=request.form['username']
        email=request.form['email']
        password=request.form['password']
        phone=request.form['phone']
        # sql query to update 
        sql_update ='update users set username=%s, email=%s,password=%s,phone=%s where username=%s'
        cursor_update=connection.cursor()
        cursor_update.execute(sql_update,(name,email,password,phone,username))
        connection.commit()
        return "Records Updated /n "
    else: 
        sql='select * from users where username=%s'
        cursor=connection.cursor()
        cursor.execute(sql,username)
        user=cursor.fetchone()
        return render_template("edit.html",user=user)
# C-create -insert -POST
# R-Read - select- GET
#U-Update -update- PUT
#D delete -delete- DELETE

# save feedback
# post
import functions
@app.route("/change_password",methods=['GET','POST'])
def Change_password():
    if request.method=='POST':
        #TODO
        # get the posted data
        email=request.form['email']
        password=request.form['password']
        confirm=request.form['confirm']
        
        # check if password is equal toconfirm
        if password != confirm:
            return render_template("change_password.html",message="Passwords do not match")
        else:
            
            # check if vendor exists
            cursor_vendor=connection.cursor()
            sql_vendor='select * from vendors where vendor_email=%s'
            cursor_vendor.execute(sql_vendor,email)
            vendor=cursor_vendor.fetchone()
            if cursor_vendor.rowcount ==0:
                return render_template("change_password.html",message="User with this email does not exist")
            else:
                # create OTP(One Time Password)
                #TODO
                OTP=functions.generate_random()
                sql_update="update vendors set vendor_password=%s where vendor_email=%s"
                # using OTP
                sql='update vendors set vendor_password=%s where email=%s'
                cursor_update=connection.cursor()
                cursor_update.execute(sql_update,(OTP,email))
                connection.commit()
                # call the send sms function
                functions.send_sms('+254703353657', f'Your new password is {OTP}')
                return render_template("change_password.html",message="Password updated successfully")
    else:
        return render_template("change_password.html")

# run app
if __name__ =="__main__":
    app.run(debug=True,port=7000)