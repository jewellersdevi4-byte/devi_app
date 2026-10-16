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

### Customer payment sound alerts

Payment alerts use Expo Push Notifications, so the backend worker can notify the
Android device while the app is in the background or closed. Each alert includes
the customer name, amount, and payment date, and uses the Android notification
channel's default sound.

Before building a release, create an Expo EAS project and set `EAS_PROJECT_ID` to
its project ID. Configure Firebase Cloud Messaging v1 credentials for that EAS
project, and set `GOOGLE_SERVICES_JSON` to the Firebase Android configuration
file. Keep that file out of source control. Sign in, enable **Payment sound
alerts**, and allow notifications on the device. The backend migration must be
applied and its worker must be running for payment alerts to be delivered.


### Background payment alert release check

The API now runs a separate payment push loop when `RUN_EMBEDDED_WORKER` is not
`false`. If disabled, run `npm run worker` as a continuously running service.
Apply backend migrations (including 012) before deployment. WhatsApp delivery
must not block payment push processing.

This checkout is missing the Expo project ID and Firebase Android config. Before
building, set `EAS_PROJECT_ID` and `GOOGLE_SERVICES_JSON` in the build environment,
configure FCM v1 credentials for that Expo project, and regenerate Android native
configuration with `npx expo prebuild --platform android --no-install`. Review the
native diff and build/install a new signed APK. Existing APKs do not acquire
Firebase configuration from a backend deployment.

Sign in and confirm device registration. Test a confirmed payment while the admin
app is backgrounded and the phone is locked, then with the app swiped away. Check
push tickets/receipts and actual phone delivery. Android force-stop blocks delivery
until the app is reopened. The local notification test verifies sound/pop-up only;
it does not verify the server, FCM, or background delivery. Do not mark this release
verified until a real phone receives the payment without reopening the app.
