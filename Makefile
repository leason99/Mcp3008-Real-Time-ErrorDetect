#mcp3008-speed-test: mcp3008-speedtest.c
	#$(CC) $(CFLAGS) -pthread mcp3008-speedtest.c -o mcp3008-speedtest
		#python3 setup.py build_ext --inplace

all:
	gcc -pthread -shared mcp3008_lib.c lfq.c -o mcp3008.so 
	
clean:
	rm -f mcp3008-speedtest
	
	
