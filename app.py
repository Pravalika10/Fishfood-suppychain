from flask import Flask, render_template, request, session, redirect, url_for
import pymysql

app = Flask(__name__)
app.secret_key = '!hv@cRsh0nU'


class Merchant:
    name = ""
    username = ""
    password = ""
    organisation = ""
    abn = None

    def __init__(self, name, usrnm, passwd, abn, org):
        self.name = name
        self.username = usrnm
        self.password = passwd
        self.abn = abn
        self.organisation = org


class Customer:
    name = ""
    email = ""
    username = ""
    password = ""

    def __init__(self, name, email, usrnm, passwd):
        self.name = name
        self.email = email
        self.username = usrnm
        self.password = passwd


class dataFish:
    product_id = ""
    species = ""
    weight = ""
    L1 = ""
    L2 = ""
    L3 = ""
    height = ""
    width = ""
    storage_temperature = ""
    estimated_storage_life_in_months = ""
    nutrients = ""
    best_before_calculated = ""
    storage_affecting_factor = ""
    price = ""

    def __init__(self, product_id, species, weight, L1, L2, L3, height, width, storage_temperature, estimated_storage_life_in_months, nutrients, best_before_calculated, storage_affecting_factor, price):
        self.product_id = product_id
        self.species = species
        self.weight = weight
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.height = height
        self.width = width
        self.storage_temperature = storage_temperature
        self.estimated_storage_life_in_months = estimated_storage_life_in_months
        self.nutrients = nutrients
        self.best_before_calculated = best_before_calculated
        self.storage_affecting_factor = storage_affecting_factor
        self.price = price


class Sql:
    SERVER = "localhost"
    USR = "root"
    PWD = "mypass123"
    DB = "Fishery"
    GET_DATA_QRY = "Select product_id,species,weight,L1,L2,L3,height,width,storage_temperature,estimated_storage_life_in_months,nutrients,best_before_calculated,storage_affecting_factor,price from newfishes"
    MERCH_SIGNUP_QRY = "Insert into merchant (name, organisation, username, password,abn) values('{}','{}','{}','{}','{}')"
    GET_MERCH = "Select name, organisation, username, password,abn from merchant where isConfirmed is NULL"
    GET_REG_MERCH = "Select count(*) from merchant where isConfirmed is True and "
    GET_SINGLE_MERCH = "Select name, organisation, username, password,abn from merchant where username = {}"
    GET_REG_CUST = "Select count(*) from customer where "
    CUST_SIGNUP_QRY = "Insert into customer (name, email, username, password) values('{}','{}','{}','{}')"
    Fish_DATA_QRY = " Insert into newfishes (product_id,species,weight,L1,L2,L3,height,width,storage_temperature,estimated_storage_life_in_months,nutrients,best_before_calculated,storage_affecting_factor,price) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
    MERCH_APPROVAL_QRY = "UPDATE merchant SET isConfirmed = (var1) WHERE username = (var2) values('{}','{}')"
    # INSERT_FISH_DATA="Insert into newfishes("

    def getData(self):
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.GET_DATA_QRY)
                data = cursor.fetchall()
                conn.commit()
                return data

    def insertMerchant(self, merchant):
        # try:
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                print(self.MERCH_SIGNUP_QRY.format(merchant.name, merchant.organisation,
                      merchant.username, merchant.password, merchant.abn))
                cursor.execute(self.MERCH_SIGNUP_QRY.format(
                    merchant.name, merchant.organisation, merchant.username, merchant.password, merchant.abn))
                conn.commit()
                return True
    # def
        # except:
        #     return False
    # def insertCustomer(self,customer):
    #     with pymysql.connect(host=self.SERVER, user = self.USR, password=self.PWD, db=self.DB) as conn:
    #         with conn.cursor(as_dict = True) as cursor:
    #             print(self.CUST_SIGNUP_QRY.format(customer.name,customer.email,customer.username,customer.password))
    #             cursor.execute(self.CUST_SIGNUP_QRY.format(customer.name,customer.email,customer.username,customer.password))
    #             cursor.commit()
    #             return True

    def insertCustomer(self, customer):
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                print(self.CUST_SIGNUP_QRY.format(customer.name,
                      customer.email, customer.username, customer.password))
                cursor.execute(self.CUST_SIGNUP_QRY.format(
                    customer.name, customer.email, customer.username, customer.password))
                conn.commit()
                return True

    def insertFishData(self, newfishes):
        # try:
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                # print(f"{fishdata}")
                cursor.execute(self.Fish_DATA_QRY.format(newfishes.product_id, newfishes.species, newfishes.weight, newfishes.L1, newfishes.L2, newfishes.L3, newfishes.height, newfishes.width,
                               newfishes.storage_temperature, newfishes.estimated_storage_life_in_months, newfishes.nutrients, newfishes.best_before_calculated, newfishes.storage_affecting_factor, newfishes.price))
                conn.commit()
                return True

    def insertApprovedMerchant(self, username, isApproved):
        # try:
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                print(f"{username} Approval Processing")
                # cursor.execute(self.MERCH_APPROVAL_QRY.format(merchant.name,merchant.organisation,merchant.username,merchant.password,merchant.abn))
                print(
                    f"Update merchant set isConfirmed = {isApproved} where username = {username}")
                cursor.execute(
                    f"Update merchant set isConfirmed = '{isApproved}' where username = '{username}'")
                conn.commit()
                return True
        # except:
        #     return False

    def getMerchantData(self, user):
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.GET_SINGLE_MERCH.format(user))
                data = cursor.fetchall()
                conn.commit()
                return data

    def getAllMerchantData(self):
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.GET_MERCH)
                data = cursor.fetchall()
                conn.commit()
                return data

    def getRegisteredUsers(self, username, password):
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                print(
                    f"{self.GET_REG_MERCH} username='{username}' and password='{password}'")
                cursor.execute(
                    f"{self.GET_REG_MERCH} username='{username}' and password='{password}'")
                data = cursor.fetchall()
                conn.commit()
                val = str(data)[2]
                if int(val) == 1:
                    return True
                else:
                    return False

    def getRegisteredCustomers(self, username, password):
        with pymysql.connect(host=self.SERVER, user=self.USR, password=self.PWD, db=self.DB) as conn:
            with conn.cursor() as cursor:
                print(
                    f"{self.GET_REG_CUST} username='{username}' and password='{password}'")
                cursor.execute(
                    f"{self.GET_REG_CUST} username='{username}' and password='{password}'")
                data = cursor.fetchall()
                conn.commit()
                val = str(data)[2]
                if int(val) == 1:
                    return True
                else:
                    return False


def getAbns():
    with open('abns.txt', 'r') as f:
        return [abn.replace(" ", "") for abn in f.read().split("\n")]


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/customerHome', methods=['GET', 'POST'])
def customerHome():
    fish_data = Sql().getData()
    return render_template('customerHome.html', data=fish_data, header=["product_id", "species", "weight", "L1", "L2", "L3", "height", "width", "storage_temperature", "estimated_storage_life_in_months", "nutrients", "best_before_calculated", "storage_affecting_factor", "price"])


@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    fish_data = Sql().getData()
    return render_template('marketplace.html', data=fish_data, header=["product_id", "species", "weight", "L1", "L2", "L3", "height", "width", "storage_temperature", "estimated_storage_life_in_months", "nutrients", "best_before_calculated", "storage_affecting_factor", "price"])


@app.route('/verify', methods=['POST'])
def verfiy_approval():
    global isLogged
    print(f"{request.form['merchant']} ::::::::::::::::::::::::::::::")
    username = str(request.form['merchant']).split(",")[2][2:-1]
    if request.form['merchant'] != pymysql.NULL and request.form['submit'] != pymysql.NULL:
        isLogged = True
        sql = Sql()
        sql.insertApprovedMerchant(username, request.form['submit'])
        data = sql.getAllMerchantData()
        return render_template("adminHome.html", merchants=data, header=["Name", "Organisation", "Username", "Password", "ABN"])
    else:
        return "<html><body>error</body></html>"


def populateRegisteredUsers(data):
    for record in data:
        merchant = Merchant(record[0], record[2],
                            record[3], record[4], record[1])
        registeredUsers[record[2]] = merchant
        registeredAbns.append(int(record[4]))


@app.route('/populateListing', methods=['POST'])
def populateListing():
    global isLogged
    # if isLogged:
    #     isLogged = False
    #     return redirect(url_for('index'))
    if "ifadmin" in request.form:
        if request.form['user'] == "admin" and request.form['pass'] == "admin@123":
            isLogged = True
            sql = Sql()
            data = sql.getAllMerchantData()
            session['username'] = request.form['user']

            return render_template("adminHome.html", merchants=data, header=["Name", "Organisation", "Username", "Password", "ABN"])
        else:
            return "<html><body>error</body></html>"
    else:
        if Sql().getRegisteredUsers(request.form['user'], request.form["pass"]):
            isLogged = True
            session['username'] = request.form['user']
            return render_template("merchantHome.html")
            # else:
            #     return "<html><body>Authentication Error: Bad Username or password </body></html>"
        elif Sql().getRegisteredCustomers(request.form['user'], request.form["pass"]):
            isLogged = True
            session['username'] = request.form['user']
            return render_template("customerHome.html")
        else:
            return "<html><body>Authentication Error: User Not registered, please Signup</body></html>"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signupForm.html")


@app.route('/two', methods=['GET', 'POST'])
def two():
    return render_template("cusMer.html")


@app.route('/cust', methods=['GET', 'POST'])
def cust():
    return render_template("customer.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("newlogin.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/saveFishData', methods=['POST'])
def saveFishData():
    # fishData=f'INSERT INTO newfishes(product_id,species,weight,L1,L2,L3,height,width,storage_temperature,estimated_storage_life_in_months,nutrients,best_before_calculated,storage_affecting_factor,price) values ('+request.form["product_id"],request.form["species"],request.form["weight"],request.form["L1"],request.form["L2"],request.form["L3"],request.form["height"],request.form["width"],request.form["storage_temperature"],request.form["estimated_storage_life_in_months"],request.form["nutrients"],request.form["best_before_calculated"],request.form["storage_affecting_factor"],request.form["price"]+')'
    newfishes = dataFish(request.form["product_id"], request.form["species"], request.form["weight"], request.form["L1"], request.form["L2"], request.form["L3"], request.form["height"], request.form["width"],
                         request.form["storage_temperature"], request.form["estimated_storage_life_in_months"], request.form["nutrients"], request.form["best_before_calculated"], request.form["storage_affecting_factor"], request.form["price"])
    # print(request.form["species"])
    sql = Sql()
    if sql.insertFishData(newfishes):
        return render_template('merchantHome.html')
    else:
        return "<p><b> Error occured: Unable to insert customer, Contact admin. </b><p>"


@app.route('/registerUser', methods=['POST'])
def registerUser():
    # if request.form["abn"].replace(" ","") in abns:
    # if request.form["user"] not in registeredUsers and request.form["abn"] not in registeredAbns:
    merchant = Merchant(request.form["firstname"]+" "+request.form["lastname"],
                        request.form["user"], request.form["pass"], request.form["abn"], request.form["org"])
    sql = Sql()
    registeredUsers[request.form["user"]] = merchant
    registeredAbns.append(request.form["abn"])
    if sql.insertMerchant(merchant):
        return render_template('newlogin.html')
    else:
        return "<p><b> Error occured: Unable to insert merchant, Contact admin. </b><p>"
    #     else:
    #         return "<p><b> User or Abn already registered</b></p>"
    # else:
    #     return "<p><b> Error occured: ABN not registered with admin, contact admin </b><p>"


@app.route('/registerCustomer', methods=['POST'])
def register():
    customer = Customer(
        request.form["name"], request.form["email"], request.form["user"], request.form["pass"])
    sql = Sql()
    # registeredCustomers[request.form["user"]] = customer
    if sql.insertCustomer(customer):
        return render_template('newlogin.html')
    else:
        return "<p><b> Error occured: Unable to insert customer, Contact admin. </b><p>"


#     if 'user' in request.form and 'pass' in request.form:
#         username = request.form['user']
#         password = request.form['pass']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
#         account = cursor.fetchone()
#         if account:
#             msg = 'Account already exists !'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address !'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers !'
#         elif not username or not password or not email:
#             msg = 'Please fill out the form !'
#         else:
#             cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
#             mysql.connection.commit()
#             msg = 'You have successfully registered !'
#     elif request.method == 'POST':
#         msg = 'Please fill out the form !'
#     return render_template('login1.html')

if __name__ == '__main__':
    isLogged = False
    # abns = getAbns()
    registeredUsers = {}
    registeredAbns = []
    populateRegisteredUsers(Sql().getAllMerchantData())
    app.run()
