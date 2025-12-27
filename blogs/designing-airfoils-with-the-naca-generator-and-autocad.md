---
slug: "designing-airfoils-with-the-naca-generator-and-autocad"
coverImg: "https://github.com/user-attachments/assets/c157e799-f2f2-4a7e-87f7-71064cb4cc34"
title: "Designing Airfoils with the NACA Generator and AutoCAD"
desc: "Learn how to set up a React project with Vite for lightning-fast development."
date: "2023-12-04"
tags:
  - Engineering
hidden: false
---
# Designing Airfoils with the NACA Generator and AutoCAD

Recently, I was challenged in one of my engineering classes to design an efficient blade for a wind turbine. Sadly, my lack of mathematical knowledge heavily hindered my chances of creating a quality blade within the time constraints. However, upon research I discovered the [NACA Airfoil Generator](http://airfoiltools.com/airfoil/naca4digit), a website which consolidates air foil data and publishes them under various IDs, provided data points which I could later transform into splines in [AutoCAD](https://www.autodesk.com/) and turn into a 3D model.


![image](https://github.com/user-attachments/assets/c157e799-f2f2-4a7e-87f7-71064cb4cc34)


## Understanding the NACA Generator
As I mentioned before I used the NACA Generator to generate points along an airfoils profile. The generator has a database of over 1,000 air foils. But for the purposes of this project I used the NACA **4 digit** air foil generator. The 4 digits represent three different values to modify your airfoil. The first digit designates the camber, the second digit is the position of the maximum camber, and the last two digits represent the thickness. There are also 5 digit airfoils, a 6 series air foil, and other features on the website which I won't delve into for the purposes of this project, but please explore for yourself all the cool features that the Airfoil Generator has to offer! For this project, I opted to used the default 4 digit airfoil, __the NACA 2412__.

## Parsing the Data Points Using Python
Once you have selected an airfoil it is time to bring this data into our script. The data provided by the Airfoil Generator doesn't smoothly transfer. Here is a sample of some data created by the generator:
```
NACA 2412 Airfoil M=2.0% P=40.0% T=12.0%
  1.000084  0.001257
  0.998557  0.001575
  0.993984  0.002524
  0.986392  0.004086
  0.975825  0.006231
  0.962343  0.008922
  0.946027  0.012110
  0.926971  0.015740
  0.905287  -0.019752
```
Luckily this is opportunity for us to practice Regex. I began by pasting the data I received from the generator into a ".txt" file. Then I applied the following Regex pattern,
```
f = open(datFilePath, "r")
results = re.findall("-?\d\.\d{6}", f.read())
f.close()
```
This pattern matched all the data points in the file and put them into array. If you are curious how this pattern works please visit [Regex101](https://regex101.com/), and you can experiment writing your own pattern for text. Now that we have collected all the data points in an array we know that all the even indexes (0,2,4,6...) are the x-value of one point along the spline. And similarly all the odd indexes are the y-values of one point along the spline. Knowing this we are prepared to generate our first spline.

## Creating an AutoCAD Script
Now that we have data points for a spline that are accessible via our python array we can programmatically write a script that'll generate a spline for us. This process is fairly straight forward and simple, to begin let's look at how a spline is created from an AutoCAD script:
```
SPLINE
0.0, 0.0, 0.0 
0.5, 1.0, 0.0
1.0, 0.0, 0.0
0.5, -1.0, 0.0
# new line
# new line
# new line 
```
The command begins with SPLINE in all caps, and then on new lines three comma separated numbers representing the X, Y, and Z values of one data point.
```
f = open("results.scr", "x")

for i in range(0, len(results), 2):    
    (x, y) = (results[i], results[i + 1])
    f.write(f"{str(x)}, {str(y)}, 0")
    
f.close()
```

## Conclusion
There are more features and thoughts that I don't go into depth about above. As you most likely know, airfoils rarely have the same design along the length of the wing. So, I wrote a couple methods to linearly interpolate the size as well as the rotation across the wing. Perhaps a future feature could also include customization of the interpolation allowing for finer grain control with user defined functions. This also comes with the question of how to create windows to modify interpolation. I also added a TKinter GUI which will help with the development of a robust UI to support this project. 

After these changes I went ahead and printed three blades of two sizes. Using these blades I did a trial with the smaller size and the larger size blades, yielding the following results:

![image](https://github.com/user-attachments/assets/8749f3e1-140f-44b5-9b8a-0a0414b7b3f7)

The first trial resulted in 0.61 average volts and the second trial getting an average of 0.82 volts. All in all, this was an interesting dive into a world that I had formerly never known about in my life. And yes, I can confirm, understanding how air works and flows is very confusing!

Two blade designs:
![image](https://github.com/user-attachments/assets/90c9f1a9-28bb-4c1f-95bb-4cdccff5a488)


[Click here for the Git Repository](https://github.com/1nsomnes/AirFoilGenerator)
