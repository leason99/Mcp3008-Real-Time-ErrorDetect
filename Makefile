#mcp3008-speed-test: mcp3008-speedtest.c
	#$(CC) $(CFLAGS) -pthread mcp3008-speedtest.c -o mcp3008-speedtest
		#python3 setup.py build_ext --inplace

all:
	gcc -pthread -shared mcp3008_lib.c  lfq.c -o mcp3008.so  -I/usr/local/include/libbson-1.0 -I/usr/local/include/libmongoc-1.0  -lbson-1.0 -lmongoc-1.0
	
clean:
	rm -f mcp3008-speedtest

pyui:
	pyuic5  ./ui/DetectErrorWidget.ui -o ./ui/DetectErrorWidget.py 
	pyuic5  ./ui/ShowHistoryWidget.ui -o ./ui/ShowHistoryWidget.py
	pyuic5  ./ui/MainWindows.ui -o ./ui/MainWindows.py 
	

