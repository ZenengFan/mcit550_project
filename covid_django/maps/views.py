from django.shortcuts import render

# MPC note: imports go here, e.g., MySQL extension (see next line re install)
# MPC note: ***to import mysql.connector, make sure to install mysql-connector while inside mcit550_project file directory in terminal!
#           ***command for installing in Ubuntu is: pip install mysql-connector-python; once installed, we can import it
import mysql.connector

# Create your views here.

def index(request):
    
    #code to make db connection --- will need to edit this so it's outside the function, so that we don't need to call it inside each function.
    #for now, we can just include it in each function as needed, unless someone feels like fixing it now
    mydb = mysql.connector.connect(
        host="cis550-proj.chge9gphb71b.us-east-1.rds.amazonaws.com",
        user="admin",
        password="CIS550_Upenn",
        database="cis550proj"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Name FROM States")
    #fetchall cmd is tricky, its result comes in form of list of tuples.
    #In this case, the javascript requires a simple list, so we reformat
    #using index function.
    statesNameList = [item[0] for item in mycursor.fetchall()]
    mycursor.execute("SELECT Population FROM States")
    statesPopList = [item[0] for item in mycursor.fetchall()]

    #in context, we just list python variables we want to use in 
    # our html file, and what we want them to be named in the html file;
    # here, I just use the same name for both
    context={'statesNameList':statesNameList, 'statesPopList':statesPopList}
    return render(request,'index.html',context)

#Mike can take ownership and version control of this function/webpage
def pageTwo(request):
    return render(request, 'pageTwo.html')

#Zeneng can take ownership and version control of this function and its html page
def pageThree(request):
    return render(request, 'pageThree.html')

#Jesus can take ownership and version control of this function and its html page
def pageFour(request):
    return render(request, 'pageFour.html')

#Ken can take ownership and version control of this function and webpage
def pageFive(request):
    return render(request, 'pageFive.html')

#if anyone wants to create additional functions and webpages, feel free (and comment your name on it)