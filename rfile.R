library(dplyr)

recipes <- read.csv("C:/Users/Pietro/Principale/Coding/Python/projects/siMagna/data/italian gastronomic recipes dataset/foods/CSV/recipes.csv", sep=";")
ingredients <- read.csv("C:/Users/Pietro/Principale/Coding/Python/projects/siMagna/data/italian gastronomic recipes dataset/foods/CSV/ingredients.csv", sep=";")
recs <- recipes %>% 
    mutate(all_ingredients = list(Ingredient.ID, Ingredient.ID.1, Ingredient.ID.2, Ingredient.ID.3, Ingredient.ID.4, Ingredient.ID.5, Ingredient.ID.6, Ingredient.ID.7, Ingredient.ID.8, Ingredient.ID.9, Ingredient.ID.10, Ingredient.ID.11, Ingredient.ID.12, Ingredient.ID.13)) %>% 
    select(Name, ID, all_ingredients)

groceries <- ingredients %>% 
    filter(Class.ID %in% c(9, 15, 12, 21, 31, 34))

write.csv(groceries, "C:/Users/Pietro/Principale/Coding/Python/projects/siMagna/data/italian gastronomic recipes dataset/foods/CSV/groceries.csv")
