# Ecomfulfil Backend

### Description
Ecomfulfil Backend is a Django-based backend application providing REST APIs for managing orders for an e-commerce fulfillment service.

### Features
- User Authentication and Authorization
- API for Managing Orders

### Installation
#### Prerequisites
- Python 3.x
- PostgreSQL or SQLite

#### Setup
1. **Clone the repository**
   ```bash
   git clone git@github.com:Ecomfulfil/ecomfulfil-backend.git
   ```
   ```bash
   cd ecomfulfil-backend
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python3 -m venv venv
   ```
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the root directory based on `.env.example`**
   ```bash
   cp .env.example .env
   ```

5. **Update the `.env` file with your configuration values**

6. **Run migrations and create a superuser**
   ```bash
   python manage.py migrate
   ```
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Usage
- **Admin Panel:** `http://localhost:8000/admin`
- **API Endpoints:** Use tools like Postman or cURL to interact with the API at `http://localhost:8000/api`

### Testing
```bash
python manage.py test
```

### License
Distributed under the MIT License. See `LICENSE` for more information.