# Erdős–Rényi random graph generator and a Barabási–Albert random graph generator.

The Erdős–Rényi model also has an attempt of a Breadth First Search to calculate the size of the biggest diameter.
It also has the code to generate random ER graphs with an incrementing probability of connection to plot the emmergence of a Giant Component

The Barabasi-albert model has two types of generators, one of them searches for a connection starting from the first index position going forward(This means that if the first of the m0 connections will have even more connections to it since it's run through them first), and a second genertaro that picks a Node at random from the already preexisting nodes.
The BA graph also has Cummulative Binning applied to it and log-log regression.

This code was developed for the class of Network Science with the following instructions.

Erdős–Rényi model.
1 Write code for generating a random network following the G(n,p) 
2 Write code for computing the size of the giant component of a given network
3 Combining your previous code, generate a series of random networks with n = 2000 and p varying from 0.0001 to 0.005 (with steps of 0.0001).
  Show a plot of your results, with the X axis representing p and the Y axis representing the size of the giant component

Barabasi-albert model
4 Write code for generating a random network following the BA(n,m0,m)
5 The previous process should generate a scale-free network with a power law degree distribution with exponent α = 3.
  Plot the degree distribution of both your generated networks using cumulative binning and try to fit with the corresponding power law function (showing it in the plot)
