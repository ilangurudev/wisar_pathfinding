pacman::p_load(tidyverse, gganimate)
num <- 2
max_prob <- T

algo <- ifelse(max_prob, "_max_prob", "_lawnmower")

# setwd("./data_science/wisar_pathfinding/other/")
heatmap <- read_delim(paste0("../heatmap_", num, ".txt"), delim = " ", col_names = c("x", "y", "prob"))

# prob_sub <- heatmap %>% filter(prob>0)

# heatmap %>% 
#   filter(prob > 0) %>% 
#   mutate(dist = sqrt(x^2 + y^2)) %>% 
#   arrange(dist)
  # filter(dist == min(dist))

path <- read_csv(paste0("../results/heatmap_", num, algo, "_path.csv")) %>% 
  mutate(n = row_number()) %>% 
  filter(n%%1 == 0 | n == 1)

p1 <- ggplot(heatmap,aes(x,y)) + 
  geom_point(aes(col = prob)) +
  scale_color_gradient(low = "white", high = "darkred") 

p1 + 
  geom_path(data = path, aes(x, y))
# 
# p3 <- p1 +
#   geom_path(data = path, aes(x, y, frame = n, cumulative = TRUE, group = 1), col = "red" )
# 
# gganimate(p3, interval = .02)
