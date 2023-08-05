library(BatchJobs)
# generating example results:
reg1 = makeRegistry(id = "BatchJobsExample1", file.dir = tempfile(), seed = 123)
f = function(x) x^2
batchMap(reg1, f, 1:20)
submitJobs(reg1)
waitForJobs(reg1)
