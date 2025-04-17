# Coishop - Coin Purchase App

A simple Django application for purchasing and managing virtual coins using the Cashfree payment gateway. Users can purchase coins with different price packs, and their balance is updated only after a successful payment.

## Features
- View current coin balance.
- Buy coins in predefined price packs (₹200, ₹500, ₹1000, ₹1500, ₹3000).
- Secure payment handling via Cashfree.
- Coin count updates only after successful payment.
- Clean and simple user interface.

## Prerequisites

Before you start, make sure you have the following installed on your local machine:

- Python 3.8+
- Django 4.2
- pip (Python package installer)
- Cashfree API credentials (You can get these from [Cashfree](https://www.cashfree.com))

## Installation

### 1. Clone the repository
Clone the repository to your local machine using:

```bash
git clone https://github.com/yourusername/coishop.git
cd coishop
```

### 2. Create a virtual environment
Create a virtual environment to manage your project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install dependencies
Install the necessary Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root of your project and add your Cashfree API credentials:

```ini
CASHFREE_APP_ID=your_cashfree_app_id
CASHFREE_SECRET_KEY=your_cashfree_secret_key
CASHFREE_BASE_URL=https://sandbox.cashfree.com/api/v2
```

### 5. Apply database migrations
Run the migrations to set up the database:

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)
If you need access to the Django admin interface, you can create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to create your superuser account.

### 7. Run the development server
Start the development server:

```bash
python manage.py runserver
```

Now you can access the app by visiting [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Usage

1. **Index Page**: View your current coin balance.
2. **Buy Coins Page**: Choose a coin pack to purchase (₹200, ₹500, ₹1000, ₹1500, ₹3000).
3. **Payment Verification**: After making a payment, your coin balance will be updated on the success page if the payment is successful. If the payment fails, your coin balance will not change.

## File Structure

- `coin_app/` - Contains the core logic of the app (models, views, templates).
  - `models.py` - Defines the database models (Transaction, Wallet).
  - `views.py` - Handles the business logic for buying coins and verifying payment.
  - `templates/` - Contains the HTML templates for rendering pages.
- `db.sqlite3` - The SQLite database for development (you can use another DB if preferred).
- `.env` - Holds your Cashfree API credentials.
- `requirements.txt` - Lists all the Python dependencies for the project.

## Testing

To run the tests, use:

```bash
python manage.py test
```

## Deployment

For deployment, you can use platforms like [Render](https://render.com), [Heroku](https://www.heroku.com), or any other service that supports Django apps. Make sure to set the necessary environment variables for production.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Cashfree](https://www.cashfree.com) for the payment gateway API.
- [Django](https://www.djangoproject.com) for the powerful web framework.
- Contributors and open-source developers who make web development easier.

Feel free to fork, modify, and improve this project as needed!
