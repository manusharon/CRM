# Wireframes & UI Spec (Annotated)

This page contains low-fidelity wireframe descriptions for the main screens of the TravelOS MVP. Use these notes to create Figma frames or HTML mockups.

## 1) Customer Home / Dashboard
- Header: logo, language selector (EN/TN/ML), currency selector, user menu
- Top summary cards: Upcoming Trips, Visa Applications, Wallet Balance, Reward Points
- Quick Actions (icon grid): Search Flights, Apply Visa, Book Hotel, Build Package, Contact Support
- Saved Searches widget (captures search & price alerts)
- Recent messages (Chat preview with assigned agencies)

## 2) Visa Request flow screens
- Step 1: Basic details (country, visa_type, travel dates, traveller profile)
- Step 2: Document upload (passport, photo, bank statement) — multi-upload with OCR preview
- Step 3: Payment (if upfront deposit required)
- Completion: Confirmation screen listing agencies pinged and countdown to assignment

## 3) Chat / Call UI (SUI widget)
- Floating SUI chat button bottom-right (open to full chat)
- Chat top-bar: assigned agency name + status + call button
- Message pane: messages with attachments, timestamps
- Side panel: Booking summary / visa status / quick actions (request call, send docs, pay)

## 4) Agency Dashboard (Inbox-first)
- Left: Lead Inbox (new, assigned, accepted, declined) with filters
- Center: Lead detail panel (customer info, documents, score, accept/decline, reply)
- Right: Quick tools: Quotation builder (Generate PDF), Create Booking (book flights/hotels), Performance metric card

## 5) Admin Live Ops (command center)
- Top summary tiles: revenue today, profit today, live users, active chats, pending visas
- Left: Real-time feed (stream of events)
- Center: Live filters & bookings table (actionable)
- Right: KPI graphs & alerts, quick actions (suspend agency, resend lead)

## Designer handoff items
- Create Figma frames for Customer Home, Visa Flow, Chat UI, Agency Inbox, Admin Dashboard
- Provide tokens for colors, spacing and components (buttons, cards, modal)
- Link API hooks for forms (POST /api/v1/visas/requests, POST /api/v1/chat/sessions)
