name := "Running Variance"

ThisBuild / scalaVersion     := "2.11.8"
ThisBuild / version          := "1.0"

val sparkVersion = "2.2.3"
    
libraryDependencies += "org.apache.spark" %% "spark-sql" % sparkVersion
libraryDependencies += "org.apache.spark" %% "spark-core" % sparkVersion
