CREATE TABLE capital(
	capital_id SERIAL PRIMARY KEY,
	timestamp timestamp,
	capital int
);

CREATE TABLE tickers(
	ticker_id integer SERIAL PRIMARY KEY,
	ticker varchar(5)
);

CREATE TABLE orders(
	order_id integer PRIMARY KEY,
	time_stamp timestamp NOT NULL,
	year integer NOT NULL,
	month integer NOT NULL,
	day integer NOT NULL,
	hour integer NOT NULL,
	minute integer NOT NULL,
	ticker varchar(6) NOT NULL,
	buy_price float NOT NULL,
	sell_price float NOT NULL,
	quantity integer NOT NULL,
	order_type varchar(4) NOT NULL, 
	trader_id integer NOT NULL,
	cost float NOT NULL
	-- foreign key(ticker_id) REFERENCES tickers(ticker_id)
);


CREATE TABLE trades(
	order_id integer,
	is_open boolean,
	foreign key(order_id) REFERENCES orders(orders_id)
);