library(ape)
## Not run:
## Write interleaved DNA data with 100 characters per line in a DATA block
data(woodmouse)
write.nexus.data(woodmouse, file= "wood.ex.nex", interleaved = TRUE, charsperline = 100)
## Write sequential DNA data in TAXA and CHARACTERS blocks
data(cynipids)
write.nexus.data(cynipids, file = "cyn.ex.nex", format = "protein",
datablock = FALSE, interleaved = FALSE)
unlink(c("wood.ex.nex", "cyn.ex.nex"))
## End(Not run)
