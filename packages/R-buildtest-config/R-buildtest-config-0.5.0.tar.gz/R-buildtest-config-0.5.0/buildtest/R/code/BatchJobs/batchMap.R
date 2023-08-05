library(BatchJobs)
reg = makeRegistry(id = "BatchJobsExample", file.dir = tempfile(), seed = 123)
f = function(x) x^2
batchMap(reg, f, 1:10)
print(reg)

