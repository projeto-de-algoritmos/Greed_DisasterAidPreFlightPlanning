# Greed_DisasterAidPreFlightPlanning
Multiple Micro Air Vehicles (MAVs) Pre-Flight Planning for Delivering Supplies Immediately After a Disaster.

**List Number**: X<br>
**Discipline Subject**: Greed<br>

## Students
|Number | Student |
| -- | -- |
| 17/0146251  |  João Lucas Zarbiélli |
| 19/0046945  |  Leonardo Michalski Miranda |

## About
#### Data
We generated some mock test data from Pokemon Emerald. These are the rules for it:

* The MAV can only land in the green area with low grass.

* A human can walk on areas with tall grass and low grass, but not on areas with trees.

#### Algorithms
* **1. Find closest landing zone**: Dijkstra-like algorithm with the human as its initial point. It finds the shortest path to all landing zones the human could reach and chooses only the closest one.
  * **Inputs**:
    * **Adjacency matrix**: It's a matrix with the classification of each zone. The possible classifications are: 'MAV can land and human can reach', 'MAV cannot land and human can reach', 'MAV cannot land and human cannot reach'. A plain house roof would be classified as 'MAV can land and human can reach', that's where the height map comes in.
    * **Height map**: The closest landing zone is not always the one that's closest to the human in the 2D picture the MAV took. We need to take the third dimension into account. So we can avoid landing, for example, at the roof of a house that is really close to the human. That's why our algorithm also receives a height map as input. This could be achieved in the real world with some kind of [Depth Estimation](https://beyondminds.ai/blog/depth-estimation/).
    * **Human coordinate**: The adjacency matrix coordinate of the human to whom the supply should be delivered.
  * **Outputs**:
    * The shortest path from the human to the closest landing zone and the path's total distance.

* **2. Pre-Flight Planning**: Prim-like algorithm. For each MAV, it finds a path that doesn't exceed the MAV's maximum flight time and, at the same time, heads back to the home GPS location. Each path is a cut of the GPS coordinates minimum spanning tree.
  * **Inputs**:
    * **List of GPS coordinates**: We consider that, previously to the cargo MAVs, exploration MAVs were sent to locate the humans that could receive supplies. After exploring, those MAVs messaged the Ground Control Station a list of GPS coordinates corresponding to those humans locations. But there's an issue: the error of the GPS measurements. As this is a simulation, we decided that the human could be anywhere within a radius (radius value equals to GPS error) that the cargo MAV camera can capture, but that the cargo MAVs can reach precisely the same GPS coordinate that's in the "List of GPS coordinates".
    * **Speed**: 
    * **Landing time**: Time each MAV takes to land vertically (we're not considering other kinds of landing).
    * **Take-off time**: Time each MAV takes to takeoff vertically (we're not considering other kinds of takeoff).
    * **Maximum flight time**: Maximum flight time of each MAV. We assume that there's only one type of MAV and that every battery lasts the same amount of time.
    * **Battery switching time**: Time it takes to switch the battery of a MAV when it is turned off. We're not considering recharging the batteries yet.
    * **Total number of batteries**: this is not the number of extra batteries. It is the total number of batteries.
    * **Number of MAVs**.
  * **Outputs**:
    * The mission each MAV should execute: waypoints and actions that should be taken at each waypoint.
<!--     * **Battery recharging  time**: Time it takes to recharge the battery of a MAV when it is turned off. -->


## App Gif
![App Gif](assets/app_gif.gif)

## Video (pt-br, [download link](https://raw.githubusercontent.com/projeto-de-algoritmos/Greed_DisasterAidPreFlightPlanning/main/assets/app_video.mp4))
[![](assets/app_video_splash_screen.png)](https://youtu.be/TODO)

## How to run
**Language**: Python.<br>
**Frameworks**: OpenCV; Jupyter Voilà; BinderHub.<br>
Access the [app](https://mybinder.org/v2/gh/projeto-de-algoritmos/Greed_DisasterAidPreFlightPlanning/main?urlpath=%2Fvoila%2Frender%2Fapp.ipynb) or the [notebook](https://mybinder.org/v2/gh/projeto-de-algoritmos/Greed_DisasterAidPreFlightPlanning/main?filepath=app.ipynb) with the BinderHub server.

## How to use

The app generates a random image for each iteration. Everytime you click the update button, a new random image is generated and the pre-flight planning algorithm is executed.

## References

Jupyter et al., "Binder 2.0 - Reproducible, Interactive, Sharable
Environments for Science at Scale." Proceedings of the 17th Python
in Science Conference. 2018. doi://10.25080/Majora-4af1f417-011