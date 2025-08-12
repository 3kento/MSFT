import yfinance as yf
import requests

#botname = MSFT

#microsoft stock
msft = yf.Ticker("MSFT")

#data collection, set values = msft.history(period="3mo", interval="1mo")["High"]
data = msft.history(period="3mo", interval="1mo")
highList = data["High"].tolist()
Ha = highList[2]
Hb = highList[1]
Hc = highList[0]
highDates = data.index.tolist()
highday = msft.history(period="1d", interval="1d")["High"]

dateA = highDates[2]
dateB = highDates[1]

currentPrice = msft.fast_info.last_price

#first formula X = Ha - (Ha - L{B, A}) * 0.75data
Lab = msft.history(start = dateB, end = dateA, interval="1mo")["Low"]
X = (Ha - (Ha - Lab) * 0.75).iloc[0]

#second formula X = Ha - 1.7 * (Ha - (Ha + Hb + Hc)/3)
Y = Ha - (2 * (Ha - ((Ha + Hb + Hc)/3)))

#0.766 percent rule
Z = (currentPrice - (highday * 0.00766)).iloc[0]

def main():
    global currentPrice
    global X
    global Y
    global Z

    if currentPrice <= X:
        changeMessage(0)

    elif currentPrice <= Y:
        changeMessage(1)
    elif currentPrice <= Z:
        changeMessage(2)
    else:
        None

message = ""

def changeMessage(n = 3): 
    global X
    global message
    global currentPrice
    global highday

    if n == 0:
        message = "Using the first formula, the current price has reached beneath X = " + str(X) + ", at: " + str(currentPrice)
    elif n == 1:
        message = "Using the second formula, the current price has reached beneath Y = " + str(Y) + ", at: " + str(currentPrice)
    elif n == 2:
        message = "Using the third formula, the current price has reached beneath X = " + str(Z) + ", at: " + str(currentPrice) + ", the highest point today was " + highday
    else:
        return None
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Message sent!")
    else:
        print("Failed to send message:", response.text)

main()
