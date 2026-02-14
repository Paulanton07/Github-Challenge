# Quick Test Guide - Phase 3A Payment System

## 🧪 Testing the Sandbox Payment Integration

### Prerequisites
- Server running: `python manage.py runserver`
- Active user account (create via `/admin/` or register)
- At least one active project in the database

---

## Test Scenario 1: Make an Investment

### Steps:
1. **Login** to your account
2. **Browse Projects** - Navigate to `/projects/`
3. **Select a Project** - Click on any active project
4. **Scroll to Investment Form**
   - Should see yellow sandbox mode banner
   - Form shows: "Min: R100 | Max: R50,000"
5. **Enter Amount**: `1000`
6. **Click** "Invest Now (Sandbox)"

### Expected Results:
✅ Redirected to success page  
✅ Green success message: "Investment Successful!"  
✅ Shows ownership percentage calculated  
✅ Investment details displayed  
✅ "What Happens Next?" section visible  

### Verify in Database:
1. Go to `/admin/investments/investment/`
2. Find your investment - Status should be **"completed"**
3. Go to `/admin/payments/paymenttransaction/`
4. Find transaction with your username - Status **"succeeded"**
5. Go to `/admin/payments/escrowaccount/`
6. Find project's escrow - `total_held` should have increased

---

## Test Scenario 2: View Payment History

### Steps:
1. Click **"Payments"** in the navigation bar
2. Or navigate to `/payments/history/`

### Expected Results:
✅ Table shows all your transactions  
✅ Transaction types with icons (💰 Investment)  
✅ Status badges (green "Succeeded")  
✅ Transaction IDs starting with `pi_sandbox_`  
✅ Yellow sandbox mode banner at top  

---

## Test Scenario 3: Check Dashboard Charts

### Steps:
1. Navigate to **Dashboard** (`/dashboard/`)
2. Scroll to Visual Analytics section

### Expected Results:
✅ **Portfolio Distribution** chart shows your investment  
✅ **Investment Performance** chart updated  
✅ Charts are interactive (hover for tooltips)  
✅ Investment amount displays in chart  

---

## Test Scenario 4: Release Escrow (Admin Only)

### Steps:
1. Go to `/admin/payments/escrowaccount/`
2. Find an escrow account with status **"active"**
3. Make sure the project has reached funding goal:
   - Go to project in admin
   - Check `current_funding >= funding_goal`
4. Select the escrow account
5. From "Actions" dropdown, choose **"Release selected escrows to creators"**
6. Click **"Go"**

### Expected Results:
✅ Green success message: "Released escrow for [Project Name]"  
✅ Escrow status changed to **"released"**  
✅ `total_released` shows creator amount (95% of total)  
✅ `platform_fee_collected` shows 5% fee  
✅ New transaction created for platform fee  

### Verify Logs:
Check console output for:
```
[SANDBOX] Released R[amount] to [username]
[SANDBOX] Platform fee: R[fee]
```

---

## Test Scenario 5: Multiple Investments in Same Project

### Steps:
1. Create **Investment 1**: R1,500
2. Create **Investment 2**: R500 (same project, same user)

### Expected Results:
✅ Both investments recorded separately  
✅ Escrow `total_held` = R2,000  
✅ Ownership % recalculated based on total  
✅ Dashboard shows both investments  

---

## Test Scenario 6: Investment Limits

### Test Min Limit:
1. Try to invest **R50** (below minimum)
2. **Expected:** Error message "Minimum investment is R100"

### Test Max Limit:
1. Try to invest **R60000** (above maximum)
2. **Expected:** Error message "Maximum investment is R50,000"

---

## Test Scenario 7: Inactive Project

### Steps:
1. Go to `/admin/projects/project/`
2. Change a project's status to **"completed"** or **"cancelled"**
3. Try to invest in that project

### Expected Results:
✅ Error message: "This project is no longer accepting investments."  
✅ Investment not created  

---

## Test Scenario 8: Refund Failed Campaign (Admin)

### Steps:
1. Go to `/admin/projects/project/`
2. Find a project with investments but goal NOT reached
3. Change status to **"cancelled"**
4. Save project
5. Go to `/admin/payments/escrowaccount/`
6. Find the project's escrow
7. Select it, choose **"Refund investors for failed campaigns"**
8. Click **"Go"**

### Expected Results:
✅ Success message: "Refunded investors for [Project Name]"  
✅ All investments status changed to **"refunded"**  
✅ Escrow status changed to **"refunded"**  
✅ Project `current_funding` reset to 0  

### Verify Logs:
```
[SANDBOX] Refunding R[amount] to [username]
```

---

## Test Scenario 9: Creator Connect (Mock)

### Steps:
1. Login as a project creator
2. Navigate to `/payments/connect/`

### Expected Results (Sandbox):
✅ Instantly redirected back  
✅ Success message: "[SANDBOX MODE] Payment account connected successfully!"  
✅ No actual Stripe onboarding (mocked)  
✅ PaymentAccount created in database with mock ID  

### Verify:
1. Go to `/admin/payments/paymentaccount/`
2. Find account for the user
3. Check:
   - `stripe_account_id` starts with `acct_sandbox_`
   - `onboarding_complete` = True
   - `charges_enabled` = True
   - `payouts_enabled` = True

---

## Common Test Data

### Valid Investment Amounts:
- ✅ R100 (minimum)
- ✅ R500
- ✅ R1,000
- ✅ R5,000
- ✅ R50,000 (maximum)

### Invalid Investment Amounts:
- ❌ R0
- ❌ R50 (below min)
- ❌ R99.99 (below min)
- ❌ R50,001 (above max)
- ❌ R100,000 (above max)

---

## Database Checks

### After Each Investment:

**Investment Table:**
```sql
SELECT * FROM investments_investment 
WHERE investor_id = [user_id] 
ORDER BY invested_at DESC;
```

**Payment Transaction Table:**
```sql
SELECT * FROM payments_paymenttransaction 
WHERE user_id = [user_id] 
ORDER BY created_at DESC;
```

**Escrow Account Table:**
```sql
SELECT * FROM payments_escrowaccount 
WHERE project_id = [project_id];
```

---

## Troubleshooting

### Issue: Investment doesn't show in dashboard
- **Check:** Investment status is "completed" (not "pending")
- **Fix:** In sandbox, should auto-complete. Check logs.

### Issue: Charts not updating
- **Check:** Browser cache
- **Fix:** Hard refresh (Ctrl+Shift+R)

### Issue: No payment transaction created
- **Check:** Server logs for errors
- **Verify:** `payments` app is in `INSTALLED_APPS`

### Issue: Escrow not updating
- **Check:** `EscrowAccount` exists for project
- **Fix:** May need to create manually or re-invest

---

## Success Indicators

After all tests, you should have:

✅ Multiple investments in database  
✅ Payment transactions recorded  
✅ Escrow accounts tracking funds  
✅ Dashboard charts showing data  
✅ Payment history page populated  
✅ Admin panel showing all activity  
✅ Console logs confirming sandbox operations  

---

## Next Steps

Once comfortable with sandbox:

1. **Test edge cases** - Concurrent investments, large amounts
2. **Simulate production** - Change `SANDBOX_MODE = False` to see what changes
3. **Add test data** - Create demo projects and investments
4. **Performance test** - Try 100+ investments, check speed
5. **User acceptance testing** - Have others try the flow

---

**Happy Testing!** 🧪

All features should work seamlessly in sandbox mode without any real money movement.
