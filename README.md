# -InterIntel

## 1.	Give examples of different integration protocols you have come across and give example scripts in python 3 on how to achieve each one. (10 pts) 


## 2.	Give a walkthrough of how you will manage a data streaming application sending one million notifications every hour 
## while giving examples of technologies and configurations you will use to manage load and asynchronous services. (10 pts)

Stream processing is a data processing technology used to collect, store, and manage continuous streams of data as it’s produced or received. 
One the advantages of using this process is that ingesting data needs minimal compute resources, each invite is an event that is added to the 
stream with no need to calculate state. 
We will be using Amazon Kinesis Data Stream platform more specifically Kinesis Data Firehose service. Firehose service handles loading data and 
pushing into data stores and analytic tools. 
Data producers can put data into Amazon Kinesis data streams using the Amazon Kinesis Data Streams APIs, Amazon Kinesis Producer Library (KPL),
or Amazon Kinesis Agent.
Amazon Kinesis Data Generator: Put sample data into a Kinesis data stream or Kinesis data firehose using the Amazon Kinesis Data Generator.
Amazon Kinesis Data Streams provides two APIs for putting data into an Amazon Kinesis stream: PutRecord and PutRecords. PutRecord allows a single 
data record within an API call and PutRecords allows multiple data records within an API call.

Amazon Kinesis Producer Library (KPL) is an easy to use and highly configurable library that helps you put data into an Amazon Kinesis data stream. 
Amazon Kinesis Producer Library (KPL) presents a simple, asynchronous, and reliable interface that enables you to quickly achieve high producer 
throughput with minimal client resources.

Amazon Kinesis Agent is a pre-built Java application that offers an easy way to collect and send data to your Amazon Kinesis stream. 
You can install the agent on Linux-based server environments such as web servers, log servers, and database servers. The agent monitors certain 
files and continuously sends data to your stream.

Step 1: To create a stream
          •	Sign in to the AWS Management Console and open the Kinesis console at https://console.aws.amazon.com/kinesis.
          •	Choose Data Streams in the navigation pane.
          •	In the navigation bar, expand the Region selector and choose a Region.
          •	Choose Create Kinesis stream.
          •	Enter a name for your stream (for example, InterIntelStream).
          •	Enter 1 for the number of shards (a shard is the base throughput unit of an Amazon Kinesis data stream.), but leave Estimate the number of shards you'll need collapsed.
          •	Choose Create Kinesis stream.
N/B: 
On the Kinesis streams list page, the status of your stream is CREATING while the stream is being created. When the stream is ready to use, the status changes to ACTIVE. Choose the name of your stream. In the page that appears, the Details tab displays a summary of your stream configuration. The Monitoring section displays monitoring information for the stream.
## Step 2: Create IAM Policy and User
•	Locate the Amazon Resource Name (ARN) for the new stream. You can find this ARN listed as Stream ARN at the top of the Details tab. The ARN format is as follows:
		<bold>arn:aws:kinesis:region:account:stream/name<bold>
region: The Region code; for example, us-west-2.
Account: The AWS account ID
Name: The name of the stream from Step 1: Create a Data Stream, which is InterIntelStream.
Determine the ARN for the DynamoDB table to be used by the consumer (and created by the first consumer instance). The Region and account are from the same place as the previous step, but this time name is the name of the table created and used by the consumer application.
To create an IAM user
                    •	Open the IAM console at https://console.aws.amazon.com/iam/.
                    •	On the Users page, choose Add user.
                    •	For User name, type InterIntelStream.
                    •	For Access type, choose Programmatic access, and then choose Next: Permissions.
                    •	Choose Attach existing policies directly.
                    •	Search by name for the policy that you created. 
                    •	Select the box to the left of the policy name, and then choose Next: Review.
                    •	Review the details and summary, and then choose Create user.
                    •	Copy the Access key ID, and save it privately. Under Secret access key, choose Show, and save that key privately also.
                    •	Paste the access and secret keys to a local file in a safe place that only you can access.
## Step 3: Download and Build the Implementation Code
•	Download the source code to your computer.
•	Create a project in your favorite IDE with the source code, adhering to the provided directory structure.
•	Add the following libraries to the project:
                            Amazon Kinesis Client Library (KCL)
                            AWS SDK
                            Apache HttpCore
                            Apache HttpClient
                            Apache Commons Lang
                            Apache Commons Logging
                            Guava (Google Core Libraries For Java)
                            Jackson Annotations
                            Jackson Core
                            Jackson Databind
                            Jackson Dataformat: CBOR
                            Joda Time

## Step 4: Implement the Producer
The application uses the real-world scenario of Inter Intel Stream monitoring. Refer to the source code and review the following information.
InterIntelStream class
An individual Inter Intel stock trade is represented by an instance of the InterIntel class. This instance contains attributes such as the ticker 
symbol, price, number of shares, the type of the trade (buy or sell), and an ID uniquely identifying the trade. This class is implemented for you.
Stream record 
A stream is a sequence of records. A record is a serialization of a StockTrade instance in JSON format.
StockTradeGenerator class
StockTradeGenerator has a method called getRandomTrade() that returns a new randomly generated stock trade every time it is invoked. 
This class is implemented for you.

## StockTradesWriter class
The main method of the producer, StockTradesWriter continuously retrieves a random trade and then sends it to Kinesis Data Streams by 
performing the following tasks:
       •	Reads the stream name and Region name as input.
       •	Creates an AmazonKinesisClientBuilder.
       •	Uses the client builder to set the Region, credentials, and client configuration.
       •	Builds an AmazonKinesis client using the client builder.
       •	Checks that the stream exists and is active (if not, it exits with an error).
In a continuous loop, calls the StockTradeGenerator.getRandomTrade() method and then the sendStockTrade method to send the trade to the stream 
every 100 milliseconds.

## Step 5: Implement the Consumer

The consumer application process Real-Time Stock Data Using KPL and KCL 1.x continuously processes the Inter Intel stock trades stream 
that you created in Step 4: Implement the Producer. It then outputs the most popular stocks being bought and sold every minute. 
The application is built on top of the Kinesis Client Library (KCL), which does much of the heavy lifting common to consumer apps. 

## StockTradesProcessor class
Main class of the consumer, provided for you, which performs the following tasks:
       Reads the application, stream, and Region names, passed in as arguments.
       Reads credentials from ~/.aws/credentials.
Creates a RecordProcessorFactory instance that serves instances of RecordProcessor, implemented by a StockTradeRecordProcessor instance.
Creates a KCL worker with the RecordProcessorFactory instance and a standard configuration including the stream name, credentials, and application name.
The worker creates a new thread for each shard (assigned to this consumer instance), which continuously loops to read records from Kinesis 
Data Streams. It then invokes the RecordProcessor instance to process each batch of records received.

## StockTradeRecordProcessor class

Implementation of the RecordProcessor instance, which in turn implements three required methods: initialize, processRecords, and shutdown.
As the names suggest, initialize and shutdown are used by the Kinesis Client Library to let the record processor know when it should be ready to 
start receiving records and when it should expect to stop receiving records, respectively, so it can do any application-specific setup and termination 
tasks. The code for these is provided for you. The main processing happens in the processRecords method, which in turn uses processRecord for each record. 
This latter method is provided as mostly empty skeleton code for you to implement in the next step, where it is explained further.
Also of note is the implementation of support methods for processRecord: reportStats, and resetStats, which are empty in the original source code.
The processRecords method is implemented for you, and performs the following steps:

<br/>

For each record passed in, calls processRecord on it.
If at least 1 minute has elapsed since the last report, calls reportStats(), which prints out the latest stats, and then resetStats() which 
clears the stats so that the next interval includes only new records.
Sets the next reporting time.
If at least 1 minute has elapsed since the last checkpoint, calls checkpoint().
Sets the next checkpointing time.
This method uses 60-second intervals for the reporting and checkpointing rate. For more information about checkpointing, see Additional Information About the Consumer.
 ## StockStats class
This class provides data retention and statistics tracking for the most popular stocks over time. This code is provided for you and contains the following methods:
                                addStockTrade(StockTrade): Injects the given StockTrade into the running statistics.
                                toString(): Returns the statistics in a formatted string.
This class keeps track of the most popular stock by keeping a running count of the total number of trades for each stock and the maximum count. It updates these counts whenever a stock trade arrives.

## Step 6: Finishing Up
Because you are paying to use the Kinesis data stream, make sure that you delete it and the corresponding Amazon DynamoDB table when you are done with it. 
Nominal charges occur on an active stream even when you aren't sending and getting records. This is because an active stream is using resources by 
continuously "listening" for incoming records and requests to get records.
To delete the stream and table
                  •	Shut down any producers and consumers that you may still have running.
                  •	Open the Kinesis console at https://console.aws.amazon.com/kinesis.
                  •	Choose the stream that you created for this application (InterIntelStream).
                  •	Choose Delete Stream.
                  •	Open the DynamoDB console at https://console.aws.amazon.com/dynamodb/.
                  •	Delete the StockTradesProcessor table.


## Give examples of different encryption/hashing methods you have come across (one way and two way) and give example 
## scripts in python 3 on how to achieve each one. (20 pts) 
## First I Install bcrypt using pip install bcrypt. We create a virtual environment and install bcrypt with pip. To use this bcrypt, 
## we'll need to import it first. Hashing passwords or any other string is very simple using the bcrypt.hashpw() function which takes  2 arguments.
## That is a string (bytes) and salt. Salt is random data used in the hashing function and this randomness of it is very important. We're not going to 
## cover salt in this article but feel free to read this Wikipedia article for more information. Salts defend against a pre-computed hash attack, e.g. rainbow tables.
## Salts do not have to be memorized by humans they can make the size of the hash table required for a successful attack 
## prohibitively large without placing a burden on the users. Salts are different in each case, they also protect commonly used passwords,
## or those users who use the same password on several sites, by making all salted hash instances for the same password different from each other.
 

This snippet prints:

 
We use the b prefix on the password string to create a byte string, though if you were taking input from a user, you may want to call the .encode("utf-8") method on the string.
Eg
		password = "qwerty12".encode("utf-8")
bcrypt also has a function to check plain text passwords against hashed passwords, returning True if the passwords match, else returning False.  That function is bcrypt.checkpw and it takes 2 arguments: The plain text password (Must be bytes) and a hashed password.
 
As we expect, we got Password match
If you're taking user data for example on a login page for example, you'll need to call .encode("utf-8") on the user input password before we checking it using bcrypt.checkpw()

Using Hashlib
Hashing algorithms are mathematical functions that converts data into a fixed length hash values, hash codes, or hashes. The output hash value is literally a summary of the original value. Now, you may be thinking, then what's the use of using hashing algorithms? Why just use encryption ? Well, though encryption is important for protecting data (data confidentiality), sometimes it is important to be able to prove that no one has modified the data you're sending. Using hashing values, you'll be able to tell if some file isn't modified since creation (data integrity).
 


 					                                            ##  SECTION B: 
## Create a login and a success page in Django. A mockup of the created pages should also be submitted. The mockups should have 
## been created by using advanced design/wireframe tools thus showcasing prowess in usage of the tools and use of production server 
## deployments on uwsgi/nginx. Ensure that the sessions are well and securely managed. (60 pts) 

First I created a virtual environment (venv ). venv (for Python 3) allow you to manage separate package installations for different projects. 
They essentially allow you to create a “virtual” isolated Python installation and install packages into that virtual installation. 
When you switch projects, you can simply create a new virtual environment and not have to worry about breaking the packages installed 
in the other environments. It is always recommended to use a virtual environment while developing Python applications.
<bold>Using this command py -m venv env <bold>

Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment 
will put the virtual environment-specific python and pip executables into your shell’s PATH
source env/Scripts/activate
From the command line, cd into a directory where you’d like to store your code, then run the following command:
			django-admin startproject login
This creates a login directory in your current directory.
Let’s verify your Django project works. Change into the outer login directory, if you haven’t already, and run the following commands.
			python manage.py runserver
Now that our environment – a “login project” – is set up, we’re set to start doing work.
Each application we write in Django consists of a Python package that follows a certain convention. Django comes with a 
utility that automatically generates the basic directory structure of an app, so we can focus on writing code rather than creating directories.
Our apps can live anywhere on our Python path. Here we’ll create our accounts app in the same directory as your manage.py file so 
that it can be imported as its own top-level module, rather than a submodule of login.
To create your app, make sure you’re in the same directory as manage.py and type this command:
		<bold>python manage.py startapp accounts</bold>

To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. 
The AccountsConfig class is in the accounts/apps.py file, so its dotted path is accounts.apps.AccountsConfig . 
Edit the mysite/settings.py file and add that dotted path to the INSTALLED_APPS setting. It’ll look like this:









