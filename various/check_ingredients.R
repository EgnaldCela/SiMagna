library(dplyr)
library(ggplot2)

recipes <- read.csv("C:/Users/Pietro/Principale/Coding/Python/projects/siMagna/data/italian gastronomic recipes dataset/foods/CSV/recipes.csv", sep=";")
ingredients <- read.csv("C:/Users/Pietro/Principale/Coding/Python/projects/siMagna/data/italian gastronomic recipes dataset/foods/CSV/ingredients.csv", sep=";")

recipes <- recipes[1:101, ]

groceries <- ingredients %>% 
    filter(Class.ID %in% c(9, 15, 12, 21, 31, 34))

# save the csv file
write.csv(groceries, "C:/Users/Pietro/Principale/Coding/Python/projects/siMagna/data/italian gastronomic recipes dataset/foods/CSV/groceries.csv")

count_occurrencies <- function(ingr_id) {
    counter <- sum(recipes$Ingredient.ID == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.1 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.2 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.3 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.4 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.5 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.6 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.7 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.8 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.9 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.10 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.11 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.12 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.13 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.14 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.15 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.16 == ingr_id, na.rm = TRUE) +
        sum(recipes$Ingredient.ID.17 == ingr_id, na.rm = TRUE)
    return(counter)
}

count_occurrencies(ingredients$ID)
result <- ingredients %>% 
    mutate(freq = sapply(ID, count_occurrencies))

result %>%
    sort_by(list(-result$freq)) %>%
    select(Ingredient, ID, freq) %>%
    head(150)
    # write.csv("C:/Users/Pietro/Principale/Coding/Python/projects/siMagna/data/italian gastronomic recipes dataset/foods/CSV/sorted_ingredients_test.csv")

ggplot(result) +
    geom_bar(aes(x = ID, y = sort(freq)), position="dodge", stat="identity")
    # geom_histogram(aes(x = log(freq)))
