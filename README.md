# TRNSIT Kolachi 🚌

**TRNSIT Kolachi** is a minimalist, high-contrast transit application designed specifically for the commuters of Karachi. Built with React Native and Expo, it focuses on providing clear, actionable journey information for people on the go.

## 🚀 The Concept
Navigating Karachi's public transport can be overwhelming. **TRNSIT Kolachi** simplifies this into a 3-screen architecture:
1. **The Search ("Where to?"):** Quick access to popular hubs like Tower, Sohrab Goth, and Civic Center.
2. **The Results ("Options"):** A clear comparison between different services (Green Line, Red Bus, local coaches).
3. **The Journey ("Step-by-Step"):** A vertical timeline that answers the three most important questions: *Where am I now? What bus do I wait for? Where do I get off?*

## 🎨 Design Identity: The "Kolachi" Vibe
The app uses a high-contrast, official-yet-modern aesthetic tailored for high visibility in Karachi's sunlight and crowded environments.

- **Asphalt Black (#1A1A1B):** Primary background for text and headers.
- **Transit Yellow (#FFD700):** High-visibility highlight for primary actions.
- **PBS Red (#E63946):** Specific indicator for People's Bus Service (R-1, etc.).
- **Green Line (#2A9D8F):** Specifically for BRT-related routes.
- **Cement Gray (#F4F4F9):** Clean card backgrounds.

## 🛠️ Features
- **Vertical Timeline:** Visualizes the journey steps clearly.
- **Popular Hubs:** One-tap search for major Karachi landmarks.
- **Service Badges:** Color-coded indicators for different bus types.
- **Big Tap Targets:** Designed for ease of use while standing in a moving bus or walking.

## 🏗️ Technical Stack
- **Framework:** React Native / Expo
- **Icons:** Lucide React Native
- **Typography:** Inter (Google Fonts)
- **Navigation:** React Navigation

## 🚦 Getting Started
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npx expo start
   ```

## 📍 Current Scope
This POC focuses on the **Gulshan-e-Iqbal to Tower** flow. The search functionality is currently hardcoded to demonstrate the "Journey Screen" logic, which is the heart of the application.
