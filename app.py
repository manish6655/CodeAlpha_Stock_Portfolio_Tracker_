from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf

app = Flask(__name__)

class Stock:
    def __init__(self, symbol, shares):
        self.symbol = symbol
        self.shares = shares
        self.update_price()

    def update_price(self):
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(period="1d")
        self.price = data['Close'].iloc[-1]

    def current_value(self):
        return self.price * self.shares

class Portfolio:
    def __init__(self):
        self.stocks = []

    def add_stock(self, symbol, shares):
        stock = Stock(symbol, shares)
        self.stocks.append(stock)

    def delete_stock(self, symbol):
        for stock in self.stocks:
            if stock.symbol == symbol:
                self.stocks.remove(stock)
                return True  
        return False  

    def portfolio_value(self):
        total_value = sum(stock.current_value() for stock in self.stocks)
        return total_value

portfolio = Portfolio()

@app.route('/', methods=['GET', 'POST'])
def portfolio_view():
    if request.method == 'POST':
        symbol = request.form['symbol']
        shares = int(request.form['shares'])
        portfolio.add_stock(symbol, shares)
    return render_template('index.html', portfolio=portfolio)

@app.route('/delete/<symbol>', methods=['POST'])
def delete_stock(symbol):
    if portfolio.delete_stock(symbol):
        return redirect(url_for('portfolio_view'))
    else:
        return "Stock not found", 404

if __name__ == '__main__':
    app.run(debug=True)
