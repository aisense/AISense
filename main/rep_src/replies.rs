! version = 2.0

+ hi
- Hello

+ who are you
- I am an artificial intelligence programmed Customer Service to enhance your experience. \n
- I'm your Banking Assistant :)

+ (* stock status *)
- Stock status is:

+ (hello|hi|hey|halo) 
- Hello, How may I help you ?

+ [*] (home|loans|interest rate|interest) [*]
- 8%

+ [*] (weather|rain|temperature|alarm|calender|agenda|meeting|time|date) [*]
- Better ask Siri

+ [*] (education loans|education) [*]
- 10%

+ [*] (war in gulf|gulf war|[*] gulf [*]| [*] tension [*]|war) [*]
- Donot invest in oil companies



+ [*] (infrastructure|infrastructures|bridges|bridge|road|roads|building|buildings|highways|highway) [*]
- I think you should buy shares in steel or real estate company{topic=buyshares}
> topic buyshares

+ [*] (status|prices|price|sell|buy|loss|profit|company) [*]
- Arcelor Mittal shares are doing well, Buy them
- Invest in Real Estate, they ll never let you down{topic=random}

< topic

+ [*] (not doing well|bad|scam|recession|lay offs|strikes|losses|loss) [*]
- Then you shouldn't buy their shares and sell off whatever you have{topic=sellshares}

> topic sellshares

+ [*] (status|prices|price|sell|loss|profit|company|buy) [*]
- TCS shares are doing well, Consider them
- Invest in Oil Company, They are doing well{topic=random}

+ (where to invest|which company to invest)
- Invest in Real Estate, they ll never let you down


< topic

+ [*] (bank balance|balance) [*]
- Rs 10000

+ (what is my ip|ip|ip address)
- Your IP address is: <env REMOTE_ADDR>

+ [*] (mortage loans|mortage) [*]
- 13%

+ what are you
- I am an artificial intelligence programmed Customer Service to enhance your experience.

+ (good|happy|pleasant) (morning|evening|afternoon)
- Yup Its a nice "<star2>"
- Good "<star2>"

+ [*]
- I am an artificial intelligence programmed Customer Service to enhance your experience \n
^ How may I help you ?{weight=20}
- How may I help you ?{weight=10}


+ [*](home|office|cell|customer|customer service|care|phone|mobile) number [*]
- You can reach me at: 1 (800) 555-1234

+ how much (money|balance|cash) i have
- You have Rs 50000

+ how are you
- I'm great, you?

+ [*] invest [*]
- Based on your account history, I think you should invest in Capegemini

+ [*] (shares|share) [*]
- You have shares of Adobe ,  Microsoft , Sprint , Yahoo , Google{topic=share}
> topic share
+ [*] (status|prices|price|sell|loss|profit|company) [*]
- Adobe shares are doing well, Sell of Yahoos
- Yahoos is price is dropping , Beware
- Sprint, Microsoft, Google are normal , Adobe well, sell off Yahoo{topic=random}


+ [*] (buy|invest|spend|put|buy [*] profit|buy [*] company) [*]
- TCS shares are doing well, Consider them
- Invest in Oil Company, They are doing well{topic=random}

< topic 

+ (What is the rate of interest in savings account|what is savings account interest rate|savings interest rate)
-  8%

+ (What is the rate of interest in savings account|what is savings account interest rate|savings interest rate|interest rate)
-  8%

+ [*] (card|credit card| debit card) [*]
- What happened to your card.{topic=card}

> topic card

  // This will match if the word "sorry" exists ANYWHERE in their message
  + [*] (interest|rates)
  - What do you want me to do ?{topic=card}
  
  + [*]
  - What do you want me to do ?{topic=card}
  
  + [*] block [*]
  - I'll block your card. Confirm your PIN{topic=pin}
> topic pin  
  + ####
  - Done Chill!{topic=random}
  
  + [*] no [*]
  - OK{topic=random}
  
  + [*] _ [*]
  - Enter your PIN!{topic=pin}
< topic  
  

  + [*] blocked [*]
  - When did it happen. Call 1 (800) 555-1234 to unblock it.{topic=random}
  
  + [*] (bill|billed|transactions) [*]
  - Your this months bill is Rs. 13000{topic=random}

< topic

