#include "mbed.h"
#include "TextLCD.h"
#include <cstdint>
#include <cstdio>

// define the textLCD commands
#define LOCATE 0x01
#define CLS 0x02
#define ROWS 0x03
#define COLUMNS 0x04
#define PUTC 0x05

static BufferedSerial pc(USBTX, USBRX); // tx, rx
I2C i2c_lcd(D14, D15); // SDA, SCL
TextLCD_I2C lcd(&i2c_lcd, 0x4E, TextLCD::LCD16x2);

FileHandle *mbed::mbed_override_console(int fd)
{
   return &pc;
}

int main() {
    while(1){
        if (pc.readable()) {
            uint8_t input;
            pc.read(&input, 1);
            uint8_t command = uint8_t(input);
            ThisThread::sleep_for(100ms); 
            pc.read(&input, 1);
            uint8_t data = uint8_t(input);

            if (command == LOCATE) {
                int row = data / 16;
                int column = data % 16;
                lcd.locate(column, row);
            } else if (command == CLS) {
                lcd.cls();
            } else if (command == ROWS) {
                int rows = lcd.rows();
                pc.write(&rows, 1);
            } else if (command == COLUMNS) {
                int columns = lcd.columns();
                pc.write(&columns, 1);
            } else if (command == PUTC) {
                char cha = char(data);
                lcd.putc(cha);
            } else {
                lcd.putc('+');
            }   
        }
    }
}


