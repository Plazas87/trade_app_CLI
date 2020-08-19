select * from openorders;

CREATE TABLE capital(
	capital_id SERIAL PRIMARY KEY,
	timestamp timestamp,
	capital int
);

CREATE TABLE tickers(
	ticker_id integer SERIAL PRIMARY KEY,
	ticker varchar(5)
);

select * from openorders;
truncate table openorders CASCADE;
drop table openorders;
CREATE TABLE openorders(
	order_id bigint,
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
	order_type varchar(5) NOT NULL, 
	trader_id bigint NOT NULL,
	cost float NOT NULL,
	trade_id bigint PRIMARY KEY,
	profit float,
	result varchar(1),
	status boolean,
	foreign key(order_id) REFERENCES orders(order_id)
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
);


select trade_id, status, result, order_id, time_stamp, ticker, buy_price, quantity, order_type, cost from openorders;