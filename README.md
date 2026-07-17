<div align="center">

# 🛍️ Digichera

A multi-vendor e-commerce marketplace built with Django, where sellers open their own stores and customers shop across all of them from a single cart.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-demo-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## About

Digichera is a Django-based multi-vendor marketplace, similar in spirit to platforms like Basalam or Digikala. Any user can register as a **customer** or a **seller**; sellers open their own storefront and list products, while customers can shop from multiple stores and check out in a single flow — with the system automatically splitting the order per store behind the scenes.

This project was built from the ground up as a hands-on exercise in designing a real-world Django application: custom user models, decoupled apps, soft deletes, race-condition-safe checkout, and more.

## Features

- 🔐 **Custom authentication** — phone-number-based login/registration (no username/email required)
- 👤 **Role-based accounts** — customer, seller, and staff roles
- 🏪 **Seller storefronts** — each seller manages their own `Store` with an auto-generated unique slug
- 🗂️ **Nested categories** — self-referential category tree with cycle protection and cascading soft-delete
- 📦 **Product catalog** — multiple images per product with automatic thumbnail compression
- 🛒 **Smart shopping cart** — works for guests (session-based) and logged-in users, with automatic cart merging on login
- 🏬 **Multi-vendor checkout** — a single cart is automatically split into one `Order` per store
- ⚛️ **Atomic, race-condition-safe checkout** — stock validation with `select_for_update` (PostgreSQL) inside a DB transaction
- 📈 **Order lifecycle** — `pending → paid → shipped → delivered`, with sellers controlling valid status transitions
- 🔍 **Search & category filtering** for the product catalog
- 🛠️ **Fully wired Django admin** — inlines for product images/order items, guarded soft-delete actions

## Tech Stack

| Layer      | Technology                                                          |
| ---------- | ------------------------------------------------------------------- |
| Backend    | Django 6.0                                                          |
| Database   | SQLite (development/demo) · PostgreSQL (recommended for production) |
| Images     | Pillow (automatic compression/resizing)                             |
| Validation | django-localflavor (Iranian postal code validation)                 |
| Config     | python-decouple (environment-based settings)                        |
| Frontend   | Django Templates + Bootstrap                                        |

## Database Schema

![Database Diagram](docs/diagram.jpg)

You can explore the full interactive schema on DrawSQL:
[View Interactive Diagram](https://drawsql.app/teams/ehsan-barghamadi/diagrams/digichera)

## Getting Started

### Prerequisites

- Python 3.x
- pip / venv

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/digichera.git
cd digichera

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

### Environment Variables

Edit `.env` with your own values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_ENV=dev
```

`DJANGO_ENV` switches between `config/settings/dev.py` (SQLite, `DEBUG=True`) and `config/settings/prod.py` (PostgreSQL, hardened settings). It defaults to `dev`, so this demo runs on SQLite out of the box — no PostgreSQL setup required.

### Run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` for the storefront and `http://127.0.0.1:8000/admin/` for the admin panel. A `db.sqlite3` with sample sellers/products is included, or you can add your own through the admin panel.

## Project Structure

```
config/     # Settings (split by environment), root URLs
core/       # Shared abstract base models (TimeStampedModel, SluggedModel) and decorators
user/       # Custom phone-based authentication
account/    # User profile (avatar, address, postal code)
store/      # Seller storefronts
product/    # Categories, products, product images
cart/       # Guest + authenticated shopping cart
order/      # Checkout, orders, order status lifecycle
page/       # Static pages (home, about, contact)
```

## Known Limitations / Roadmap

This is an educational project, built incrementally with a focus on getting the fundamentals right. A few things are intentionally left for future iterations:

- [ ] No real payment gateway integration (checkout uses a simulated "bank" redirect page)
- [ ] `prod.py` settings are scaffolded but not yet hardened for real deployment
- [ ] No automated test suite yet
- [ ] Some image-compression logic is duplicated across models and could be refactored into a shared abstract base class

## License

This project is licensed under the [MIT License](LICENSE).

---

  <br>
  <img src="https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=for-the-badge&logo=github" alt="Status">
  <br>
  <b>😎 New features and improvements are on the way! 
  😅😄😘</b>
</p>

Developed by [Ehsan Barghamadi](https://github.com/EhsanBarghamadi)
