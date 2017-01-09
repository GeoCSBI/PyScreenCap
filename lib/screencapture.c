#include <stdio.h>
#include <X11/X.h>
#include <X11/Xutil.h>
#include <X11/Xlib.h>
//Compile hint:gcc -shared -O3 -lX11 -fPIC -Wl,-soname,screencaputre -o screencapture.so screencapture.c

void getScreen(const int, const int, const int, const int, unsigned char *);
void getScreen(const int xx, const int yy, const int W, const int H, /*out*/ unsigned char *data){
	
	Display *display = XOpenDisplay(NULL);
	Window root = DefaultRootWindow(display);

	XImage *image = XGetImage(display, root, xx, yy, W, H, AllPlanes, ZPixmap);

	unsigned long red_mask = image->red_mask;
	unsigned long green_mask = image->green_mask;
	unsigned long blue_mask = image->blue_mask;

	int x, y;
	int i = 0;

	for(y = 0; y < H; y++){
		for(x = 0; x < W; x++){
			unsigned long pixel = XGetPixel(image, x, y);
			unsigned char blue = (pixel & blue_mask);
			unsigned char green = (pixel & green_mask) >> 8;
			unsigned char red = (pixel & red_mask) >> 16;
			
			data[i + 2] = blue;
			data[i + 1] = green;
			data[i + 0] = red;
			i += 3; 
		}	

	}

	XDestroyImage(image);
	XDestroyWindow(display, root);
	XCloseDisplay(display);

}