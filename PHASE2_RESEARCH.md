# Phase 2: Legal Research & Compliance Planning

**Status:** In Progress  
**Started:** February 13, 2026  
**Goal:** Research equity crowdfunding regulations and prepare for Phase 3 payment integration

---

## Overview

Phase 2 focuses on understanding the legal and regulatory landscape for equity-based crowdfunding platforms. This research will inform technical requirements and compliance features needed before implementing real payment processing in Phase 3.

---

## Key Research Areas

### 1. Equity Crowdfunding Regulations

#### International Frameworks
- **United States**: SEC Regulation Crowdfunding (Reg CF) and Regulation A+
- **European Union**: European Crowdfunding Service Providers Regulation (ECSPR)
- **United Kingdom**: FCA rules for investment-based crowdfunding
- **South Africa**: Financial Sector Conduct Authority (FSCA) regulations
- **Australia**: ASIC regulatory framework
- **Canada**: Provincial securities regulations

#### Key Questions
- [ ] What are the registration/licensing requirements for platform operators?
- [ ] What investor protections must be implemented?
- [ ] Are there investment limits per investor?
- [ ] What disclosure requirements exist for projects?
- [ ] Are there reporting obligations to regulators?

---

### 2. Securities Law Considerations

#### Classification Issues
- When does an investment constitute a "security"?
- Equity stakes vs. revenue sharing arrangements
- Token/digital asset considerations
- Exemptions for small offerings

#### Compliance Requirements
- Anti-Money Laundering (AML) requirements
- Know Your Customer (KYC) verification
- Investor accreditation verification
- Ongoing reporting to investors
- Annual financial statements

---

### 3. Payment Processing Infrastructure

#### Payment Processor Selection Criteria

**Option 1: Stripe Connect**
- ✅ Supports marketplace/platform models
- ✅ Built-in escrow functionality
- ✅ Strong fraud protection
- ✅ Excellent documentation and API
- ⚠️ May have restrictions on securities/investments
- 🔍 **Need to verify**: Terms of service for equity crowdfunding

**Option 2: PayPal/Braintree**
- ✅ Global reach
- ✅ Marketplace solutions available
- ✅ Strong buyer protection
- ⚠️ Higher fees for certain transactions
- 🔍 **Need to verify**: Acceptable use policy for investment platforms

**Option 3: Paystack (Africa-focused)**
- ✅ Optimized for African markets
- ✅ Local payment methods
- ✅ Lower fees in target markets
- ⚠️ Limited to specific regions
- 🔍 **Need to verify**: Support for escrow/marketplace models

**Option 4: Specialized Solutions**
- Investment-specific payment processors (e.g., Dwolla, Synapse)
- Banking-as-a-Service (BaaS) providers
- Direct bank integration

#### Payment Flow Requirements
- Investor funds collection
- Escrow holding during campaign
- Disbursement to project creators
- Dividend distribution to investors
- Fee collection for platform
- Refund processing (failed campaigns)

---

### 4. Tax Implications

#### Platform Operator
- Revenue recognition (platform fees)
- Payment processor fee deductibility
- Jurisdictional tax obligations

#### Project Creators
- Revenue recognition timing
- Expense deductibility
- Dividend distribution tax treatment
- 1099/tax reporting requirements (US)

#### Investors
- Capital gains vs. ordinary income
- Dividend taxation
- Loss deductions for failed projects
- Form 1099-DIV or equivalent reporting

---

### 5. Risk Management & Disclosures

#### Required Disclosures
- Investment risk warnings
- No guarantee of returns
- Illiquidity of investments
- Platform fee structure
- Project-specific risks

#### Platform Protections
- Terms of Service requirements
- User agreements and acknowledgments
- Dispute resolution mechanisms
- Limitation of liability clauses
- Insurance considerations

---

## Regulatory Research by Jurisdiction

### 🇺🇸 United States

#### Regulation Crowdfunding (Reg CF)
- **Max raise**: $5 million per 12 months
- **Investment limits**: Based on investor income/net worth
- **Platform requirements**: 
  - Register as funding portal or broker-dealer
  - FINRA membership required
  - Background checks on officers
- **Issuer requirements**:
  - Form C filing with SEC
  - Financial disclosures
  - Annual reports
- **Resources**: 
  - SEC Regulation Crowdfunding: https://www.sec.gov/education/smallbusiness/exemptofferings/regcrowdfunding
  - FINRA Funding Portal Rules

#### Regulation A+ (Mini-IPO)
- **Tier 1**: Up to $20M (state review required)
- **Tier 2**: Up to $75M (federal preemption)
- More extensive disclosure requirements
- Suitable for larger campaigns

#### State Regulations
- State "Blue Sky" laws may apply
- Some states have intrastate crowdfunding exemptions
- Coordination with state regulators needed

---

### 🇿🇦 South Africa

#### FSCA Regulations
- **Licensing**: May require Financial Services Provider (FSP) license
- **Categories**: 
  - Category I: Discretionary FSP
  - Category II: Administrative FSP
- **FICA Compliance**: Financial Intelligence Centre Act
  - KYC/AML requirements
  - Customer Due Diligence (CDD)
  - Record keeping (5 years)
- **Resources**:
  - FSCA website: https://www.fsca.co.za/
  - FICA Act requirements
  - Collective Investment Schemes Control Act

#### Taxation (SARS)
- Dividends Tax: 20% withholding
- Capital Gains Tax: Inclusion rate 40-80%
- Tax reporting obligations

---

### 🇪🇺 European Union

#### ECSPR (Effective November 2021)
- **Platform authorization**: Required across EU
- **Max offering**: €5 million per project per 12 months
- **Investor protection**:
  - Risk warnings
  - Cooling-off period
  - Entry knowledge test for non-sophisticated investors
- **Passport system**: Operate across EU with single authorization
- **Resources**:
  - EU Regulation 2020/1503
  - ESMA guidelines

---

### 🇬🇧 United Kingdom

#### FCA Authorization
- **Regulatory permission**: Required for operating investment-based crowdfunding
- **Client money rules**: Strict segregation requirements
- **Promotions**: Financial promotion restrictions
- **Resources**:
  - FCA Handbook COBS rules
  - PS14/4 Policy Statement

---

### 🇦🇺 Australia

#### ASIC Regulations
- **Licensing**: AFS license required for securities
- **Disclosure**: Product Disclosure Statement (PDS)
- **Crowd-sourced funding (CSF) regime**:
  - Max $5M per 12 months
  - Investor caps: $10,000 per company per 12 months
- **Resources**:
  - Corporations Act 2001
  - ASIC Regulatory Guide 261

---

## Technical Requirements for Compliance

### KYC/AML Implementation

#### Identity Verification
- [ ] Government ID verification (passport, driver's license)
- [ ] Address verification (utility bills, bank statements)
- [ ] Biometric verification (optional, enhanced security)
- [ ] Third-party verification services:
  - Jumio, Onfido, Trulioo, Veriff
  - Stripe Identity
  - Sum&Substance

#### Ongoing Monitoring
- [ ] Transaction monitoring for suspicious activity
- [ ] Politically Exposed Persons (PEP) screening
- [ ] Sanctions list checking (OFAC, UN, EU)
- [ ] Automated alerts for unusual patterns

#### Record Keeping
- [ ] 5-year retention of verification documents
- [ ] Audit trail of all verification attempts
- [ ] Secure encrypted storage

---

### Investor Accreditation

#### Self-Certification
- [ ] Income/net worth questionnaire
- [ ] Acknowledgment of investment limits
- [ ] Risk tolerance assessment

#### Verification (if required)
- [ ] Bank statements
- [ ] Tax returns
- [ ] Brokerage statements
- [ ] Third-party accreditation services

---

### Disclosure & Consent Framework

#### Platform-Level Disclosures
- [ ] Terms of Service
- [ ] Privacy Policy
- [ ] Fee Schedule
- [ ] Risk Warnings
- [ ] Conflict of Interest Statements

#### Project-Level Disclosures
- [ ] Business plan/description
- [ ] Use of funds
- [ ] Risk factors
- [ ] Financial information
- [ ] Management team backgrounds
- [ ] Related party transactions

#### Investor Acknowledgments
- [ ] Risk acknowledgment checkbox
- [ ] Investment suitability confirmation
- [ ] No guarantee of returns
- [ ] Illiquidity acknowledgment
- [ ] Electronic signature

---

### Reporting & Audit Features

#### Investor Reporting
- [ ] Portfolio dashboard
- [ ] Investment confirmations
- [ ] Periodic statements
- [ ] Annual tax forms (1099-DIV, etc.)
- [ ] Dividend payment notifications

#### Regulatory Reporting
- [ ] Transaction reports to regulators
- [ ] Annual Form C amendments (US)
- [ ] Suspicious activity reports (SAR)
- [ ] Large transaction reports

#### Internal Audit
- [ ] Complete transaction logs
- [ ] Dividend calculation audit trail
- [ ] User activity logs
- [ ] Payment reconciliation
- [ ] Compliance monitoring dashboard

---

## Payment Integration Architecture (Technical Planning)

### Escrow Model

```
Investor Payment Flow:
1. Investor initiates investment
2. Funds held in escrow (platform or payment processor)
3. Campaign reaches funding goal
4. Funds released to project creator (minus platform fee)
5. If goal not met: funds returned to investors

Dividend Payment Flow:
1. Project creator reports revenue
2. Platform calculates dividend distribution
3. Platform initiates payout from creator's account
4. Dividends distributed to investor accounts
5. Tax reporting generated
```

### Database Schema Additions Needed

```python
# Payment tracking
class PaymentTransaction:
    - transaction_id (external payment processor ID)
    - user (investor or creator)
    - amount
    - type (investment, dividend, refund, fee)
    - status (pending, completed, failed)
    - payment_method
    - processor_response
    - created_at, updated_at

# KYC verification
class KYCVerification:
    - user
    - verification_status (pending, approved, rejected)
    - verification_method
    - documents (FileField)
    - verified_by (staff member)
    - verified_at
    - expiry_date

# Investor accreditation
class InvestorProfile:
    - user
    - accredited_status
    - income_range
    - net_worth_range
    - risk_tolerance
    - investment_limits
    - verification_documents

# Compliance tracking
class ComplianceLog:
    - event_type
    - user
    - details (JSON)
    - ip_address
    - timestamp
    - flagged_for_review
```

---

## Decision Matrix

### Recommended Approach

#### For MVP/Testing (Phase 3A)
1. **Jurisdiction**: Start with single jurisdiction (e.g., US or South Africa)
2. **Payment Processor**: Stripe Connect (most flexible for testing)
3. **Compliance**: Implement basic KYC, clear disclaimers
4. **Legal**: Obtain legal opinion on required licensing
5. **Limits**: Set conservative investment limits
6. **Disclaimer**: Clearly mark as "demo/testing" until fully compliant

#### For Production Launch (Phase 3B)
1. **Licensing**: Obtain required licenses/registrations
2. **Legal Counsel**: Retain securities attorney
3. **Compliance Officer**: Hire or consult compliance expert
4. **Insurance**: Obtain E&O and cyber insurance
5. **Audit**: Third-party security and compliance audit
6. **Banking**: Establish relationship with compliant bank

---

## Risks & Mitigations

### Legal Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Operating without license | Severe (shutdown, fines) | Obtain legal opinion, file for license |
| Securities violations | Severe (criminal liability) | Follow Reg CF or equivalent |
| Inadequate disclosures | High (investor lawsuits) | Comprehensive disclosure framework |
| Tax reporting failures | High (penalties) | Automated tax form generation |
| AML violations | Severe (fines, criminal) | Robust KYC/AML program |

### Technical Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Payment processor shutdown | Critical | Multiple processor support |
| Data breach | Severe | Encryption, security audit |
| Calculation errors | High | Comprehensive testing, audit trail |
| Downtime during critical period | Medium | High availability architecture |

### Business Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Low adoption | Medium | Marketing, user education |
| Fraud by creators | High | Vetting process, milestone disbursement |
| Investor complaints | Medium | Clear communication, dispute resolution |
| Regulatory changes | Medium | Stay informed, flexible architecture |

---

## Action Items & Next Steps

### Immediate (Research Phase)
- [ ] Consult with securities attorney (estimated cost: $2,000-$5,000)
- [ ] Determine primary target jurisdiction
- [ ] Review payment processor terms of service
- [ ] Research KYC/AML service providers
- [ ] Create compliance checklist
- [ ] Draft preliminary Terms of Service
- [ ] Draft risk disclosure templates

### Before Phase 3 Implementation
- [ ] Finalize licensing strategy
- [ ] Select payment processor
- [ ] Select KYC/AML provider
- [ ] Engage with legal counsel
- [ ] Create compliance documentation
- [ ] Design escrow workflow
- [ ] Plan tax reporting system

### Development Priorities
1. KYC/AML verification module
2. Payment processor integration (sandbox mode)
3. Escrow management system
4. Tax reporting automation
5. Compliance logging and audit trails
6. Enhanced Terms of Service acceptance flow
7. Risk disclosure and investor education

---

## Estimated Costs

### Legal & Compliance
- Securities attorney consultation: $2,000 - $5,000
- License application fees: $1,000 - $10,000 (jurisdiction dependent)
- Annual compliance costs: $5,000 - $20,000
- Insurance (E&O, cyber): $2,000 - $10,000/year

### Technical Services
- KYC/AML provider: $1-5 per verification
- Payment processing fees: 2.9% + $0.30 typical
- Third-party security audit: $5,000 - $15,000
- Cloud infrastructure: $100 - $500/month

### Ongoing Operations
- Compliance officer/consultant: $50-200/hour as needed
- Annual legal review: $2,000 - $5,000
- Regulatory filings: Variable by jurisdiction

---

## Resources & References

### Regulatory Bodies
- **US**: SEC (www.sec.gov), FINRA (www.finra.org)
- **EU**: ESMA (www.esma.europa.eu)
- **UK**: FCA (www.fca.org.uk)
- **South Africa**: FSCA (www.fsca.co.za)
- **Australia**: ASIC (www.asic.gov.au)

### Industry Associations
- Crowdfund Capital Advisors (CCA)
- National Crowdfunding & Fintech Association (NCFA)
- European Crowdfunding Network (ECN)

### Legal Resources
- SEC Small Business Resources
- FINRA Funding Portal Guide
- Crowdfunding Legal Hub
- Local securities law firms

### Technical Resources
- Stripe Connect documentation
- Dwolla API for payments
- Onfido/Jumio for KYC
- Modern Treasury for payment operations

---

## Timeline Estimate

### Phase 2 Completion Target
- **Legal research**: 2-3 weeks
- **Processor evaluation**: 1-2 weeks
- **Compliance framework design**: 2-3 weeks
- **Cost-benefit analysis**: 1 week

**Total Phase 2**: 6-9 weeks

### Phase 3 Timeline (estimated)
- **Phase 3A (Sandbox)**: 8-12 weeks
- **Phase 3B (Production)**: Additional 6-12 weeks
- **Regulatory approval**: 3-6 months (parallel track)

---

## Conclusion

Phase 2 research reveals that equity crowdfunding is a **heavily regulated space** requiring significant legal and compliance investment. The platform has strong technical foundations from Phase 1, but **legal clearance is essential** before processing real money.

### Key Takeaways
1. ✅ **Technical foundation is solid** - Platform ready for payment integration
2. ⚠️ **Legal complexity is high** - Professional legal counsel essential
3. 💰 **Costs are significant** - Budget $10,000-$30,000 for initial compliance
4. 📋 **Licensing required** - Most jurisdictions require registration/license
5. 🔒 **KYC/AML mandatory** - Identity verification critical
6. 📊 **Reporting obligations** - Ongoing tax and regulatory reporting

### Recommended Path Forward
1. **Engage securities attorney** - Get jurisdiction-specific guidance
2. **Choose target market** - Start with one jurisdiction
3. **Implement KYC/AML** - Build compliance infrastructure
4. **Sandbox testing** - Use payment processor test mode extensively
5. **Soft launch** - Limited beta with clear disclaimers
6. **Scale carefully** - Expand only after legal clearance

---

**Status**: Phase 2 research framework complete. Awaiting legal consultation and jurisdiction selection to proceed.
