TARGET = stream_cli stream_ser
CC = gcc
SE_OBJ = stream_ser.o 
CL_OBJ = stream_cli.o 

all: $(TARGET)

%.o: %.c $(DEPS)
	$(CC) -w -c -o $@ $< -lpthread

stream_ser: $(SE_OBJ)
	$(CC) -o $@ $^ 

stream_cli: $(CL_OBJ)
	$(CC) -o $@ $^ -lpthread

.PHONY: clean

clean:
	rm -f $(TARGET) $(CL_OBJ) $(SE_OBJ) core *~
