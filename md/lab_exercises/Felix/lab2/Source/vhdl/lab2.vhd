----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/09/2019 10:47:12 AM
-- Design Name: 
-- Module Name: led_thingy_top - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity led_thingy_top is
  Port (
    btn :       in  STD_LOGIC_VECTOR(1 downto 0);
    sw :        in  STD_LOGIC_VECTOR(1 downto 0);
    led :       out  STD_LOGIC_VECTOR (3 downto 0);
    led4_r :    out STD_LOGIC;
    led4_g :    out STD_LOGIC;
    led4_b :    out STD_LOGIC;
    led5_r :    out STD_LOGIC;
    led5_g :    out STD_LOGIC;
    led5_b :    out STD_LOGIC
  );
end led_thingy_top;

architecture Behavioral of led_thingy_top is
   
    -- group of RGB led signals
    signal RGB_Led_4: std_logic_vector(0 to 2);
    -- group of RGB led signals
    signal RGB_Led_5: std_logic_vector(0 to 2);
    
    -- temporary signals for green leds that are chosen with switch(1) 
    signal led_group_1: std_logic_vector(3 downto 0);
    signal led_group_2: std_logic_vector(3 downto 0);

begin    
    
    -- buttons directly mapped to green leds when sw(1) is off    
    with btn(1 downto 0) select
        led_group_1 <=  "0001" when "00",
                        "0010" when "01",
                        "0100" when "10",
                        "1000" when others;
                        

    -- buttons directly mapped to green leds when sw(1) is on    
    led_group_2(0) <= btn(1) and btn(0);
    led_group_2(1) <= btn(1) xor btn(0);
    led_group_2(2) <= btn(1) or btn(0);
    led_group_2(3) <= btn(1) nand btn(0);
    
    -- switch that defines the behaviour of green leds
    with sw(1) select
        led <= led_group_1 when '0',
               led_group_2 when others;
        
           
    -- Some "housekeeping" first
    -- map signal "RGB_Led_4" to actual output ports
    led4_r <= RGB_Led_4(2);
    led4_g <= RGB_Led_4(1);
    led4_b <= RGB_Led_4(0);
    
    -- map signal "RGB_Led_5" to actual output ports
    led5_r <= RGB_Led_5(2);
    led5_g <= RGB_Led_5(1);
    led5_b <= RGB_Led_5(0);
            
                
    -- Control of RGB LED 4
    with btn(1 downto 0) select
        RGB_Led_4 <=    "001" when "01", --red
                        "010" when "10", --green
                        "100" when "11", --blue
                        "000" when others; --off
    
    -- Control of RGB LEDS using switches
    with sw(1 downto 0) select
        RGB_Led_5 <=    "000" when "00",
                        RGB_Led_4 when "01",
                        "111" when others;       
                        
end Behavioral;