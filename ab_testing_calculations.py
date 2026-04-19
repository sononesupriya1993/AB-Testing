"""
A/B Testing Calculations — The Math Behind the Numbers
=======================================================
Author: Supriya Sonone | Data Scientist | Oslo, Norway
GitHub: github.com/supriyasonone

This file contains all the calculations referenced in the A/B Testing guide.
Every number in the document can be traced back to a function here.

I built this while learning A/B testing deeply — the goal is to make
the math transparent so anyone can plug in their own numbers and understand
exactly how each result is derived.

Sections:
  1. Sample Size Calculation
  2. Test Duration Calculation
  3. Revenue Impact Calculation
  4. Z-Test for Proportions (the actual statistical test)
  5. Confidence Interval Calculation
  6. Full Example — Checkout Button Test (end to end)
"""

import math
from scipy import stats
import numpy as np


# SECTION 1: SAMPLE SIZE CALCULATION


def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.80):
   
    treatment_rate = baseline_rate + mde

    # z-score for significance level (two-tailed, so alpha/2)
    z_alpha = stats.norm.ppf(1 - alpha / 2)

    # z-score for power
    z_beta = stats.norm.ppf(power)

    # Variance of each group: p * (1 - p)
    var_control   = baseline_rate * (1 - baseline_rate)
    var_treatment = treatment_rate * (1 - treatment_rate)

    # Core formula
    numerator   = (z_alpha + z_beta) ** 2 * (var_control + var_treatment)
    denominator = (treatment_rate - baseline_rate) ** 2

    n = numerator / denominator
    return math.ceil(n)


# SECTION 2: TEST DURATION CALCULATION


def calculate_test_duration(sample_size_per_group, daily_users, traffic_split=0.50):
    
    users_per_group_per_day = daily_users * traffic_split * 0.50
    
    total_days = math.ceil(sample_size_per_group / users_per_group_per_day)

    return {
        "sample_size_per_group": sample_size_per_group,
        "daily_users": daily_users,
        "users_per_group_per_day": users_per_group_per_day,
        "total_days": total_days,
        "explanation": (
            f"You need {sample_size_per_group:,} users per group. "
            f"With {daily_users:,} daily users and {int(traffic_split*100)}% in the experiment, "
            f"each group gets {users_per_group_per_day:.0f} users/day. "
            f"Total duration: {total_days} days."
        )
    }


# SECTION 3: REVENUE IMPACT CALCULATION


def calculate_revenue_impact(monthly_users, baseline_rate, lift_absolute,
                              avg_order_value):
   
    new_rate = baseline_rate + lift_absolute

    baseline_conversions = monthly_users * baseline_rate
    new_conversions      = monthly_users * new_rate
    extra_conversions    = new_conversions - baseline_conversions

    baseline_revenue     = baseline_conversions * avg_order_value
    new_revenue          = new_conversions * avg_order_value
    incremental_revenue  = extra_conversions * avg_order_value

    return {
        "monthly_users":        monthly_users,
        "baseline_rate":        f"{baseline_rate*100:.1f}%",
        "new_rate":             f"{new_rate*100:.2f}%",
        "extra_conversions":    round(extra_conversions),
        "baseline_revenue":     round(baseline_revenue),
        "new_revenue":          round(new_revenue),
        "incremental_revenue":  round(incremental_revenue),
        "explanation": (
            f"A {lift_absolute*100:.2f}% absolute lift means "
            f"{round(extra_conversions):,} more conversions per month. "
            f"At {avg_order_value:,.0f} per order, that is "
            f"{round(incremental_revenue):,.0f} in additional monthly revenue."
        )
    }


# SECTION 4: Z-TEST FOR PROPORTIONS


def run_proportion_ztest(conversions_a, users_a, conversions_b, users_b,
                          alpha=0.05):
   
    p_a = conversions_a / users_a
    p_b = conversions_b / users_b

    # Pooled proportion (under null hypothesis that groups are equal)
    p_pool = (conversions_a + conversions_b) / (users_a + users_b)

    # Standard error
    se = math.sqrt(p_pool * (1 - p_pool) * (1/users_a + 1/users_b))

    # Z-statistic
    z = (p_b - p_a) / se

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    significant = p_value < alpha

    return {
        "rate_control":   f"{p_a*100:.2f}%",
        "rate_treatment": f"{p_b*100:.2f}%",
        "absolute_lift":  f"{(p_b - p_a)*100:.2f}%",
        "relative_lift":  f"{((p_b - p_a)/p_a)*100:.1f}%",
        "z_statistic":    round(z, 4),
        "p_value":        round(p_value, 4),
        "significant":    significant,
        "verdict": (
            f"REJECT null hypothesis — the green button performs significantly better."
            if significant else
            f"FAIL TO REJECT null hypothesis — no significant difference detected."
        )
    }


# SECTION 5: CONFIDENCE INTERVAL


def calculate_confidence_interval(conversions_a, users_a, conversions_b,
                                   users_b, alpha=0.05):
    
    p_a = conversions_a / users_a
    p_b = conversions_b / users_b

    diff = p_b - p_a

    # Unpooled SE for the confidence interval
    se = math.sqrt((p_a*(1-p_a)/users_a) + (p_b*(1-p_b)/users_b))

    z = stats.norm.ppf(1 - alpha/2)
    lower = diff - z * se
    upper = diff + z * se

    includes_zero = lower <= 0 <= upper

    return {
        "point_estimate":  f"{diff*100:.2f}%",
        "ci_lower":        f"{lower*100:.2f}%",
        "ci_upper":        f"{upper*100:.2f}%",
        "ci_summary":      f"95% CI: [{lower*100:.2f}%, {upper*100:.2f}%]",
        "includes_zero":   includes_zero,
        "interpretation": (
            "CI includes zero — result is not conclusive."
            if includes_zero else
            "CI excludes zero — the effect is real with 95% confidence."
        )
    }


# SECTION 6: FULL WORKED EXAMPLE (Checkout Button Test)

def run_full_example():
    print("=" * 60)
    print("Grey button (control) vs Green button (treatment)")
    print("=" * 60)

    # ── Inputs ──────────────────────────────────────────────
    BASELINE_RATE    = 0.12    # 12% current conversion rate
    MDE              = 0.02    # want to detect at least +2% lift
    ALPHA            = 0.05    # 5% false positive tolerance
    POWER            = 0.80    # 80% chance of catching a real effect
    DAILY_USERS      = 500     # users on the checkout page per day
    MONTHLY_USERS    = 10_000  # for revenue calculation
    AVG_ORDER_VALUE  = 800     # NOK 800 average order

    print("\n--- STEP 1: How many users do we need? ---")
    n = calculate_sample_size(BASELINE_RATE, MDE, ALPHA, POWER)
    print(f"  Baseline rate:   {BASELINE_RATE*100}%")
    print(f"  Target rate:     {(BASELINE_RATE + MDE)*100}%")
    print(f"  MDE:             {MDE*100}%")
    print(f"  Sample needed:   {n:,} users per group  ({n*2:,} total)")

    print("\n--- STEP 2: How long will the test take? ---")
    duration = calculate_test_duration(n, DAILY_USERS, traffic_split=0.50)
    print(f"  {duration['explanation']}")
    print(f"  NOTE: This is where the '36 days' in the document came from.")
    print(f"  Formula: {n*2:,} total users / {DAILY_USERS} users per day = {duration['total_days']} days")

    print("\n--- STEP 3: Run the test, collect results ---")
    # Simulated results after running the experiment
    CONV_A   = 523   # conversions in control
    USERS_A  = 4500  # users in control
    CONV_B   = 612   # conversions in treatment
    USERS_B  = 4500  # users in treatment
    print(f"  Control:   {CONV_A} conversions out of {USERS_A} users")
    print(f"  Treatment: {CONV_B} conversions out of {USERS_B} users")

    print("\n--- STEP 4: Run the statistical test ---")
    result = run_proportion_ztest(CONV_A, USERS_A, CONV_B, USERS_B, ALPHA)
    for k, v in result.items():
        print(f"  {k:<20}: {v}")

    print("\n--- STEP 5: Calculate confidence interval ---")
    ci = calculate_confidence_interval(CONV_A, USERS_A, CONV_B, USERS_B, ALPHA)
    for k, v in ci.items():
        print(f"  {k:<20}: {v}")

    print("\n--- STEP 6: Translate to business impact ---")
    actual_lift = (CONV_B/USERS_B) - (CONV_A/USERS_A)
    revenue = calculate_revenue_impact(MONTHLY_USERS, BASELINE_RATE,
                                       actual_lift, AVG_ORDER_VALUE)
    print(f"  {revenue['explanation']}")
    print(f"  Incremental monthly revenue: NOK {revenue['incremental_revenue']:,}")
    print(f"\n  NOTE: The 'NOK 158,000' figure in the document used:")
    print(f"    100,000 monthly users x 1.98% lift x NOK 800 avg order")
    print(f"    = 1,980 extra conversions x 800 = NOK 1,584,000")
    
    print(f"    With 10,000 monthly users the correct figure is:")
    print(f"    NOK {revenue['incremental_revenue']:,}/month")

    print("\n" + "=" * 60)
    print("FINAL DECISION FRAMEWORK")
    print("=" * 60)
    print(f"  Statistically significant?  {result['significant']}")
    print(f"  CI excludes zero?           {not ci['includes_zero']}")
    print(f"  Business impact (monthly):  NOK {revenue['incremental_revenue']:,}")
    print(f"  Recommendation:             {'SHIP IT' if result['significant'] else 'DO NOT SHIP'}")


# RUN EVERYTHING


if __name__ == "__main__":
    run_full_example()

    
    my_baseline    = 0.08   # your current conversion rate
    my_mde         = 0.015  # the lift you want to detect
    my_daily_users = 1000   # your daily traffic on the page

    my_n = calculate_sample_size(my_baseline, my_mde)
    my_duration = calculate_test_duration(my_n, my_daily_users)
    print(f"  Sample size needed: {my_n:,} per group")
    print(f"  Test duration:      {my_duration['total_days']} days")