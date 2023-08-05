library(ape)
## Test one monophyletic and one paraphyletic group on the bird.orders tree
data("bird.orders")
is.monophyletic(phy = bird.orders, tips = c("Ciconiiformes", "Gruiformes"))
is.monophyletic(bird.orders, c("Passeriformes", "Ciconiiformes", "Gruiformes"))
