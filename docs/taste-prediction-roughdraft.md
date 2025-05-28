# Taste Prediction Rough Draft

This document outlines a simple, non-ML-based approach to **taste prediction** for Adresur, forming the foundation for future improvements. The aim is to create an **early taste profile matching system** without relying on ML, using straightforward scoring and rules.

---

## 🎯 Why No ML at First?

✅ **Simplicity** – Early predictions can be based on static scoring or rules, no data needed for ML.  
✅ **Real Data First** – ML requires data. Starting small lets you gather **real buyer and cook data**.  
✅ **Better UX** – Even simple “taste profile matching” feels magical for early adopters.

---

## 🔎 Basic Approach: Manual Taste Profile Matching

1️⃣ **Taste Attributes for Dishes**  
- Each dish has **taste ratings**:  
  - Sweetness (1–5)  
  - Spiciness (1–5)  
  - Saltiness, umami, richness, etc.  
- These come from **cook input** during dish listing.

2️⃣ **Taste Preferences for Buyers**  
- Let buyers fill out a **taste profile**:  
  - “I like spicy food: 4/5”  
  - “I prefer mild sweetness: 2/5”  
- Simple form during account creation or onboarding.

3️⃣ **Scoring / Matching**  
- Create a **basic scoring function**:  
  - If a buyer likes spicy (4/5) and the dish is spicy (4/5), it’s a **good match**.  
  - If the buyer likes mild flavors and the dish is very spicy, lower the match score.  
- **No ML**: Just **simple math** (like a distance formula or weighted average).

---

## 🏗️ Example Pseudocode

```python
def match_score(buyer_profile, dish_profile):
    # Example: Euclidean distance
    score = 0
    for taste in ['spicy', 'sweet', 'salty']:
        score += (buyer_profile[taste] - dish_profile[taste]) ** 2
    return 100 - (score ** 0.5) * 10  # Convert to percentage
