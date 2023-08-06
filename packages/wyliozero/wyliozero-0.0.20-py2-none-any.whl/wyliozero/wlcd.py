import Adafruit_CharLCD as LCD


lcd_rs        = 12 
lcd_en        = 25
lcd_d4        = 6
lcd_d5        = 26
lcd_d6        = 24
lcd_d7        = 16


# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

single = None


# Initialize the LCD using the pins above.
def lcd():
    global single
    if (single == None):
        single = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
    else:
        pass
    return single
