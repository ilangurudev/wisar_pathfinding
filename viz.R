pacman::p_load(tidyverse)


heatmap <- read_delim("./heatmap_1.txt", delim = " ", col_names = c("x", "y", "prob"))

prob_sub <- heatmap %>% filter(prob>0)

ggplot(heatmap,aes(x,y)) + 
  geom_point(aes(col = prob)) +
  scale_color_gradient(low = "#440154FF", high = "#FDE725FF")
  


heatmap %>% 
  filter(prob > 0) %>% 
  mutate(dist = sqrt(x^2 + y^2)) %>% 
  arrange(dist)
  # filter(dist == min(dist))
