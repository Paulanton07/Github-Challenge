# Crowdfunding Platform Concept

## Overview
A self-hosted crowdfunding platform with micro stock exchange functionality where backers become investors with equity stakes and dividend returns.

## Business Model
- User purchases the software
- User hosts it on their own infrastructure
- User promotes and manages their own crowdfunding campaigns

## Core Features

### Platform Components
- Landing page
- Members dashboard
- Project listing and management
- Industry-grade payment integration (third-party processor)

### Investment Model Example
- Project posted: "Build a bench"
- Funding needed: R3000 (materials + labour)
- Backers invest amounts and receive ownership percentages
- Returns/dividends tracked and distributed based on ownership

### Micro Stock Exchange Features
- Investment tracking per project
- Ownership percentage calculation
- Dividend/return distribution system
- Transparent logging and tracking for all transactions
- Member portfolio view (all investments across projects)

## Technical Stack

### Proposed
- **Frontend/Backend**: Django + Python
- **Backend (optional)**: Rust for performance-critical components (financial calculations, payment processing)
- **Payments**: Third-party processor (Stripe Connect, PayPal, Paystack)

### Architecture Considerations
- Start with Django for rapid development
- Optimize with Rust later if performance bottlenecks emerge
- Use payment processor to handle PCI compliance and escrow

## Key Challenges to Address

### Legal/Regulatory
- Equity-based crowdfunding may trigger securities regulations
- Backers owning shares = investment securities in most jurisdictions
- May need compliance features or jurisdiction restrictions
- Tax implications for dividend distribution

### Technical
- Robust financial tracking and audit trails
- Secure payment handling and escrow management
- Accurate percentage/dividend calculations
- Multi-project portfolio management per user

### Financial Infrastructure
- Payment gateway integration
- Money-in and money-out flow management
- Escrow holding for project funding
- Dividend distribution mechanism

## Questions to Research
1. How do existing platforms handle equity crowdfunding legally?
2. What payment infrastructure do they use (banks, payment processors)?
3. What compliance/regulatory frameworks apply?
4. Best practices for dividend calculation and distribution?
5. Simplification opportunities without losing core functionality?

## Development Approach

### Phase 1: Framework & Frontend (Current)
**Build core platform WITHOUT payment/financial integration**
- ✅ Set up Django project structure
- ✅ Create user authentication and authorization
- ✅ Build landing page and member dashboard UI
- ✅ Design project listing/detail pages
- ✅ Create investment tracking UI (mock data)
- ✅ Implement percentage calculation logic (no real money)
- ✅ Build admin panel for project management

**NEW: Customizable Landing Pages**
- Each user gets their own branded landing page/storefront
- Backend page builder for users to customize their page
- Options:
  1. Visual page builder (drag-drop sections, color picker, logo upload)
  2. Template selector with customization options
  3. Code upload option (HTML/CSS) for advanced users
- Custom domain/subdomain support (e.g., username.crowdfund.com)
- Each user's page showcases only THEIR projects
- User can customize: branding, colors, logo, about text, featured projects

**Mock/Placeholder Components:**
- Simulated payment buttons (no actual transactions)
- Fake investment tracking (demonstrates functionality)
- Dividend calculator (shows calculations, doesn't move money)
- API endpoints ready for backend integration later

### Phase 2: Legal Research & Decision (Parallel)
- Research equity crowdfunding regulations by jurisdiction
- Identify compliance requirements
- Choose payment processor and banking partner
- Determine legal structure needed (broker-dealer license, etc.)
- Consult with legal/financial advisors

### Phase 3: Backend Integration (After legal clarity)
- Integrate chosen payment processor API
- Connect bank/escrow accounts
- Implement KYC/compliance checks
- Add real transaction handling
- Set up dividend distribution system
- Security audit and testing

## Next Steps
1. **Initialize Django project with frontend focus**
2. **Build UI/UX and business logic layer**
3. **Research legal frameworks in parallel**
4. **Connect financial backend only after legal compliance confirmed**
