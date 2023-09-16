# SocialNetwork

---

### 📋 Features

- **User Management**: User Signup, User Login
- **Posts Management**: Post Creation, Post Like/Unlike, Post Analytics
- **User Activity Tracking**: Last Activity, Last Login
- **Automated Bot**: For Creation User Posts And Likes

---

### 🛠 Technical Stack

- **Programming Language**: Python
- **Web Framework**: Django
- **Databases**: PostgreSQL, Redis
- **Async**: Async scripts(Bot)

---

### 🛠 Setup & Installation
### For windows

1. **Clone the Repository:**
    ```
    git clone https://github.com/davidkrivko/SocialNetwork.git
    cd SocialNetwork
    ```
   
2. **Set Up Environment Variables**:
    ```
   cp .env.example .env
    ```
3. **Launch Docker Services**:
    ```
    docker-compose up -d
    ```
4. **Virtual environment activation:**
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
5. **Install Python Dependencies:**
    ```
    pip install -r requirements.txt
    ```
6. **Run migrations**
    ```
    python manage.py migrate
    ```
7. **Create data with bot(Optional)**


8. **Run the Server:**
    ```
    python manage.py runserver
    ```
---