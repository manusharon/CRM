# TravelOS — MVP Product Requirements Document (PRD)

## Summary
MVP objective: Deliver a production-ready travel booking platform core that enables flight booking, payment, agency onboarding, visa lead marketplace with document upload and OCR, in-app chat & call bridging, admin dashboard (live feed), and foundational AI VisaAgent matching/dispatch. Must be secure, multi-language (English + Tamil + Malayalam initially), multi-currency, and able to scale.

## Target users
- Consumers (B2C): Individual travelers (India-first; global expansion later).
- Agencies (B2B): Travel agencies in Kerala & Tamil Nadu initially.
- Admin / Ops: Platform operators (finance, operations, support).

## MVP Modules (Priority)
1. Authentication & Profiles
2. Flight search & booking (single aggregator + caching)
3. Payments (Stripe + Razorpay)
4. Agency Onboarding (apply + KYC upload)
5. Visa Marketplace (request, upload docs, match, ping agencies, accept/decline)
6. In-app Chat & Call bridging (Twilio) for customer ↔ assigned agency communications (all through platform)
7. Document Vault + OCR (Google Doc AI / Tesseract fallback)
8. Admin Live Feed & Dashboard (bookings, visa leads, live chat/calls, profit markers)
9. Basic SUI (VisaAgent prototype — OCR + matching + dispatch)
10. Google Sheets sync worker (bookings & visa leads)

## Non-functional requirements
- Availability: 99.95% for booking/payment endpoints.
- Latency: 95th percentile < 300ms for internal endpoints; flight search may be slower.
- Scale: initial capacity 10k active users; design for horizontal scale.
- Security: PCI-compliant payment flows, encrypted PII, RBAC, audit logs.

---

## Feature details & acceptance criteria

### 1. Authentication & Profiles
- Features:
  - Email/mobile signup, OTP verification, password login, JWT-based auth, TOTP MFA optional.
  - User profile with preferred language & currency.
- Acceptance:
  - Signups must validate email or phone via OTP within 5 minutes.
  - JWT expires in 24 hours; refresh tokens supported.
  - Profile update persists and is reflected immediately in UI.

### 2. Flight Search & Booking
- Features:
  - Search flights (one supplier / aggregator) with caching and fare quote flow.
  - Booking: confirm price, capture passenger details, seat class, Baggage option, booking request.
  - Add fixed platform markup (default ₹500) and show breakdown at checkout.
- Acceptance:
  - Pricing shown at search must be verified before payment; if changed, user alerted and must re-confirm.
  - Bookings created must include supplier booking id and platform markup fields saved.
  - Test: end-to-end sample booking (search -> quote -> book -> payment) completes with records in DB.

### 3. Payment
- Features:
  - Integrate Stripe & Razorpay, support webhooks for success/failure, support wallet top-up.
- Acceptance:
  - Payment success webhook must mark booking as confirmed and trigger booking.created event.
  - Test: simulate successful & failed payment via sandbox.

### 4. Agency Onboarding
- Features:
  - Agency apply flow with document upload (GST, PAN, bank).
  - Admin verification flow to approve/suspend.
- Acceptance:
  - Application stored; admin can approve/reject in UI.
  - Only approved agencies can accept leads.

### 5. Visa Marketplace (core MVP)
- Features:
  - Customer creates visa request, uploads docs.
  - VisaAgent auto-match and ping top-K agencies (configurable K, default 10).
  - Agencies accept within T minutes; accepted -> assigned; chat created.
  - Platform adds fixed markup (default ₹1000).
- Acceptance:
  - Visa request persists with status history.
  - System sends ping to at least K agencies and records acceptance events.
  - Assignment occurs automatically if agency accepts.
  - Chat session created after assignment and accessible to both parties.

### 6. Chat & Call (customer ↔ agency)
- Features:
  - Real-time in-app chat (WebSockets) with attachments.
  - Call bridging via Twilio — platform mediates calls; recording stored.
  - Communication firewall blocks revealing phone/email/URL in messages (simple regex).
- Acceptance:
  - Chat messages delivered in <1s for local tests.
  - Call bridging connects both parties in demo and recording saved to S3.

### 7. Document Vault & OCR
- Features:
  - Presigned S3 uploads; OCR pipeline returns extracted structured fields.
  - Document verification status (accepted/flagged/manual_review).
- Acceptance:
  - OCR must extract passport number, name and expiry for uploaded passport with confidence > 85% in demo data.
  - If OCR confidence < threshold, the lead is flagged for manual review.

### 8. Admin Live Feed & Dashboard
- Features:
  - Live event feed (booking.created, visa.assigned, payment.succeeded) with filters (day/week/month/product).
  - Profit marker shown for each event (e.g., Flight +₹500, Visa +₹1000).
- Acceptance:
  - Events appear in admin UI in real-time as simulation events are generated.

### 9. Google Sheets Sync
- Features:
  - Background worker to append booking & visa lead rows to specified Sheets; manual trigger.
- Acceptance:
  - On manual trigger, designated sheet receives a batch of rows and worker responds with sync status.

---

## MVP Exclusions (phase-2)
- Multi-supplier dynamic flight routing with fallback
- Full BI & ORION analytics
- Loyalty program & referral payouts
- White-label multi-tenant deployments
- Insurance marketplace, EMI finance integrations (phase-3)

## Release Criteria (MVP)
- All critical flows pass UAT: signup, flight booking, payment, visa request->assignment->chat, agency onboarding, admin live feed.
- Security & pen-test remediation for OWASP top 10.
- Backup & recovery validated.
- Production runbook (incident management).
