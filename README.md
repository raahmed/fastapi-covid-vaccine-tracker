# Exploring Covid Vaccine Type Popularity with Python using FastAPI, Fire, Azure Database for PostgreSQL-Flexible Server(Preview) and Azure Web Apps

In this code, I will explore how FastAPI, Fire and Azure can be combined to gather meaningful insights from COVID vaccination data. We will use Fire to load publicly available data into Azure **Azure Database for PostgreSQL**-**Flexible Server** which is currently in public preview. We will then use FastAPI to query data, perform meaningful transformation on them and build APIs to share these insights with the world. These APIs will be hosted on Azure WebApps.

## Prerequisites
- Azure Subscription (e.g. [Free](https://aka.ms/azure-free-account) or [Student](https://aka.ms/azure-student-account))
- Latest [pip](https://pip.pypa.io/en/stable/installing/) package installer
- Python 3.6+

## Install the Python libraries

To install all the necessary libraries for this program, open a terminal or command prompt and run the command `pip install -r requirements.txt`.

## Get database connection information

First, we are going to set up our CLI to connect to Azure in a manner that is secure and one which will allow us to quickly delete resources to avoid incurring additional cost.

First, log into Azure through the following command. It should open up a browser where you can add your credentials.

```
az login
```

Next, we will set up Azure to create resources in an organized manner. To do this, we will create a resource group. A resource group can be imagined as a container with all our work. At the end of this README, we can delete this one container and get rid of any cost-incurring resources easily. Finally, we will turn on parameter persistence - this will ensure that we do not have to set default parameters repeatedly.

```
az group create --location westus --name eurocovidvaccine
az config param-persist on
```

After you have finished setting up Azure, it is time to set up your Azure Database for Flexible Server. To do this, enter the following command. Note that the firewall settings are set to public access for simplicity of demonstration - you can limit these in the future by seeing the documentation. Give the command some time to execute.

``` 
az postgres flexible-server create --public-access all
```

When the command finishes executing, copy the JSON output of the output - paying particular attenion to the dbname, hostname, username and password:
![image](https://user-images.githubusercontent.com/25991359/125120292-1d42a800-e0a7-11eb-8199-b14d625a3a1b.png)


## Data Reference:

1. The data in this repository is a snapshot of https://www.ecdc.europa.eu/sites/default/files/documents/Variable_Dictionary_VaccineTracker-03-2021.pdf as of June 30, 2021.


## How to run the Python examples

1. First, we need to figure out what data we want to put into our database. For this demo, I download data from the ECDC website and added my sample CSV to this repository. You can obtain this data by cloning this repository:
   ```
   git clone https://github.com/raahmed/fastapi-covid-vaccine-tracker.git
   cd fastapi-covid-vaccine-tracker
   ```

2. Next, we will use the contents of the JSON you saved when provisioning the database above in the "Get database connection information" section.

![image](https://user-images.githubusercontent.com/25991359/125120292-1d42a800-e0a7-11eb-8199-b14d625a3a1b.png)
Insert the information from the JSON into the following string:
   
  ```
   export SERVER_NAME='server176472475.postgres.database.azure.com'
   export ADMIN_USERNAME='myusername'
   export ADMIN_PASSWORD='mypassword'
   export DB_NAME="flexibleserverdb"
 ```
   
Then execute the line below - no need to substitute the values in the line below - it will be done automatically:
```
   export CONNECTION_STRING "host=${SERVER_NAME} port=5432 dbname=postgres user=${ADMIN_USERNAME} password=${ADMIN_PASSWORD} sslmode=require"
```

3. Once that is done, execute the following line:

```
   echo $CONNECTION_STRING
```

You should see an output string with the correctly formatted information.

Copy this output string and set it aside.

4. Next, let's create a table and load some data from a local CSV file, [covid_data.csv](covid_data.csv). The [loadData](dataworks.py#L27) function of the dataworks.py program will automatically connect to the database (using our connectionString), create our tables if they don't exist, and then use a COPY command to load our data into the `raw_data` table from `data.csv`. All we need to do is invoke that function with the name of the data file. 

```
   python3 dataworks.py loadData covid_data.csv
```
5. However, if you open the [covid_data.csv](covid_data.csv), it contains a lot of information. Specifically, the columns inclde a lot of information we will probably not need for exploring vaccine popularity. So, we can populate a new table called vaccine_data. The [populateVaccineData](dataworks.pyL#83) function inserts only the necessary information for our analysis into this smaller and more efficient data set.

6. Let's do something more interesting with this new dataset. The function [getCountryVaccineCounts](dataworks.py#119) obtains the total count of each vaccine type that is administered.

We can execute 
```
   python3 dataworks.py getCountryVaccineCounts
```

and we will see some numerical analysis.

7. Now, absolute numbers are not very human-friendly. Percentages are far better. 

Thankfully, there is a program that will give us the total percentage share of the market for each vaccine type. You can invoke it:
   
   
```
   python3 dataworks.py getCountryVaccinePercentages
```

## Connecting Our Analysis to the Web
### Setting up Local FastAPI Server:

1. At this point, you might be interested in sharing your insights and data learnings with others. This is where FastAPI can help us quickly build an API to share our analysis with others.

You can quickly build an endpoint that will:

1) Return all the vaccine counts
2) Return all the vaccine percentages
3) Return the most popular vaccine per country
4) Return the least popular vaccine by country

All of these functions are shown in [main.py](main.py)!

However, in order to execute them and see their output locally, you need to run the server. To do so, execute the following:

```
   uvicorn main:app --reload
```

Then navigate to any of the following locally to see some interesting data trends:

localhost:8000/
localhost:8000/getpercentages
localhost:8000/mostpopular
localhost:8000/leastpopular



### Showing your code to the World:

#### Deploy Website Code 
You might be interested in sharing your vaccine analysis with the world! To do this, you need to deploy your FastAPI and dataworks code to the internet. To do this, execute the following in your Terminal:

```
   az webapp up --name europecovidvaccine
```

Please note - the value of the name flag needs to be unique across all of Azure! ProTip: try to add some random numbers to your preferred name.

Wait until the deployment the is complete. Your command should tell you to visit your website, which will be based on your application name (for example:  europecovidvaccine.azurewebsites.net)

### Set up database connection on Azure

Navigate to portal.azure.com and log in.
In the search bar, write "App Services" and click the icon below:

![image](https://user-images.githubusercontent.com/25991359/125123280-4ebd7280-e0ab-11eb-9f73-64902555fac9.png)

Next, pick your website name from the list (or search for it):

![image](https://user-images.githubusercontent.com/25991359/125123401-76acd600-e0ab-11eb-852a-eda07e34ff59.png)

Next, click "Settings" under "Configuration". ProTip: Use "Command + F" to search for "Configuration" if you are having trouble navigating the UI.

![image](https://user-images.githubusercontent.com/25991359/125123580-b07ddc80-e0ab-11eb-92e5-6b6f0a8563c5.png)

Next, click "Add new Setting"

![image](https://user-images.githubusercontent.com/25991359/125123663-cab7ba80-e0ab-11eb-98e6-d507e9f02741.png)

Next, used the copied output of your previous ``` echo $CONNECTION_STRING ``` command from the previous step and paste it:

![image](https://user-images.githubusercontent.com/25991359/125123910-2aae6100-e0ac-11eb-8638-27dbc8f3b2a3.png)

Next, click "OK"

![image](https://user-images.githubusercontent.com/25991359/125123999-49145c80-e0ac-11eb-87be-81c8a16a53eb.png)

Next, click "SAVE" - this is in addition to the OK!

Double-check that the save worked by refreshing the page. It should look as follows (with the CONNECTION_STRING present and the "SAVE" icon disabled)

![image](https://user-images.githubusercontent.com/25991359/125124147-7eb94580-e0ac-11eb-8da0-f29bc7df0a4e.png)


### Set up Server connection on Azure

Finally, navigate to "General Settings" inside of the Configuration view:

![image](https://user-images.githubusercontent.com/25991359/125124252-a6a8a900-e0ac-11eb-8b18-1605ba2f296b.png)


In the "Startup Command" section, copy and paste the following command:

```
   gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app
```

Then click "Save" and then click "OK" when you are warned about application restart.

![image](https://user-images.githubusercontent.com/25991359/125124391-d8ba0b00-e0ac-11eb-9e72-a433d2944d88.png)

Your web applicaiton will now start up with the right command!

## Show your website to the world!

You can now go to your Azure website and see the API endpoints!

## Troubleshooting:

If you are are having trouble with your website, please navigate to the log stream in the Azure Portal for important debugging information:

![image](https://user-images.githubusercontent.com/25991359/125125415-69ddb180-e0ae-11eb-9a9b-3171179b6f4f.png)


## (Optional) Delete/Stop your Azure Resources

If you have created an Azure resources for the purposes of this lab and you *do not* want to keep and continue to be billed for it, you can delete via the terminal:

```
   az group delete --name eurocovidvaccine --no-wait
```


## Want to Learn More about PostgreSQL Flexible Server on Azure

If you want to dig deeper and undestand what all PostgreSQL Flexible Server on Azure has to offer , the Flexible Server [documents](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/) are a great place to start.

## Want to Learn More about WebApps on Azure

If you want to dig deeper and undestand what all PostgreSQL Flexible Server on Azure has to offer , the Flexible Server [documents](https://docs.microsoft.com/en-us/azure/app-service/) are a great place to start.

## Reference:
- Code inspired by:
https://github.com/Azure-Samples/azure-python-labs/edit/main/4-postgres/README.md
