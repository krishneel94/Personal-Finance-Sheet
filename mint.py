import webbrowser
import pyautogui
import time
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from tkinter import Tk
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import math

class hillendale: #personal class used to calc equity in my home - mint only does current home value
    hillendale_purch = "2020-05-29 11:59:59" #the date we closed the hillendale mortage
    hillendale_obj = datetime.datetime.strptime(hillendale_purch, '%Y-%m-%d %H:%M:%S') #convert the date string into a datetime object
    equity_obj = datetime.datetime.now() #get todays date as a datetime obj
    mortgage = 111.16
    down_payment = 8918.0 + 1250.0

class Krish: #class used to express my known finances 
    rent = 800
    utils = 100
    my_expense = 400
    date_expense = 300
    emp_401k = 150
    roth_401k = 675
    roth = 375
    espp = 1125
    mom = 300
    tax_health = 2171
    expected_expenses = rent + utils + my_expense + date_expense
    pretax_income = XXXX

#define reused variables - should I make a time class?
secs_between_keys = .25
ts = time.gmtime() #get strings for current month/year
equity_date = time.strftime("%Y-%m",ts)
p_filename = equity_date + "-mint.csv"
dir = time.strftime("%Y/%m",ts)
filename = dir + "/" + p_filename #create the rel path for the mint csv data
month = time.strftime("%m",ts)
year = time.strftime("%Y",ts)
history =  year + "/history.csv"
mbal = month + " Balance"
debt = 0.0

#this is used to determine the number of days since close date in order to determine equity built in
def equity_calc(current_date, close_date, down_payment, mortgage):   
    time_dif = str(close_date - current_date)
    time_dif = int(time_dif[0]+time_dif[1])
    res = down_payment + (math.ceil(time_dif/30) * mortgage)
    return res

#this appends a new month column to my history tracker
def history_append(df1, df2):
    df1['Account'] = df2['Account']
    df1[mbal] = df2['Balance'].astype('float64')
    df1.to_csv(history, index=False)
    return df1

#used to plot savings accounts to visually track goals
def plot_savings(kind,fund_name,color,goal,hist_df):
    ax = hist_df.plot(kind=kind,x='index', y=[fund_name], color=color)
    ax.set_ylim(0,goal)
    temp_f = hist_df[fund_name][len(hist_df)-1]
    temp_percent = (temp_f/goal)*100
    ax.text(0,goal, fund_name + ': ${}/$'.format(temp_f) + str(goal), fontsize=14)
    ax.text(0,(goal*.75), '{}% to goal!'.format(str(temp_percent)[:4]), fontsize=14)
    plt.savefig(year + '/' + month + '/img' +'/{}.jpg'.format(fund_name))
    plt.close()

#method to handle directory creation
def makedir(path):
    try: #make a new month dir
        os.makedirs(path)
    except FileExistsError: #if it exists already ignore the error
        pass

#call the equity calc method to do just that type of int or float
hillendale_equity = equity_calc(hillendale.equity_obj, hillendale.hillendale_obj, hillendale.down_payment, hillendale.mortgage)

#make some directories
makedir(dir)
makedir(dir+'/img')
login = True


if login is True:
    #open chrome
    webbrowser.open('https://accounts.intuit.com/index.html?offering_id=Intuit.ifs.mint&namespace_id=50000026&redirect_url=https%3A%2F%2Fmint.intuit.com%2Foverview.event%3Futm_medium%3Ddirect%26cta%3Dnav_login_dropdown%26ivid%3D1e19d2d8-23e0-468c-b222-a980b7a2dc97%26adobe_mc%3DMCMID%253D28919876010070450850228591355723009559%257CMCAID%253D2F6E08320515A421-60000824ADAF4799%257CMCORGID%253D969430F0543F253D0A4C98C6%252540AdobeOrg%257CTS%253D1591752696%26ivid%3D1e19d2d8-23e0-468c-b222-a980b7a2dc97',1)
    time.sleep(3)

    #begin login
    pyautogui.hotkey('ctrl', 'a') #select page
    time.sleep(1)
    pyautogui.keyDown('delete')
    pyautogui.typewrite('krishneel_sahdeo@yahoo.com', interval=secs_between_keys) #username
    pyautogui.keyDown('tab') #go to next bar
    pyautogui.typewrite('Pleasework$94\n', interval=secs_between_keys) #password
    time.sleep(4)

    #allow some time for mint to refresh balances
    time.sleep(100)

    #get acc info
    pyautogui.hotkey('ctrl', 'a') #select page
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'c') #copy
    time.sleep(.5)
    root = Tk()
    root.withdraw()
    monies = root.clipboard_get()
    time.sleep(1)
    pyautogui.hotkey('alt', 'tab')

    #output to file
    with open(filename, "w+", encoding="utf-8") as f:
        f.write(monies)




#begin file manipulation
file_cnt = 0 #will use this to keep track of list pos

#save a copy of the file
with open(filename, "r") as f:
    cp = f.readlines() #remember cp is a LIST

#find where there's reference to money - put in new list
new_list = [] #init empty list
for x in cp:
    if '$' in x[0] or '-' in x[0]:
        for i in range(0,len(x)): # strip unneccessary comma and add one for csv purpose
            if x[i] == ',':
                x = x[:i] + x[i+1:] #strip comma
            if x[i] == '$':
                x = x[:i] + x[i+1:] #strip $            
            if x[i].isalpha():
                x = x[:i] + ',' + x[i:] #add comma
                break
        if 'Hillendale' in x: #personal - remove for public...replaces Mint's est home value with my true equity share
            x = str(hillendale_equity) + ',Hillendale St Equity\n'
            new_list.insert(file_cnt, x) #add balance info to new list
        elif 'ASSET' in x:
            continue #do not add assets from mint
        elif 'DEBT' in x:
            leng = (len(x))
            num = leng - 7        
            debt = float(x[:num]) #save debt into a float var
        elif 'NET WORTH' in x: #end loop, don't need data beyond this
            break # end loop ignore net worth from mint
        else:
            new_list.insert(file_cnt, x) #add balance info to new list
        file_cnt+=1 #increment my pos counter
new_list.insert(0, 'Balance,Account\n') #label the csv table

#overwrite csv with sorted data
with open(dir + '/' +'tmp_' + p_filename, "w+") as f:
    for x in new_list: 
        f.write(x) 


#load current month data
monthframe = pd.read_csv(dir + '/' +'tmp_' + p_filename)
os.remove(dir + '/' +'tmp_' + p_filename)

#add correct networth add a method for this?
net_worth = pd.DataFrame() #create a df called networth
#net_worth = monthframe[:-1] 
net_worth = monthframe #copy the entire dataframe
liquid = pd.DataFrame()
liquid = monthframe[:-2] #copy but remove bottom 2 rows - keep in mind debt doesnt get added
df = pd.DataFrame({"Account": ['NET WORTH'], "Balance": [str(net_worth['Balance'].sum())]}) #calculate networth
df1 = pd.DataFrame({"Account": ['LIQUID'], "Balance": [str(liquid['Balance'].sum())[0:8]]}) #calculate liquidable cash
monthframe = monthframe.append(df, ignore_index=True) #append to original dataframe
monthframe = monthframe.append(df1, ignore_index=True) #append to original


#create a history.csv for the current year if one does not already exist
if not os.path.exists(history):
    with open(history, "w+") as f: #create file
        f.write("Account," + mbal) #create columns
    history_frame = pd.read_csv(history) #read in the file as a dataframe
    history_append(history_frame, monthframe) #apppend month frame to the new df
    #print(history_frame)
    
elif os.path.exists(history): #if history for year exists just append new month info
    history_frame = pd.read_csv(history)
    with open(history, "r") as f: 
        first_line = f.readline() #read first line of existing history file
        if mbal in first_line: #if the current month exists in history
            print("Data for the month already exists in history!")
            login = False
            #print(history_frame)
            pass
        else: #if current month does not exist in history
            history_frame = history_append(history_frame, monthframe)
            #print(history_frame)

#transpose dataframe and create necessary plots
hist_t = history_frame.set_index('Account').T
hist_t =  hist_t.reset_index()


#modify the parameters to represent your true account names from mint and your personal goals
#feel free to also change the colors
#for different types of graphs refer to matlibplot although this method is specific for bar or barh
plot_savings('bar','House Fund','Orange',200000, hist_t)
plot_savings('bar','Emergency Fund','DarkGreen',9000, hist_t)
plot_savings('bar','Wedding','LightBlue',40000, hist_t)

#plot line graph of liquidity vs net worth BROKEN???
#hist_t.plot(x='index', y=['LIQUID', 'NET WORTH']) #liquidity plot
#plt.savefig(year + '/' + month + '/img' +'/net.jpg')
#plt.close()

print(history_frame)
#user interface
print('Your debt this month is: {}'.format(debt))
vee = float(input("How much of this is charged to Vee?"))
total_debt_paid =  float(input("In total, how much are you paying down debt?"))
erroneous = float(input("Any expeditures not calced here? Real Estate and extra venmo charges?"))

total_expenses = (total_debt_paid + erroneous + Krish.rent + Krish.utils) - vee
budget = Krish.expected_expenses - total_expenses
if budget > 0:
    spendingis = "Monthly budget spending under by"
elif budget < 0:
    spendingis = "Monthly budget spending over by"
else: 
    spendingis = "Monthly budget spending as expected"

# print(spendingis + "{}".format(budget))
leftover_debt = debt + total_debt_paid  
# print('Leftover debt is: {}'.format(leftover_debt))

#to add budget spend tracker
#name = history_frame.iloc[len(history_frame) - 1]
total_budget = 0
if 'Budget Tracker' in hist_t:
    history_frame[mbal][len(history_frame)-1] = budget
    history_frame.to_csv(history, index=False)

    
    total_budget = float(hist_t['Budget Tracker'].sum())
    #total_budget = total_budget + budget 
    #df3 = pd.DataFrame({"Account": ['Budget Tracker'], mbal: [float(budget)]}) #calculate networth
    #history_frame = history_frame.append(df3, ignore_index=True)
    #test = history_frame['Budget Tracker'][mbal]

else:
    print('work to do')
    df3 = pd.DataFrame({"Account": ['Budget Tracker'], mbal: [float(budget)]}) #calculate networth
    history_frame = history_frame.append(df3, ignore_index=True)
    history_frame.to_csv(history, index=False)


#print('Net Budget Tracking is: {}'.format(total_budget))
if total_budget > 0:
    spendingis1 = "Net budget spending is under by"
elif total_budget < 0:
    spendingis1 = "Net budget spending is over by"
else: 
    spendingis1 = "Net budget spending is as expected"
#TODO
#track venmo spenditures 
#close browser automatically
#open html doc

#create an html document to visualize data
html = history_frame.to_html(index=False)
with open(year + '/' + month + '/' + year + '-' + month +'-report.html', "w+") as f: #create file
    html_text = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <style>
    /* Remove the navbar's default margin-bottom and rounded borders */ 
    .navbar {{
      margin-bottom: 0;
      border-radius: 0;
    }}
    
    /* Add a gray background color and some padding to the footer */
    footer {{
      background-color: #f2f2f2;
      padding: 25px;
    }}
  </style>
</head>
<body>

<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">

      <a class="navbar-brand" href="#">Portfolio</a>
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">Home</a></li>

      </ul>
      <ul class="nav navbar-nav navbar-right">

      </ul>
    </div>
  </div>
</nav>

<div class="jumbotron">
  <div class="container text-center">
    <h1>Finance Snapshot - {0}/{1} </h1>      
    <p>{2}: {3} </p>
    <p>{4}: {5} </p>
  </div>
</div>
  
<div class="container-fluid bg-3 text-center">    
  <h3>Progress...</h3><br>
  <div class="row">
    <div class="col-sm-3">
      <p>House Fund</p>
      <img src="img/House Fund.jpg" class="img-responsive" style="width:100%" alt="Image">
    </div>
    <div class="col-sm-3"> 
      <p>Emergency Fund</p>
      <img src="img/Emergency Fund.jpg" class="img-responsive" style="width:100%" alt="Image">
    </div>
    <div class="col-sm-3"> 
      <p>Wedding Fund</p>
      <img src="img/Wedding.jpg" class="img-responsive" style="width:100%" alt="Image">
    </div>
    <div class="col-sm-3">
      <p>Growth x Time</p>
      <img src="img/Net.jpg" class="img-responsive" style="width:100%" alt="Image">
    </div>
  </div>
</div><br>

<footer class="container-fluid text-center">
  <p>History</p>
</footer>

</body>
</html>
""".format(month,year,spendingis1,total_budget,spendingis,budget)
#append to html file
    f.writelines(html_text)
    f.write(html)