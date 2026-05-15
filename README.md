# Mobile-Based Library Management System

> **Project:** Students' Assessment of the Academic Library Services at
> Isabela State University – Echague Campus: Basis for a Proposed
> Mobile-Based Library Management System Framework

This is a **prototype** Android app written in **Java** for the digital
library of ISU Echague. It has **no backend** — every book, notification
and user is hardcoded in the source code so the project can be opened and
run by a student without any server, internet or database setup.

---

## 1. Demo Login

```
Email:    student@isu.edu.ph
Password: student123
```

You can also tap **Register** on the login screen to create your own demo
account (it is just saved on the phone via SharedPreferences).

---

## 2. How to run

1. Open the project folder in **Android Studio** (Hedgehog or newer).
2. Let Gradle finish syncing.
3. Plug in an Android phone (USB debugging on) **or** start an emulator
   running Android 7.0 (API 24) or newer.
4. Click the green ▶ **Run** button.

That's it. There is nothing to configure, no `.env` file, no API keys.

---

## 3. What the app does

| Screen           | What it shows                                          |
|------------------|--------------------------------------------------------|
| Splash           | Logo + tagline, then jumps to Login or Home.           |
| Login            | Validates the hardcoded demo credentials.              |
| Register         | "Creates" a new account locally on the phone.          |
| Forgot Password  | Pretends to send a reset link.                         |
| Home / Dashboard | Search bar, quick-access tiles, Featured + Recommended.|
| Search & Browse  | Full-text search + category chip filters.              |
| Book Details     | Cover, bibliographic info, Borrow / Read / Download.   |
| My Library       | Borrowed books (with due dates) + Downloaded items.    |
| Notifications    | Due-date reminders, new arrivals, announcements.       |
| Profile          | Student info + menu (QR, Feedback, Settings, Logout).  |
| QR Catalog       | A real QR code generated from a hardcoded URL.         |
| Feedback Survey  | 5 star ratings + comments saved to SharedPreferences.  |

---

## 4. Project structure

```
app/src/main/
├── AndroidManifest.xml
├── java/com/example/mobile_basedlibrarymanagementsystem/
│   ├── SplashActivity.java          ← first screen on app launch
│   ├── LoginActivity.java
│   ├── RegisterActivity.java
│   ├── ForgotPasswordActivity.java
│   ├── MainActivity.java            ← shell with bottom navigation
│   ├── BookDetailsActivity.java
│   ├── NotificationsActivity.java
│   ├── QrCatalogActivity.java
│   ├── FeedbackSurveyActivity.java
│   ├── fragment/
│   │   ├── HomeFragment.java
│   │   ├── SearchFragment.java
│   │   ├── MyLibraryFragment.java
│   │   └── ProfileFragment.java
│   ├── adapter/
│   │   ├── BookAdapter.java
│   │   ├── BookHorizontalAdapter.java
│   │   ├── BorrowedBookAdapter.java
│   │   └── NotificationAdapter.java
│   ├── model/
│   │   ├── Book.java
│   │   ├── BorrowedBook.java
│   │   └── NotificationItem.java
│   └── data/
│       ├── BookRepository.java       ← the hardcoded catalog
│       ├── BorrowManager.java        ← in-memory borrow / download list
│       ├── NotificationRepository.java
│       └── UserSession.java          ← demo creds + SharedPreferences
└── res/
    ├── drawable/   ← icons (vectors) + button / card backgrounds
    ├── layout/     ← all XML screens
    ├── menu/       ← bottom nav menu
    ├── values/     ← colors.xml, strings.xml, themes.xml
    └── values-night/
```

### Where to make common changes

| I want to…                           | Edit this file                          |
|--------------------------------------|------------------------------------------|
| Add a new book                       | `data/BookRepository.java`               |
| Change demo credentials              | `data/UserSession.java`                  |
| Edit the brand colors                | `res/values/colors.xml`                  |
| Add a new notification               | `data/NotificationRepository.java`       |
| Change the QR code link              | `QrCatalogActivity.java` (`CATALOG_URL`) |

---

## 5. Color palette

From the design specs:

| Role      | Hex       | XML name              |
|-----------|-----------|-----------------------|
| Primary   | `#1E3A8A` | `@color/primary_blue` |
| Secondary | `#F3F4F6` | `@color/secondary_gray`|
| Accent    | `#F59E0B` | `@color/accent_orange`|

---

## 6. Scope statement coverage

| Scope item                                              | Implemented in                       |
|---------------------------------------------------------|--------------------------------------|
| Mobile-friendly digital library interface               | All screens                          |
| Online catalog with sample bibliographic records        | `BookRepository.java`                |
| Basic search and browse functionality                   | `SearchFragment.java`                |
| Resource request / reservation feature                  | `BookDetailsActivity` Borrow button  |
| QR code access to the digital catalog                   | `QrCatalogActivity.java`             |
| User feedback and evaluation survey                     | `FeedbackSurveyActivity.java`        |
| Documentation for basic system use and maintenance      | This `README.md`                     |

---

## 7. Limitations (on purpose)

This is a **classroom prototype**:

- No real backend, no real database, no internet calls.
- Closing the app resets the borrowed-books list (it is in memory only).
- The "Read Online" and "Download" buttons just show a toast — they do not
  open a real PDF.
- Authentication is just a string match against the demo credentials.

These trade-offs keep the source code small enough that students can read
through every file in one sitting and understand what each line does.

---

## 8. Maintenance tips

- **Add a new screen:** create the layout in `res/layout/`, the
  `Activity` (or `Fragment`) in `java/...`, then register the activity in
  `AndroidManifest.xml`.
- **Change the launcher screen:** move the `<intent-filter>` in
  `AndroidManifest.xml` to a different activity.
- **Reset the demo data:** uninstall and reinstall the app — that wipes
  `SharedPreferences` (where the user's session and feedback are stored).
