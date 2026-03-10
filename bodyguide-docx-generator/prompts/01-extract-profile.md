# Profile Extraction Prompt

Model: Claude Sonnet 4.6
Max tokens: 4096

## System Prompt

You are a data transformation specialist that converts raw Typeform questionnaire responses into structured client profiles for personalized nutrition coaching.

## User Prompt Template

```
<task>
Analyze the following Typeform response and extract a structured client profile JSON. Interpret verbose or unclear answers into specific, actionable data. Generate appropriate dietary categories from content analysis.
</task>

<typeform_response>
{{TYPEFORM_JSON}}
</typeform_response>

<output_schema>
Return ONLY valid minified JSON matching this schema:
{"personal":{"firstName":"string","lastName":"string","email":"string","age":number,"gender":"string","heightCm":number,"currentWeightKg":number,"goalWeightKg":number},"health":{"conditions":"string|null","menopauseStatus":"string|null","menopauseSymptoms":"string|null","bloodTestResults":"string|null","sleepHours":number,"sleepQuality":"string","dailyStressLevel":number,"workStressLevel":number},"nutrition":{"dietaryPreference":"Flexitarisch|Vegetarisch|Vegan|LowCarb|Glutenfrei","intolerances":"string|null","dislikedFoods":"string|null","preferredFoods":"string|null","favoriteProteins":"string|null","cravingsTime":"string|null","cravingsHandling":"string|null","dailyWaterIntake":"string|null"},"activity":{"level":"string","currentTraining":"string|null","equipment":"string|null","dailySittingHours":"string|null"},"mealPlanning":{"prepTimePreference":"string|null","eatingOutFrequency":"string|null","cookingForHousehold":boolean,"desiredRecipes":"string|null"},"goals":{"mainGoals":"string","motivation":"string","importance":"string|null"},"additionalInfo":"string|null"}
</output_schema>

<rules>
- If dietary preference is ambiguous, default to "Flexitarisch"
- Convert stress scales (1-10) to numbers
- Extract specific food items from verbose descriptions
- Set null for genuinely missing data, never guess
- All output field names in camelCase
</rules>
```

## Typeform Field Mapping

| Typeform ref | Profile field |
|---|---|
| contact_information (first/last/email) | personal.firstName/lastName/email |
| age | personal.age |
| height | personal.heightCm |
| current_weight | personal.currentWeightKg |
| goal_weight | personal.goalWeightKg |
| Wechseljahre | health.menopauseStatus |
| Symptome_Wechseljahre | health.menopauseSymptoms |
| Blutuntersuchung_in_12_Monaten | health.bloodTestResults |
| Gesundheitliche_einschraenkungen | health.conditions |
| sleep_hours_per_night | health.sleepHours |
| sleep_quality | health.sleepQuality |
| daily_stress_level | health.dailyStressLevel |
| Stresslevel_Arbeitsalltag_1-10 | health.workStressLevel |
| nutrition_preference | nutrition.dietaryPreference |
| Nahrungsmittelunvertraeglichkeiten_Allergien | nutrition.intolerances |
| Abneigungen_Lebensmittel | nutrition.dislikedFoods |
| Lieblings_Proteinquellen | nutrition.favoriteProteins |
| Heisshunger_tageszeit | nutrition.cravingsTime |
| water_intake_per_day | nutrition.dailyWaterIntake |
| training_frequency_per_week | activity.currentTraining |
| home_training_equipment | activity.equipment |
| Stunden_sitzend_pro_Tag | activity.dailySittingHours |
| meal_prep_time_requirements | mealPlanning.prepTimePreference |
| eating_out_frequency | mealPlanning.eatingOutFrequency |
| cooking_for_household | mealPlanning.cookingForHousehold |
| desired_recipes | mealPlanning.desiredRecipes |
| main_goals | goals.mainGoals |
| goals_importance | goals.motivation |
| additional_info | additionalInfo |
