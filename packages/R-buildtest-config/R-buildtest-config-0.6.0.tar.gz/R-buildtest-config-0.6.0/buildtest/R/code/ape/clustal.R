library(ape)
## Not run:
### display the options:
clustal()
muscle()
tcoffee()
data(woodmouse)
### open gaps more easily:
clustal(woodmouse, pw.gapopen = 1, pw.gapext = 1)
### T-Coffee requires negative values (quite slow; muscle is much faster):
tcoffee(woodmouse, MoreArgs = "-gapopen=-10 -gapext=-2")
## End(Not run)
