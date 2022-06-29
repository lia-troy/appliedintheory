---
title: "Easy signs of a stable system"
date: 2022-06-28T11:09:07+03:00

categories: []
tags: []
toc: false
author: "Lia Troy"
---

Luckily, some systems can be easily identified as stable.
In these cases we can easily find hints that indicate that we can sleep easily at night knowing
that our system is well behaved.

![Image by Olav Ahrens Rotne on Unsplash](/dynamics/rubiks-easy-stability.jpg)

For our purposes, *stable* simply means that rounding errors do not change the output drastically.

We're going to look at a few types of stable dynamics that are very good signs that
what we expect is actually happening.

<!--more-->

## Monotone functions

Exponential functions like $e^x$ don't have minima or maxima over $\mathbb{R}$,
but that definitely doesn't force them to be chaotically mixing.
They have a property that is much easier to identify:
they're monotone.

A monotone function is either non-increasing or non-decreasing.
While some are unbounded, like $e^x$, by definition the output can't ping-pong around like we
saw with the logistic map.
It might get spread out like $\frac {1} {x}$ near 0,
but the key property is that with a monotone function, larger inputs equals larger outputs (or vice versa).
The system is predictable.

![Image by Volodymyr Hryshchenko on Unsplash](/dynamics/increasing-blocks.jpg)

Let's get down to brass tacks.
In practice, the important thing to check in monotone systems is if they are bounded.
If not, best to check if there is an asymptote that could mess up the error margin
(like $x = 0$ in $\frac {1} {x}$).
Overall, nothing crazy.

## Periodic systems

Periodic systems are the first example of a more interesting dynamic.
Like monotonicity, periodic functions are easy to identify.

![Image by Mohammad Bagher Adib Behrooz on Unsplash](/dynamics/interesting-periodicity.jpg)

Periodicity has the same meaning in dynamics as it does in physics:
a function whose output repeats in a cycle.

The easiest example of a periodic system is wallclock time.
The time right now is always exactly equal to the time 24 hours from now.
No matter if you are counting seconds, minutes, or hours, after a finite number of steps,
the wallclock time will repeat the same exact cycle indefinitely.

Even cooler, some systems start as non-periodic, but after some time enter into a periodic cycle.
Consider decimal expansion of a fraction, where each iteration is another place after the decimal
(like long division).
We all know that in decimal expansion, $\frac {1} {3} = 0.\overline{3}$.
In contrast, $\frac {1} {75} = 0.01\overline{3}$.
In both cases, the $3$ repeats indefinitely, but in $\frac{1} {75}$ this pattern doesn't start immediately.

This type of pattern is called *eventually periodic*.
For once, the math term is actually well named:
it means that even if the system does not begin as periodic, eventually, it falls into a periodic cycle.

Let's take a moment to think about what eventually periodic systems look like when they are more complex.

**Real life example:**
molecular dynamics simulations.  
If the system is eventually periodic, at first the simulation changes over time.
At some point the system enters into a repeated cycle, shifting between a finite number of states.
From this point on, there is no use in continuing the simulation,
since this cycle repeats indefinitely.
The simulation has reached stability.

## Convex functions

The subject of convexity is an entire university course, but for our purposes we don't have to go that far.
A system is convex if it has a unique minimum or maximum point.
The functions $x^2$ and phone charging are convex systems;
the functions $x^4 - x^2$ and finding the shortest route on Google maps are not
(there can be two distinct shortest paths).

The amazing thing about convex systems is that there is always one clear answer.
As long as you choose an error margin that is appropriate for the problem, you should be good to go.

![Image by Alex Krum on Unsplash](/dynamics/sand-dune-peak.jpeg)

A lot of algorithms assume that the system they are being used on is convex.
The easiest example is gradient descent, which by definition only finds local minima.
If your local minimum isn't guaranteed to also be global, you could be in for a world of hurt.

As a result of this, most machine learning algorithms also require convexity.
ML can achieve incredible results, but behind the scenes they often rely on gradient descent.
In particular, neural nets are nearly always trained using gradient descent.
Unfortunately, depending on the data, it can be difficulty to test for convexity.

## Linear systems

If you are lucky enough to be working on a problem that is reducible to a linear calculation,
you get to rely on incredibly powerful theorems and pre-cooked libraries based on those theorems.

![Image by Joel Filipe on Unsplash](/dynamics/linear-building.jpeg)

How can you identify that your system is linear? Personally, I use one of two methods.

The first method, which is way less work, is to look at all of the functions in the calculation.
If all functions are matrix or vector calculations, I know that I have a linear system for sure.
As a rule of thumb, if I see a fraction where the denominator is based on input and not static, I know that my system is not linear.
Also, if I see nonstatic input being raised to a power, it isn't linear either.

Unfortunately, this method doesn't always work.
The rigorous definition of a linear system is a function with the following two properties:

1. $f(x + y) = f(x) + f(y)$ for all inputs $x$ and $y$.
2. $f(a \cdot x) = a \cdot f(x)$ for all inputs $x$, when $a$ is a real number.

These properties are fairly restrictive, since $x^2$ isn't linear, and neither are $\frac {1} {x}$ and $x + 3$.

However, when we do have these properties, then our system can be expressed as a series of matrix multiplications.
Even better, we can rely on the following theorem:

*If $f$ is linear, and $\lambda$ is the eigenvalue with the largest absolute value, then:*
$$| f(x) - f(y) | \leq | \lambda | \cdot | x - y|$$

In other words, the distance between $x$ and $y$ never grows by more than a factor of $\lambda$
in one iteration.
This is why the input can't ping pong all over the place.

A deep dive into linear algebra and eigenvectors can show a lot more than this result.
Fundamentally, linear systems behave in structured ways.
As a result, we can use tons of prebaked tools and libraries like `numpy` to learn about the system
and predict its behaviour over time, the antithesis of chaos.

## The bottom line

We've seen now a few types of stable behaviour.
Specifically, we've seen some familiar properties,
and thought a bit about how their appearance ensures that the system behaves as expected.
The properties described have straightforward definitions, and in many cases can be easy to spot.

Moreover, in practice,
it isn't always necessary to provide a rigorous proof that your system has one of these properties.
Once you know what to look for, it's often good enough to be on the lookout,
checking heuristically to verify that the system is behaving as expected.
For example, if I see empirically that my simulation's energy is monotonically decreasing,
I can reasonably assume that my simulation is nonchaotic.

## What's next?

Since it is not always clear if our target function has any of the above properties,
the best route left is to check for convergence.

Convergence and fixed points are a bit more complex (and in my opinion, more interesting)
than the types of stability discussed here.
The next post is fully dedicated only to this new type of stability.

After that, once we have a sense of *what* we want to see in our system,
we'll talk about methodologies to test for chaotic behaviour in real applications.
Even incredibly complex applications, like HPC apps, can be analyzed for chaos within bounds.

