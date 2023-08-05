library(BatchJobs)
## Not run:
# Assume you have three nodes larry, curley and moe. All have 6
# cpu cores. On curley and moe R is installed under
# "/opt/R/R-current" and on larry R is installed under
# "/usr/local/R/". larry should not be used extensively because
# somebody else wants to compute there as well.
# Then a call to 'makeClusterFunctionsSSH'
# might look like this:
cluster.functions = makeClusterFunctionsSSH(
makeSSHWorker(nodename = "larry", rhome = "/usr/local/R", max.jobs = 2),
makeSSHWorker(nodename = "curley", rhome = "/opt/R/R-current"),
makeSSHWorker(nodename = "moe", rhome = "/opt/R/R-current"))
## End(Not run)

