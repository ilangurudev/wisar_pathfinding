pacman::p_load(tidyverse, gganimate)

# setwd("./data_science/wisar_pathfinding/other/")
heatmap <- read_delim("./heatmap_1.txt", delim = " ", col_names = c("x", "y", "prob"))

prob_sub <- heatmap %>% filter(prob>0)


  


# heatmap %>% 
#   filter(prob > 0) %>% 
#   mutate(dist = sqrt(x^2 + y^2)) %>% 
#   arrange(dist)
  # filter(dist == min(dist))

path <- read_csv("./path_heatmap_1.csv") %>% 
  mutate(n = row_number())

p1 <- ggplot(heatmap,aes(x,y)) + 
  geom_point(aes(col = prob)) +
  scale_color_gradient(high = "#440154FF", low = "#FDE725FF") 

p3 <- p1 +
  geom_path(data = path, aes(x, y, frame = n, cumulative = TRUE, group = 1), col = "red" )

gganimate(p3, "output.mp4")
