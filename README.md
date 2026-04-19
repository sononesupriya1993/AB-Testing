# A/B Testing for Data Scientists: A Practical Decision-Making Guide

This repository contains a comprehensive guide and a Python-based calculation engine designed to bridge the gap between theoretical statistics and real-world product experimentation.

## 🌟 Overview
Most A/B testing resources are either overly academic or too shallow. This project was born from my journey of mastering experimentation from the ground up while transitioning into the Oslo tech market. It focuses on the **"Why"** and **"When"** of testing, rather than just the "How."

## 📁 Repository Contents
* **`AB_Testing_Guide_Supriya_Sonone.pdf`**: A step-by-step strategic guide covering the full experimentation lifecycle—from hypothesis formulation to business decision-making.
* **`ab_testing_calculations.py`**: A documented Python script to automate:
  * Power Analysis (Sample Size & Duration)
  * Two-Proportion Z-Tests
  * Confidence Interval Calculation
  * Revenue Impact Translation

## 🚀 Key Frameworks Covered
Based on industry standards and interview patterns, this guide deep-dives into:
- **The "When Not to Test" Framework:** Identifying cases where traffic is too low or changes are irreversible.
- **Metric Instrumentation:** The anatomy of reliable logging (`user_id`, `variant`, `timestamp`).
- **Guardrail Metrics:** Protecting user experience (e.g., page load time) while optimizing for conversions.
- **The Pitfalls:** Practical explanations of **p-hacking**, **Simpson’s Paradox**, and the **Novelty Effect**.

## 📊 Sample Calculation Logic
The included Python tool allows you to input your baseline conversion rates and traffic volume to immediately see your experiment's constraints:
> *Example: With a 12% baseline and 2% MDE, the tool calculates exactly why you need ~4,435 users per group to achieve 80% power.*

## 👩‍💻 About the Author
I am a **Data Scientist based in Oslo, Norway**, passionate about building data products that drive genuine business value. I specialize in translating complex statistical signals into actionable product insights.

---
**Connect with me:**
* **LinkedIn:** https://www.linkedin.com/in/supriya-sonone-355a89252/
* **Email:** supriyasonone111@gmail.com
