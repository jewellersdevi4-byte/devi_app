# Devi Jewellers — Owner & Staff Android Mobile App (`devi_app`)

Standalone React Native / Expo native Android application for Devi Jewellers owner and authorized staff.

---

## Features

- **Owner & Staff Authentication**: Secure token-based session handling with biometric/storage encryption via `expo-secure-store`.
- **Filtered Presentation Schemes**: Shows strictly the confirmed presentation schemes (`₹500 Monthly Savings`, `₹3,00,000 Single Payment`, `Gold-Rate Booking`).
- **Payment Collection & Recording**: In-store cash, UPI, and bank transfers, with instant receipt generation and printable PDF sharing via `expo-print` and `expo-sharing`.
- **Payment-Day Gold Tracking**: Displays daily gold rate, allocated grams per transaction (`grams = payment ÷ daily rate`), and total reserved gold balance with immutable historical records.
- **Pay Link Generation**: Quick shareable Razorpay payment links for customer WhatsApp messaging.
- **Enquiry Management**: Full WhatsApp inbox access for shop staff to communicate directly with customers.

---

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Local Properties (Android SDK)
Ensure your Android SDK path is configured in `android/local.properties`:
```properties
sdk.dir=/Users/<your-username>/Library/Android/sdk
```

### 3. Start Metro Bundler
```bash
npm start
```

### 4. Run on Android Device / Emulator
```bash
npm run android
```

---

## Building Standalone Release APK

To compile the release APK directly using Gradle:
```bash
cd android
./gradlew assembleRelease
```
The compiled signed APK will be output to:
`android/app/build/outputs/apk/release/app-release.apk`

---

## Git Setup

To push this standalone repository to your remote Git hosting service (e.g. GitHub):
```bash
git remote add origin https://github.com/<your-org>/devi_app.git
git branch -M main
git push -u origin main
```
