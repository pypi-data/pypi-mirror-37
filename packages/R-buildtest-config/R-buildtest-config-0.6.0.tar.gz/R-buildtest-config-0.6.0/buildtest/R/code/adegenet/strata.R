library(adegenet)
# let's look at the microbov data set:
data(microbov)
microbov
# We see that we have three vectors of different names in the 'other' slot.
# ?microbov
# These are Country, Breed, and Species
names(other(microbov))
# Let's set the strata
strata(microbov) <- data.frame(other(microbov))
microbov
# And change the names so we know what they are
nameStrata(microbov) <- ~Country/Breed/Species
## Not run:
# let's see what the strata looks like by Species and Breed:
head(strata(microbov, ~Breed/Species))
# If we didn't want the last column combined with the first, we can set
# combine = FALSE
head(strata(microbov, ~Breed/Species, combine = FALSE))
#### USING splitStrata ####
# For the sake of example, we'll imagine that we have imported our data set
# with all of the stratifications combined.
setPop(microbov) <- ~Country/Breed/Species
strata(microbov) <- NULL
# This is what our data would look like after import.
microbov
# To set our strata here, we need to use the functions strata and splitStrata
strata(microbov) <- data.frame(x = pop(microbov))
microbov # shows us that we have "one" level of stratification
head(strata(microbov)) # all strata are separated by "_"
splitStrata(microbov) <- ~Country/Breed/Species
microbov # Now we have all of our strata named and split
head(strata(microbov)) # all strata are appropriately named and split.
## End(Not run)
