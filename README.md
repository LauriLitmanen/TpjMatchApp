# TPJ Match App
Match app built on Flask micro webframework. Create upcoming matches and store match results in a blog type of way. The app was built using this [Flask tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/#tutorial) as a base and extending from that. 
# Motivation
The purpose of this project was to create a way to update a match list on www.tpj.fi without the need to edit the HTML -code of the website everytime. And of course, to learn some Python on the way.
# How it works
Checkout this [repo](https://github.com/LauriLitmanen/TpjKotisivut) of the www.tpj.fi to see the javascript that uses the JSON data this project produces.

On the live version I have disabled Registering so no one else can use my 'Blog'.

<b>After signing in you create a new match result.</b> 
![Alt text](./flaskr/static/images/create.png?raw=true "Optional Title")

<b>It gets saved on the database and will be printed on the frontpage. </b>
![Alt text](./flaskr/static/images/frontpage.png?raw=true "Optional Title")

<b>JSON data gets printed out on api.tpj.fi/api/data/results and ../upcoming</b>
![Alt text](./flaskr/static/images/JSON.png?raw=true "Optional Title")

<b> www.tpj.fi gets the JSON data and constructs HTML list items of the matches and prints it on the website</b>
![Alt text](./flaskr/static/images/tpjfi.png?raw=true "Optional Title")

