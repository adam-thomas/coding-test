# Read this first!

Welcome to this coding test! For this, you'll need some familiarity with Django, ideally some experience with
using web APIs, and your ingenuity. 

In this test, you need to fill in a function to parse some online store orders, retrieved from an external API,
into your system's internal Django database. Your function needs to accept a dictionary of `api_data`, and create
some number of Django model instances. The database already contains customers and products; it's your job
to store new orders as they come in. 

You haven't used this particular order API before; you have the documentation to get you started, a set of
internal Django models to fill in, and some guidance from your coworkers in other departments. These coworkers
are also going to be testing and using your work. Your solution needs to work for them. They are
experts in their own fields, but they're not familiar with your code, so their descriptions of the issues may not
lead you directly to the problem.

I've written a set of SUPER SECRET unit tests that represent manual testing or usage that you or your coworkers
might perform. The error messages from failed tests are written similarly to feedback messages you might get
from said coworkers - it's on you to figure out the guts of the problem and adapt your solution appropriately!

#### To take this test, you need to:

1. Set up this project
2. Don't look in the `dont_look_in_here` folder
3. Familiarise yourself with the Django models in `models.py`
4. Implement the `parse_orders` function, so that it creates the appropriate `Order` and `LineItem` objects to
represent the `api_data` input
5. Run the tests and see what does and doesn't work
6. Repeat steps 4 and 5 until you feel you want to wrap up

The test isn't designed to eat up a bunch of your time - I'm targeting around an hour, maybe two. Don't feel pressured to
put loads of effort in, or persevere through getting stuck. If anything is unreasonably unclear, the setup instructions
don't work, or you need a hint, feel free to send me an email. If you feel you've spent enough time and haven't made
all the tests pass, that's fine. Jot down what you've done, and your overall approach, and we can talk through it
in the interview :)

The rest of this README gives you instructions on setting up the project and running the tests, and then the
documentation and information you're given to start this hypothetical project.

## Setup

This project is designed for a Unix system with Python 3 installed. Run the following in your terminal:

* Clone the project and `cd` into the cloned directory.
* Create a virtual environment with `python3 -m venv .`.
* Activate the virtual environment with `source bin/activate`.
* Ensure Postgres is running on your system ([instructions are here](https://www.postgresql.org/) if you need to set it up).
* Create the database and install dependencies with `make install`.

## Running the tests

* Run `make test` in the terminal and observe the outcome!

## The code

Most of the code isn't particularly relevant. There are two files you need to look at:

* `orders/models.py` - these are the Django models you're going to be creating. In particular, your code needs to
produce `Order` and `LineItem` objects.
* `orders/parse_orders.py` - this file contains the `parse_orders(api_data)` function you need to fill in. This
function accepts a dictionary returned by an API call (documented below), and creates Django models to store the
data in the database.

There is also a SUPER SECRET folder that you need to not look at! `dont_look_in_here/` contains the unit tests,
and reading them would spoil the fun. Try to resist the temptation at least until you've done the test itself.
Pretty please. :)

## API data documentation and other information you have

The API returns information in the following format:

```json
{
    "orders": [
        {
            "number": "001234",
            "customer_email": "leeroy.jenkins@example.com",
            "line_items": [
                {
                    "sku": "PRODUCT-CODE",
                    "quantity": 1,
                    "discount_price": 0.99
                }
            ]
        }
    ]
}
```

The data fields on an order are:

* `number` (Required) - A unique number identifying this order on the online store.
* `customer_email` (Required) - The email address of the customer who purchased this order.
* `line_items` (Required) - A list of all of the items purchased as part of this order.

The data fields on a line item are:

* `sku` (Required) - Stock-Keeping Unit. A unique product code identifying the purchased product.
* `quantity` (Required) - The amount of this product purchased.
* `discount_price` (Optional) - If the product was sold at a different price from the default, this field will
hold the modified value.

In addition to the above, during planning discussions for this feature, your coworkers have told you:

* We have to import all orders on the store - we can't miss any.
* The fields all have to be accurate to the order as it is online.
* We need to connect new orders to existing customer and product records.
* We want to support customers amending their orders, because people sometimes get it wrong the first time.
* Guest customers (customers who haven't pre-registered) should be handled as well.

From your initial research, you also know the database contains the following existing records:

* One customer, `Leeroy Jenkins (leeroy.jenkins@example.com)`.
* Two products - `SMALL-HAT` costing £10, and `REALLY-BIG-HAT` costing £250. (It's a _really_ big hat.)
