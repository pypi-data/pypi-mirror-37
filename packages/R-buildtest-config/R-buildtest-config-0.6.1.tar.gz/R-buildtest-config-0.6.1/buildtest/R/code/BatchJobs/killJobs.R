library(BatchJobs)
## Not run:
reg = makeRegistry(id = "BatchJobsExample", file.dir = tempfile(), seed = 123)
f = function(x) Sys.sleep(x)
batchMap(reg, f, 1:10 + 5)
submitJobs(reg)
waitForJobs(reg)
# kill all jobs currently _running_
killJobs(reg, findRunning(reg))
# kill all jobs queued or running
killJobs(reg, findNotTerminated(reg))
## End(Not run)
