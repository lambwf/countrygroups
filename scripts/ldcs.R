setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
library(countrycode)
library(tidyverse)

##list from here (couldn't find an easy to parse list of inclusion dates): https://unctad.org/topic/least-developed-countries/list

ldcs = "Angola, Benin, Burkina Faso, Burundi, Central African Republic, Chad, Comoros, Democratic Republic of the Congo, Djibouti, Eritrea, Ethiopia, Gambia, Guinea, Guinea-Bissau, Lesotho, Liberia, Madagascar, Malawi, Mali, Mauritania, Mozambique, Niger, Rwanda, Sao Tome and Principe, Senegal, Sierra Leone, Somalia, South Sudan, Sudan, Togo, Uganda, United Republic of Tanzania, Zambia, Afghanistan, Bangladesh, Cambodia, Lao People’s Democratic Republic, Myanmar, Nepal, Timor-Leste, Yemen, Haiti, Kiribati, Solomon Islands, Tuvalu"
ldcs = data.frame(strsplit(ldcs,", "))
names(ldcs) <- "Name"
ldcs <- ldcs %>% 
  mutate(Code=countrycode(Name,"country.name","iso3c")) %>% 
  select(Code,Name) %>% 
  mutate(`Year-Of-Inclusion`=NA) %>% 
  arrange(Name)

write.csv(ldcs,"../data/ldc.csv",row.names = FALSE)
