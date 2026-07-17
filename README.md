<div align="center">

# Digichera

**A multi-vendor e-commerce marketplace built with Django**

Sellers open their own stores, list products, and manage orders — customers browse every store from one catalog and check out in a single flow, with orders automatically split per vendor behind the scenes.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-dev-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-prod-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

</div>

---

## Overview

Digichera is a Django-based multi-vendor marketplace, in the spirit of platforms like Digikala or Basalam. Any visitor can register with just a phone number, then act as a **customer** or open a **store** and sell as a **seller**. Customers can add products from several different stores to a single cart; at checkout, that cart is split into one order per store automatically, and stock is validated inside a database transaction to prevent overselling.

The project is organized as a set of small, decoupled Django apps rather than one monolith, each owning a single concern (users, stores, products, cart, orders, profiles).

## Features

- **Phone-based authentication** — custom user model, no username or email required to sign up or log in
- **Role-aware accounts** — `customer`, `seller`, and `staff` roles on the same user model
- **Seller storefronts** — each seller owns one `Store`, with an auto-generated slug and a compressed, auto-resized logo
- **Nested product categories** — a self-referential category tree with cycle protection (`clean()` blocks a category from becoming its own ancestor) and cascading soft-delete
- **Product catalog** — multiple images per product, with a designated primary image and automatic thumbnailing/compression via Pillow on save
- **Guest & authenticated carts** — anonymous users get a session-based cart that transparently merges into their account cart on login/register
- **Multi-vendor checkout** — one cart, split into a separate `Order` per store, each with its own `OrderItem`s and shipping snapshot
- **Transaction-safe stock handling** — checkout runs inside `transaction.atomic()` and locks product rows with `select_for_update()` on PostgreSQL to prevent race conditions on stock
- **Order lifecycle** — `pending → paid → shipped → delivered`, with sellers restricted to valid status transitions on their own store's orders
- **Search & category filtering** on the product catalog
- **Access-controlled seller actions** — decorators (`store_required`, `store_owner_required`) guard store/product management views
- **Django admin** wired up for all models

## Tech Stack

| Layer         | Technology                                                     |
| ------------- | -------------------------------------------------------------- |
| Backend       | Django 6.0                                                     |
| Database      | SQLite (development) · PostgreSQL (production, via `psycopg2`) |
| Images        | Pillow (server-side resize/compression on upload)              |
| Localization  | django-localflavor (Iranian postal code validation), `fa-ir`   |
| Configuration | python-decouple (environment-based settings)                   |
| Frontend      | Django Templates + Bootstrap                                   |

## Project Structure

```
Digichera/
├── config/          # Project settings (base / dev / prod), root URLconf, WSGI/ASGI
├── core/            # Shared abstract models (TimeStampedModel, SluggedModel) & decorators
├── user/            # Custom phone-based user model, auth views
├── account/         # Customer profile (address, postal code, avatar)
├── store/           # Seller storefronts
├── product/         # Categories, products, product images
├── cart/            # Guest & user shopping cart
├── order/           # Checkout, orders, order items, status transitions
├── page/            # Static-ish pages (home, about, contact, bank)
├── static/          # Frontend assets (CSS/JS)
├── templates/       # Shared templates
└── docs/            # Database diagram
```

## Database Schema

![Database Diagram](docs/diagram.jpg)

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

# Only required when running against PostgreSQL (prod settings)
NEW_DB_NAME=digichera
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

By default the project runs on `config.settings.dev`, which uses SQLite and requires no database setup. Point `DJANGO_SETTINGS_MODULE` at `config.settings.prod` to switch to PostgreSQL with hardened settings for production.

### Run

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the storefront and `http://127.0.0.1:8000/admin/` for the admin panel.

## Roadmap / Ideas

- Payment gateway integration for the checkout → `page:bank` flow
- Seller-side product/order dashboards beyond the Django admin
- REST API layer for a decoupled frontend

## License

No license has been chosen for this project yet. Add a `LICENSE` file to specify how others may use this code.

---

  <br>
  <img src="https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=for-the-badge&logo=github" alt="Status">
  <br>
  <b>😎 New features and improvements are on the way! 
  😅😄😘</b>
</p>

Developed by [Ehsan Barghamadi](https://github.com/EhsanBarghamadi)
