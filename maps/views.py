from django.shortcuts import render

# MPC note: imports go here, e.g., MySQL extension (see next line re install)
# MPC note: ***to import mysql.connector, make sure to install mysql-connector while inside mcit550_project file directory in terminal!
#           ***command for installing in Ubuntu is: pip install mysql-connector-python; once installed, we can import it
import mysql.connector
from decimal import Decimal
import json

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
    mydb = mysql.connector.connect(
        host="cis550-proj.chge9gphb71b.us-east-1.rds.amazonaws.com",
        user="admin",
        password="CIS550_Upenn",
        database="cis550proj"
    )
    mycursor = mydb.cursor()
    
    #querying and formatting mask data for input into chartjs graph
    mycursor.execute("WITH CS1 AS (SELECT cts.Name, cts.State, m.Frequently, m.Always FROM Masks m JOIN Counties cts ON (m.FIPS = cts.FIPS)) SELECT CS1.State, AVG((CS1.Frequently+CS1.Always)*100) AS Perc_High_Frequency FROM CS1 WHERE CS1.State<>'Puerto Rico' GROUP BY CS1.State ORDER BY Perc_High_Frequency DESC")
    tempList = mycursor.fetchall()
    statesMaskName = [item[0] for item in tempList]
    statesMaskPerc = [item[1] for item in tempList]
    
    #querying and formatting sentiment data for input into highchart map
    mycursor.execute("WITH CS2 AS ( WITH CS1 AS ( SELECT cts.Name, cts.State, s.WeekStart, s.NumNegtiveSntmnt FROM Sentiments s JOIN Counties cts ON (s.FIPS = cts.FIPS)) SELECT CS1.State, SUM(CS1.NumNegtiveSntmnt) AS Total_Negative_Sentiment FROM CS1 WHERE CS1.State<>'Puerto Rico' AND CS1.State<>'District of Columbia' GROUP BY CS1.State) SELECT CS2.State, CS2.Total_Negative_Sentiment / st.Population * 1000 AS Per_Capita_NegSentiment FROM CS2 JOIN States st ON (CS2.State = st.Name) ORDER BY CS2.State ASC")
    tempList2 = mycursor.fetchall()    
    statesSentDec = [item[1] for item in tempList2]
    statesSentAbbrev = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    for item in statesSentDec:
        statesSentDec[statesSentDec.index(item)]=float(item)
    jsonListSent=[]
    for i in range(0,len(statesSentAbbrev)):
        jsonListSent.append({'value' : statesSentDec[i], 'code' : statesSentAbbrev[i]})

    jsonFinalMap = json.dumps(jsonListSent)
    

    #in context, we just list python variables we want to use in 
    # our html file, and what we want them to be named in the html file;
    # here, I just use the same name for both
    #showMap='True'
    context={'statesMaskName':statesMaskName, 'statesMaskPerc':statesMaskPerc, 'jsonFinalMap':jsonFinalMap}
    return render(request, 'pageTwo.html', context)

#Zeneng can take ownership and version control of this function and its html page
def pageThree(request):
    return render(request, 'pageThree.html')

#Jesus can take ownership and version control of this function and its html page
def pageFour(request):
    # Getting data from AWS
    mydb = mysql.connector.connect(
        host="cis550-proj.chge9gphb71b.us-east-1.rds.amazonaws.com",
        user="admin",
        password="CIS550_Upenn",
        database="cis550proj"
    )
    count = 0
    abbStatesList = []
    statesNameList = []
    statesPopList = []
    totalVaccinationsList = []
    vaccinationRateList = []
    vaccinationRankList = []
    mycursor = mydb.cursor()
    query = "WITH data_date AS (SELECT DISTINCT date AS date FROM Vaccinations ORDER BY date DESC LIMIT 1) SELECT sta.name AS state, sta.population AS population, COALESCE(vac.total_vaccinations,0) AS total_vaccinations, ROUND(COALESCE(vac.total_vaccinations,0)/sta.population,4) AS vaccination_rate, RANK() OVER (ORDER BY COALESCE(vac.total_vaccinations,0)/sta.population DESC) AS vaccination_rank FROM Vaccinations vac LEFT JOIN States sta ON LOWER(sta.name) = LOWER(vac.state) WHERE date IN (SELECT * FROM data_date)"
    mycursor.execute(query)
    for row in mycursor:
        temp = abbreviations(row[0])
        abbStatesList.insert(count,temp)
        statesNameList.insert(count,row[0])
        statesPopList.insert(count,row[1])
        totalVaccinationsList.insert(count,row[2])
        vaccinationRateList.insert(count,str(row[3]))
        vaccinationRankList.insert(count,row[4])
        count += 1
    context={'statesNameList':statesNameList, 'abbStatesList':abbStatesList, 'statesPopList':statesPopList, 'totalVaccinationsList':totalVaccinationsList, 'vaccinationRateList':vaccinationRateList, 'vaccinationRankList':vaccinationRankList}
    return render(request, 'pageFour.html', context)

#Ken can take ownership and version control of this function and webpage
def pageFive(request):
    mydb = mysql.connector.connect(
        host="cis550-proj.chge9gphb71b.us-east-1.rds.amazonaws.com",
        user="admin",
        password="CIS550_Upenn",
        database="cis550proj"
    )
    mycursor = mydb.cursor()
    
    #querying and formatting mask data for input into chartjs graph
    mycursor.execute("select * from warning_state order by ICU_possible_shortage DESC")
    predicted = mycursor.fetchall()
    print(predicted)
    states = [item[0] for item in predicted]
    ICU_shortage = [int(item[1]) for item in predicted]
    # total_beds = [item[2] for item in predicted]
    # ICU_pred = [item[3] for item in predicted]
    # mycursor.execute("WITH CS1 AS (SELECT cts.Name, cts.State, m.Frequently, m.Always FROM Masks m JOIN Counties cts ON (m.FIPS = cts.FIPS)) SELECT CS1.State, AVG((CS1.Frequently+CS1.Always)*100) AS Perc_High_Frequency FROM CS1 WHERE CS1.State<>'Puerto Rico' GROUP BY CS1.State ORDER BY Perc_High_Frequency DESC")
    # tempList = mycursor.fetchall()
    # states = [item[0] for item in tempList]
    # ICU_shortage = [item[1] for item in tempList]
    
    #querying and formatting sentiment data for input into highchart map
    mycursor.execute("select * from predicted_cases")
    tempList2 = mycursor.fetchall()    
    predictedCases = [item[0] for item in tempList2]
    statesSentAbbrev = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    for item in predictedCases:
        predictedCases[predictedCases.index(item)]=int(item)
    jsonListSent=[]
    for i in range(0,len(statesSentAbbrev)):
        jsonListSent.append({'value' : predictedCases[i], 'code' : statesSentAbbrev[i]})

    jsonFinalMap = json.dumps(jsonListSent)
    

    #in context, we just list python variables we want to use in 
    # our html file, and what we want them to be named in the html file;
    # here, I just use the same name for both
    #showMap='True'
    # context={'states':states, 'ICU_shortage':ICU_shortage,'total_beds':total_beds, 'ICU_pred':ICU_pred, 'jsonFinalMap':jsonFinalMap, 'predicted':predicted}
    context={'states':states, 'ICU_shortage':ICU_shortage,'jsonFinalMap':jsonFinalMap}
    return render(request, 'pageFive.html', context)

#if anyone wants to create additional functions and webpages, feel free (and comment your name on it)

def stateButtonData(request):
    mydb = mysql.connector.connect(
        host="cis550-proj.chge9gphb71b.us-east-1.rds.amazonaws.com",
        user="admin",
        password="CIS550_Upenn",
        database="cis550proj"
    )
    mycursor = mydb.cursor()
    
    #querying and formatting mask data for input into chartjs graph
    mycursor.execute("WITH CS1 AS (SELECT cts.Name, cts.State, m.Frequently, m.Always FROM Masks m JOIN Counties cts ON (m.FIPS = cts.FIPS)) SELECT CS1.State, AVG((CS1.Frequently+CS1.Always)*100) AS Perc_High_Frequency FROM CS1 WHERE CS1.State<>'Puerto Rico' GROUP BY CS1.State ORDER BY Perc_High_Frequency DESC")
    tempList = mycursor.fetchall()
    statesMaskName = [item[0] for item in tempList]
    statesMaskPerc = [item[1] for item in tempList]
    
    #querying and formatting sentiment data for input into map chart
    mycursor.execute("WITH CS2 AS ( WITH CS1 AS ( SELECT cts.Name, cts.State, s.WeekStart, s.NumNegtiveSntmnt FROM Sentiments s JOIN Counties cts ON (s.FIPS = cts.FIPS)) SELECT CS1.State, SUM(CS1.NumNegtiveSntmnt) AS Total_Negative_Sentiment FROM CS1 WHERE CS1.State<>'Puerto Rico' AND CS1.State<>'District of Columbia' GROUP BY CS1.State) SELECT CS2.State, CS2.Total_Negative_Sentiment / st.Population * 1000 AS Per_Capita_NegSentiment FROM CS2 JOIN States st ON (CS2.State = st.Name) ORDER BY CS2.State ASC")
    tempList2 = mycursor.fetchall()    
    statesSentDec = [item[1] for item in tempList2]
    statesSentAbbrev = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    for item in statesSentDec:
        statesSentDec[statesSentDec.index(item)]=float(item)
    jsonListSent=[]
    for i in range(0,len(statesSentAbbrev)):
        jsonListSent.append({'value' : statesSentDec[i], 'code' : statesSentAbbrev[i]})
    jsonFinalMap = json.dumps(jsonListSent)

    #get button input
    clickedState=request.POST.get('clickedState')
    
    #querying and formatting sentiment data for input into lollipop chart
    mycursor.execute("WITH CS1 AS (SELECT s.WeekStart, s.NumNegtiveSntmnt FROM Sentiments s JOIN Counties cts ON (s.FIPS = cts.FIPS) WHERE cts.State=\'"+clickedState+"\') SELECT CS1.WeekStart, SUM(CS1.NumNegtiveSntmnt) AS Weekly_Negative_Sentiment FROM CS1 GROUP BY WeekStart ORDER BY WeekStart ASC")
    tempList3 = mycursor.fetchall()

    clickedXtemp = [item[0] for item in tempList3]    
    clickedYtemp = [item[1] for item in tempList3]
    clickedX = [(item.strftime("%m")+'/'+item.strftime("%d")+'/'+item.strftime("%Y")) for item in clickedXtemp]
    clickedY = [float(item) for item in clickedYtemp]
 
    #showMap='False'
    context={'statesMaskName':statesMaskName, 'statesMaskPerc':statesMaskPerc, 'clickedX':clickedX, 'clickedY': clickedY, 'clickedState':clickedState, 'jsonFinalMap':jsonFinalMap}
    return render(request, 'pageTwo.html', context)

def abbreviations(state_complete_name):
    choices = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District Of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Is': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Virgin Islands': 'VI',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}
    result = choices.get(state_complete_name, 'error')
    return result