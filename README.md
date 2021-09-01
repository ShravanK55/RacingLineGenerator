# Racing Line Generator

This is a project to generate racing lines on tracks created on or loaded into Blender. The current tracks are imported into Blender from Assetto Corsa using the blender [Assetto Corsa Importer/Exporter](https://github.com/leBluem/io_import_accsv/). This is an extension of a project I did during my final year as an undergraduate student. The older project was implemented in Unreal Engine 4 using custom tracks. The description and source of the original project can be found in the repository [Autonomous Car](https://github.com/ShravanK55/AutonomousCar).


# Introduction

Racing lines are paths taken by cars around a track in order to minimize the time spent driving a lap. They are lines which attempt to maximize the speed taken around the track while also minimizing the amount of distance to drive. Calculating such a line is not a simple task as various parameters are involved, such as the engine power, tire wear, track surface friction, aerodynamics, fuel load and so on. All these parameters affect how a driver approaches a corner and changes the path as well as throttle characteristics that they might take. Since a racing line cannot be calculated by using just math, we need a generalized approach which can take into account all these parameters and produce an output that can work on any track or car configuration. This is where genetic algorithms come in.

Genetic algorithms are used to generate solutions for problems that typically require optimization of it's input or problems that require exploration over a solution space. In this case, since we need to do a bit of both, in terms of minimizing the lap time as well as searching for newer ways to move around the track, these algorithms are a perfect fit. An initial random solution space is generated and optimized over several generations to produce an optimized racing line at the end of the algorithm.

# Implementation

Currently, a (μ + λ) evolutionary strategy with mutated mutabilities is used. More information on the algorithm can be found in the video for [evolutionary strategies](https://www.youtube.com/watch?v=mxNFeYZFdps&t=1318s). The eventual goal is to utilize the [CMA-ES](https://github.com/leBluem/io_import_accsv/) algorithm as it is an incredibly good algorithm that can explore and find the global minima in a limited amount of iterations by modifying the amount we search over a generation depending on the mean and variance of the population.
Lap times are used as the fitness measurement of a candidate/solution. The lesser the lap time, the higher the fitness. Lap times are calculated using the information from the paper for [Lap Time Simulation](http://www.jameshakewill.com/Lap_Time_Simulation.pdf).

# Screenshots

[Track imported into Blender](https://i.imgur.com/osTFYnV.png)

[Sample output after 15 generations](https://i.imgur.com/yYR68Ho.png)

[Velocity graph of algorithm v/s telemetry of a 2021 F1 car](https://i.imgur.com/u7myOng.png)

# Next Steps

- Currently, the project uses a very inefficient evolutionary strategy. The strategy used is prone to being stuck in local optima in spite of the mutations and variance introduced. In order to resolve this, the CMA-ES algorithm needs to be implemented.
- Add detailed statistics and telemetry publishing.
- Export generated track data.
- Compare with AI in Assetto Corsa.
