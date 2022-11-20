---
title: "Chaos in HPC apps"
date: 2022-11-13T05:11:51+02:00

categories: []
tags: []
toc: false
author: "Lia Troy"
---

I originally studied chaos in the context of pure mathematical thought experiments like the Cantor set.
I had no clue that the extremely abstract material from my dynamics class would repeatedly inform the way I write code.

I first experienced applied chaos theory while writing an app that maps light past rotating black holes.

![Photo by Jeremy Perkins on Unsplash](/dynamics/black-hole.jpeg)

As I've seen more HPC applications, I've realized that understanding the app's runtime dynamics is critical to performance, and should determine the app's design.

<!--more-->

## Links to related posts

I've described chaos and stability in previous posts:
1. [Chaos 101]({{< ref "/article/chaos101.md" >}} "Post: Chaos 101")
2. [Easy signs of stability]({{< ref "/article/easy-stability.md" >}} "Post: Easy signs of stability")
3. [What is convergence?]({{< ref "/article/convergence.md" >}} "Post: What is convergence?") 

## Parallelizing chaotic black hole lensing

One summer, I applied to an [NSF funded initiative]({{< ref "https://necyberteam.org/" >}} "Northeast Cyberteam") that matches computer science students with scientists.
I was paired with a special relativity professor who was writing an HPC application.
My job was to create a software framework to parallelize Professor Kling ODEs.
The material of my dynamical systems class showed up front and center in the code design.
I was shocked. 

The path that each light ray takes through a space is called a *geodesic*.
We normally think of light in Euclidean space, shining in a straight line from the source.
However, when light passes through a lens, it changes direction.
It follows the geodesic. 

If a mass generates an enormous gravitational force, space bends around it, creating a lens.
When light shines past the mass, its geodesic curves.
In our case, Professor Kling had developed ODEs that described how the geodesics curved around a rotating black hole.

My role was to create a framework that could run many rays of light through Professor Kling's ODEs as fast as possible.
The idea was to take a bunch of light rays that started off behind the black hole, and calculate where each ray ended up after passing near the black hole.

Depending on how close the ray is to the black hole as it passes by, the geodesic takes a completely different path.
If the light ray passes very far away from the black hole, it follows a nearly straight line and is pretty unaffected by the gravitational force.
If the light ray is very close to the black hole, it is simply absorbed.

There is a boundary in between, where the ray is close enough to be affected by the black hole, but not so close as to fall in -- the chaotic region of the system.
These light rays fall into orbit around the black hole, repeatedly wrap around, then either fall in and get absorbed, or exit the orbit and continue into space.
Because the black hole rotates, its mass bends space-time asymmetrically around the axis of rotation, and the ODEs are non-linear.

From a dynamics perspective, the system is fascinating because there are both chaotic and non-chaotic regions of the system. 
In addition, it's intuitive which rays are behaving chaotically -- the ones repeatedly orbiting around the black hole.

## The math problem

We saw in the [post on chaos]({{< ref "/article/chaos101.md" >}} "Post: Chaos 101") 
that even the tiniest rounding error (such as floating point representation) is mathematically problematic in a chaotic system.
When the light rays orbit the black hole dozens of times, the discretized computations become mathematically meaningless.

Bumping up the precision to 128bit or even 512bit does not resolve this issue. ANY rounding could create a totally different result in these cases. There's no way to bound the error margin.

## The GPU branching problem

GPUs were a great choice for parallelization of this HPC app.
There was one loop that executed the computations, with each step an iteration of the loop.
GPUs have many cores, batched into sets that all share an instruction set.
That seemed perfect for our needs -- every iteration was the exact same instruction set.

At each step, a step size would be chosen and the ODE would be calculated for that distance forward. 
While the ray was progressing in a fairly straight line, the step would be large.
But, if it was in the middle of an aggressive curve, the step size would be tiny.
This is a similar process to choosing the step size in gradient descent -- according to the rate of change of the derivative, the curvature at the point.

Rays that are far away from the black hole have geodesics that are reasonably close to straight lines.
The same is true of rays that fall straight into the black hole.
In either case, neighbouring rays would have a similar number of steps.

In contrast, rays that are in the chaotic region wind around the black hole different numbers of times, meaning the overall length of their geodesics also differ widely. 
In addition, the curvature is aggressive while orbiting the black hole, so the step size gets smaller and smaller, exaggerating the discrepancy in loop iterations per ray.

Because the GPU cores are batched, they are all required to get new input data for a new ray at the same time.
If one ray does way more iterations than the rest of its batch, the cores that have completed their rays cannot get new data to crunch until the long ray is done too.
We could end up with a handful of rays running for hours while the vast majority of the GPU cores sit idle.

![Photo by Nicolene Olckers on Unsplash](/dynamics/one-seat-used.jpg)

## Two birds, one threshold

Professor Kling brought up the chaotic nature of the ODEs as part of the initial description of the system.
As a result, the software parallelization framework was specifically designed to be able to handle the different behaviours of the rays.
Fundamentally, the mathematical chaos and the GPU branching problem are two sides of the same coin, each an expression of the same system behaviour.

As a ray becomes more and more chaotic, by design, the step size shrinks quickly.
Both problems -- the math problem and the GPU branching problem -- can be completely sidestepped by simply quitting computations on any ray whose step size shrinks below a predetermined threshold.
These threads would have orders of magnitude more calculations than their neighbours, and in the end, the computation isn't mathematically viable anyway.

Not only was the step size threshold trivial to implement in this design, but the definition of "neighbouring rays" was carefully chosen.
The rays were run in concentric circles -- neighbouring rays were more likely to have similar behaviour, since they were the same distance from the center of the black hole.
These choices prevented the GPU branching problem from getting out of hand.

Running the ODEs with this software with an Nvidia A100 was 38x faster than on a single node in Boston University's cluster, using only the 24 CPU cores.

## Bottom line

Going into this project, I had only taken basic courses in classical physics.
Of my math background, I had expected my analysis courses to be most useful, helping me grasp how the ODEs describe the metric space around the black hole.
But from a software engineering perspective, the ODEs were a given, I didn't really need to understand them in order to use them in the code.
In the end, my analysis background wasn't even a fraction as useful as the dynamical systems material.

Keeping the dynamics in mind guided the app design. 
Neither I nor Professor Kling was familiar with GPUs prior to this project --
we would never have anticipated needing this type of threshold for the hardware architecture.
This is the beauty of mathematics: identifying the underlying cause, instead of putting a bandaid on the symptom.

This HPC app was a great candidate for GPU parallelization.
But, if we had been unaware of the dynamics, it's likely that we would have created an app that had terrible runtime on the GPU. 
Even worse, we wouldn't have been able to understand why.
