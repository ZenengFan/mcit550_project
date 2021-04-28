from django.shortcuts import render
import mysql.connector
from decimal import Decimal
import json

# Establishing conneciton to AWS RDS
mydb = mysql.connector.connect(
        host="cis550-proj.chge9gphb71b.us-east-1.rds.amazonaws.com",
        user="admin",
        password="CIS550_Upenn",
        database="cis550proj"
    )

#homepage function
def index(request):
    return render(request,'index.html')

#Mike can take ownership and version control of this function/webpage
def pageTwo(request):
   
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
    
    context={'statesMaskName':statesMaskName, 'statesMaskPerc':statesMaskPerc, 'jsonFinalMap':jsonFinalMap}
    return render(request, 'pageTwo.html', context)

#Zeneng can take ownership and version control of this function and its html page
def pageThree(request):
    mycursor = mydb.cursor()
    
    #querying and formatting mask data for input into chartjs graph
    mycursor.execute("select * from warning_state order by ICU_possible_shortage DESC")
    predicted = mycursor.fetchall()
    states = [item[0] for item in predicted]
    ICU_shortage = [int(item[1]) for item in predicted]
    
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
    
    context={'states':states, 'ICU_shortage':ICU_shortage,'jsonFinalMap':jsonFinalMap}
    return render(request, 'pageThree.html', context)

#Jesus can take ownership and version control of this function and its html page
def pageFour(request):
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

#helper functions

#function for using buttons in pageTwo's bar graph to select additional state data in lollipop graph
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
 
    context={'statesMaskName':statesMaskName, 'statesMaskPerc':statesMaskPerc, 'clickedX':clickedX, 'clickedY': clickedY, 'clickedState':clickedState, 'jsonFinalMap':jsonFinalMap}
    return render(request, 'pageTwo.html', context)

#helper function for filling pageFour map labels
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