pacman::p_load(tidyverse, gganimate)

# setwd("./data_science/wisar_pathfinding/other/")
heatmap <- read_delim("../heatmap_1.txt", delim = " ", col_names = c("x", "y", "prob"))

path <- read_csv("../results/heatmap_1_max_prob_path.csv") %>% 
  mutate(n = row_number()) 

x <- 
  path %>% 
  mutate(dist = sqrt((lag(x)-x)^2 + (lag(y)-y)^2))

x %>% filter(!is.na(dist)) %>% count(x,y, sort = T)

heatmap %>% 
  filter(prob > 0) %>% 
  tally()


nrow(x)
