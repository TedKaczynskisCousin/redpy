# redpy
My experiments with Python's OpenCV implementation.

If I am remembering correctly, I used a slightly modified algorithm to detect a border around a shape of a specific color and find the center of that shape.
I mapped the colors into different hues using HSV so that I can single out specific color codes and ignore other similar colors.

There is also a system to take screenshots from the monitor and analyze the visual information there. I used a crop to focus the screenshots onto the center of the screen to speed up capture time, and I also used some masks to speed up the processing itself.
Pretty sure I also used bitmaps or whatever for faster captures as well.

Borders were detected using OpenCV's contour system and the center of the shape is detected by iterating over the array of contours and doing something smart that I can no longer recall. Funny because I came up with it myself.

That's about it. There's also some debug views so you can see the live output during various stages of processing. The thing only runs when you hold down Q. I have provided some example images to play with.
