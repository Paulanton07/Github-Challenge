# Crowdfunding Platform 🚀

A self-hosted crowdfunding platform with micro stock exchange functionality where backers become investors with equity stakes and dividend returns.

![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📋 Overview

This platform enables users to host their own crowdfunding campaigns where investors receive equity stakes proportional to their contributions. Unlike traditional crowdfunding, backers become actual stakeholders with ownership percentages and potential dividend returns.

### Key Features

- **User Authentication & Authorization** - Secure account management
- **Customizable Landing Pages** - Each user gets their own branded storefront
- **Project Management** - Create, list, and manage crowdfunding projects
- **Investment Tracking** - Monitor ownership percentages and returns
- **Member Dashboard** - Portfolio view across all investments
- **Admin Panel** - Comprehensive project and user management
- **Micro Stock Exchange** - Equity-based investment model with dividend tracking

> **Note:** This is currently a **Phase 1 development build** with mock data and no live payment processing. Payment integration is planned for Phase 3 after legal compliance research.

## 🏗️ Architecture

### Tech Stack

- **Framework:** Django 5.2.4
- **Language:** Python 3.x
- **Database:** SQLite (development) - PostgreSQL recommended for production
- **Frontend:** Django Templates + Static Assets

### Project Structure

```
crowdfund_platform/
├── accounts/           # User authentication and profiles
├── projects/           # Project creation and management
├── investments/        # Investment tracking and calculations
├── templates/          # HTML templates
├── crowdfund_platform/ # Main Django settings
├── manage.py           # Django management script
└── db.sqlite3          # Development database
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:Paulanton07/Github-Challenge.git
   cd Github-Challenge
   ```

2. **Create and activate virtual environment**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set username, email, and password.

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 💡 Usage

### For Platform Owners

1. Log into the admin panel at `/admin/`
2. Create and manage projects
3. Monitor user investments and equity distributions
4. Customize landing page branding

### For Investors

1. Register for an account
2. Browse available projects
3. Make investments (currently mock/demo mode)
4. Track portfolio and ownership percentages in dashboard
5. View calculated dividends and returns

## 🔧 Development

### Running Tests

```bash
python manage.py test
```

### Creating Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

```bash
python manage.py collectstatic
```

## 📊 Investment Model Example

**Project:** Build a Workshop Bench  
**Funding Needed:** R3,000 (materials + labor)

| Investor | Investment | Ownership % | Returns (if R1,000 profit) |
|----------|-----------|-------------|---------------------------|
| Alice    | R1,500    | 50%         | R500                      |
| Bob      | R900      | 30%         | R300                      |
| Carol    | R600      | 20%         | R200                      |

## 🛣️ Development Roadmap

### ✅ Phase 1: Core Platform (Current)
- User authentication and authorization
- Landing pages and dashboards
- Project listing and management
- Investment tracking UI (mock data)
- Ownership percentage calculations
- Admin panel

### 🔄 Phase 2: Legal Research (In Progress)
- Research equity crowdfunding regulations
- Identify compliance requirements
- Choose payment processor
- Consult legal/financial advisors

### 📅 Phase 3: Payment Integration (Planned)
- Integrate payment processor API (Stripe/PayPal/Paystack)
- Implement KYC/compliance checks
- Real transaction handling
- Dividend distribution system
- Security audit

## ⚠️ Important Notes

### Legal Considerations

This platform involves equity-based crowdfunding which may trigger securities regulations in many jurisdictions. Before deploying with real money:

- Consult with legal counsel
- Understand local securities laws
- Implement required compliance measures
- Consider jurisdiction restrictions
- Address tax implications

### Security

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Implement HTTPS
- Regular security audits

## 🤝 Contributing

This is a competition submission project. Feedback and suggestions are welcome!

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**Paul Schneider**

## 🙏 Acknowledgments

- Built as part of the GitHub Copilot CLI Challenge
- Thanks to the Django community for excellent documentation

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Status:** Development/Concept Phase  
**Demo Video:** [Watch on YouTube](https://youtu.be/N3P2i0bF8Zo)
