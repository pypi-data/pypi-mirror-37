library(BatchJobs)
reg = makeRegistry(id = "BatchJobsExample", file.dir = tempfile(), seed = 123)
f = function(x) x^2
batchMap(reg, f, 1:10)
submitJobs(reg)
waitForJobs(reg)
# which square numbers are even:
filterResults(reg, fun = function(job, res) res %% 2 == 0)
