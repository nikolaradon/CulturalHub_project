# CulturalHub

CulturalHub is a web application that allows users to explore and share cultural content, events, and interests. It provides a platform for users to create, edit, and discover various cultural content, fostering a community of cultural enthusiasts.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

CulturalHub aims to connect individuals with diverse cultural interests by providing a centralized platform to share and discover cultural content. Users can explore events, articles, and other cultural items, as well as interact through comments and ratings.

## Features

- **User Authentication:** Users can register, log in, and log out. Authentication is handled securely.

- **User Profiles:** Each user has a profile page where they can showcase their interests and contributions.

- **Content Creation:** Users can create and share cultural content, including events, articles, and more.

- **Category Filtering:** Content is organized into categories, making it easy for users to find what interests them.

- **Comments:** Users can engage in discussions by adding comments to content items.

- **Search Functionality:** Users can search for content and other users based on keywords.

- **Latest and Top Rated Content:** The main page displays the latest added content and the top-rated content.

## Technologies

- **Django:** The web framework used for the backend.

- **HTML/CSS:** Frontend development for the user interface.

- **SQLite:** Database management.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.10
- Django 4.2
- Other dependencies (specified in `requirements.txt`)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/CulturalHub.git
   cd CulturalHub
   ```


2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

  
  - **On Windows:**
     ```
     .\venv\Scripts\activate
     ```

   - **On macOS/Linux:**
     ```
     source venv/bin/activate
     ```

3. **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
   ```

4. **Apply Migrations:**
  ```bash
  python manage.py migrate
   ```


5. **Create a Superuser (Admin):**
  ```bash
  python manage.py createsuperuser
   ```

6. **Run the Development Server:**
  ```bash
  python manage.py runserver
   ```

**Access the Application:**
Open your web browser and go to http://127.0.0.1:8000/

**Access the Admin Panel:**
Visit http://127.0.0.1:8000/admin/ and log in with the superuser credentials.

## Usage
Visit the main page to explore cultural content and categories.
Log in or create an account to contribute by adding new content, commenting, and rating.
Use the search functionality to find specific content or users.

## Contributing
If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.
