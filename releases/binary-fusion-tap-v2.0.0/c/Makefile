CC=gcc
CFLAGS=-O3 -Wall
TARGET=binary_fusion_tap

all: $(TARGET)

$(TARGET): binary_fusion_tap.c
	$(CC) $(CFLAGS) binary_fusion_tap.c -o $(TARGET)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)
