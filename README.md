# MountainTrails
This code was generated to aid in visualizing terrain conditions at ski resorts. Comparing online snow reports with busy trail maps manually became frustrating and I became interested in generating my own version of trail maps that incorporated up-to-date information from the reports. 

Example snow report for 03/02/2024! (May take a moment to load in the browser) 
![Generated Image](Daily_Trail_Maps/Wildcat_2024_03_02.png) 
                                                                                                                                                                                                                                                                    
## Resorts Currently Supported
The process to adjust the maps and manually separate out each run takes a little while photoshopping by hand, so this list will *slowly* grow over time. 
- Wildcat Mountain, White Mountains NH

## What The Code Does
The snow report is pulled from the resort's website each day, and scraped for the terrain and lift details. Then a base map of the mountain is pulled in, and images of each run are stacked on top of the base map with the appropriate transparency/color. Open runs are their original color, and closed runs are grey and opaque. The final product is a map of the mountain with the runs colored based on the snow report.

Copyright Charlie Hanner - 2023
