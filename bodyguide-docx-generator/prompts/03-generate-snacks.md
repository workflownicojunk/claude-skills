# Snack Card Generation Prompt

Model: Claude Sonnet 4.6 (temperature 1.0)
Max tokens: 8000

## User Prompt Template

```
<task>
Generate 24 personalized snack cards (6 per category) for the StrongerYou BodyGuide system. Each snack must be approximately 130 kcal and fully elaborated with ingredients and preparation.
</task>

<science_basis>
- One snack per day (100-150 kcal) fits within the calorie deficit
- Protein and fiber-rich for sustained satiety
- Blood sugar stabilizing
- Critical window: 19:00-20:00 (common craving attacks)
- Afternoon snack (15:00-16:00): energy for training days or protein for rest days
- Evening protein snack (22:00): casein-rich for overnight regeneration
</science_basis>

<categories>
1. VEGAN (6 snacks): plant-based only, no animal products
2. VEGETARIAN (6 snacks): no meat, but eggs/dairy allowed
3. FLEXITARIAN (6 snacks): mixed diet including meat/fish options
4. MIDNIGHT/NIGHT REGENERATION (6 snacks): casein-rich, sleep-promoting, tryptophan-containing
</categories>

<client_profile>
{{CLIENT_PROFILE_JSON}}
</client_profile>

<personalization_rules>
- Exclude all client allergens and intolerances
- Exclude disliked foods
- Prioritize preferred ingredients where possible
- Adapt to client's kitchen equipment and prep time preferences
- Each snack: name, exact calorie count (~130), complete ingredient list with amounts, step-by-step preparation
- All ingredient weights are RAW weights
- All recipes in German
</personalization_rules>

<output_format>
Return ONLY minified JSON with flat structure:
{"veganSnack1Name":"...","veganSnack1Calories":130,"veganSnack1Ingredients":"...","veganSnack1Preparation":"...","veganSnack2Name":"...",...,"vegetarianSnack1Name":"...",...,"flexitarianSnack1Name":"...",...,"midnightSnack1Name":"...",...}

Field naming pattern: [category]Snack[1-6][Name|Calories|Ingredients|Preparation]
Categories: vegan, vegetarian, flexitarian, midnight
Numbers: 1-6 for vegan/vegetarian, 1-5 for flexitarian/midnight
</output_format>
```
